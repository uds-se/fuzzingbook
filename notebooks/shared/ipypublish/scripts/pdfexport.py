#!/usr/bin/env python
""" a module for exporting latex file to pdf

"""
import logging
import os
import shutil
import tempfile
from subprocess import Popen, PIPE, STDOUT

# python 3 to 2 compatibility
try:
    from shutil import which as exe_exists
except ImportError:
    from distutils.spawn import find_executable as exe_exists

VIEW_PDF = r"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
    <meta http-equiv="content-type" content="text/html; charset=windows-1252">
    <title>View PDF</title>

    <script type="text/javascript">
 	   var filepath = "{pdf_name}";
       var timer = null;

       function refresh(){{
          var d = document.getElementById("pdf"); // gets pdf-div
          d.innerHTML = '<iframe style="position: absolute; height: 100%; border: none" id="ipdf" src='+window.filepath+'  width="100%"></iframe>';
       }}

       function autoRefresh(){{
          timer = setTimeout("autoRefresh()", 20000);
          refresh();
       }}

       function manualRefresh(){{
          clearTimeout(timer);
          refresh();
       }}
	   function check_pdf() {{
	     var newfile = document.f.userFile.value;
	     ext = newfile.substring(newfile.length-3,newfile.length);
	     ext = ext.toLowerCase();
	     if(ext != 'pdf') {{
	       alert('You selected a .'+ext+
	             ' file; please select a .pdf file instead!'+filepath);
	       return false; }}
	     else
			 alert(newfile);
		     window.filepath = newfile;
			 alert(filepath);
			 refresh();
	       return true; }}
    </script>

</head>
<body>
	<!-- <form name=f onsubmit="return check_pdf();"
	    action='' method='POST' enctype='multipart/form-data'>
	    <input type='submit' name='upload_btn' value='upload'>
		<input type='file' name='userFile' accept="application/pdf">
	</form> -->
	<button onclick="manualRefresh()">manual refresh</button>
   <button onclick="autoRefresh()">auto refresh</button>
   <div id="pdf"></div>
</body>
<script type="text/javascript">refresh();</script>
</html>
"""


class change_dir:
    """Context manager for changing the current working directory"""

    def __init__(self, new_path):
        self.newPath = os.path.expanduser(new_path)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


# python 3 to 2 compatibility
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib
try:
    basestring
except NameError:
    basestring = str


def export_pdf(texpath, outdir, files_path=None,
               convert_in_temp=False, html_viewer=True,
               debug_mode=False):
    if isinstance(texpath, basestring):
        texpath = pathlib.Path(texpath)
    if not texpath.exists() or not texpath.is_file():
        logging.error('the tex file path does not exist: {}'.format(texpath))
        raise IOError('the tex file path does not exist: {}'.format(texpath))

    texname = os.path.splitext(texpath.name)[0]

    if files_path is not None:
        if isinstance(files_path, basestring):
            files_path = pathlib.Path(files_path)
        if not files_path.exists() or not files_path.is_dir():
            logging.error('the external folder path does not exist: {}'.format(texpath))
            raise IOError('the external folder path does not exist: {}'.format(texpath))

    if not exe_exists('latexmk'):
        logging.error('requires the latexmk executable to run. See http://mg.readthedocs.io/latexmk.html#installation')
        raise RuntimeError(
            'requires the latexmk executable to run. See http://mg.readthedocs.io/latexmk.html#installation')

    if convert_in_temp:
        out_folder = tempfile.mkdtemp()
        try:
            exitcode = run_conversion(texpath, out_folder, files_path, debug_mode)
            if exitcode == 0:
                shutil.copyfile(os.path.join(out_folder, texname + '.pdf'),
                                os.path.join(outdir, texname + '.pdf'))
        finally:
            shutil.rmtree(out_folder)
    else:
        exitcode = run_conversion(texpath, outdir, files_path, debug_mode)

    if exitcode == 0:
        logging.info('pdf conversion complete')

        if html_viewer:
            view_pdf = VIEW_PDF.format(pdf_name=texname.replace(' ', '%20') + '.pdf')
            with open(os.path.join(outdir, texname + '.view_pdf.html'), 'w') as f:
                f.write(view_pdf)
        return True
    else:
        logging.error('pdf conversion failed: '
                      'Try running with pdf_debug=True')
        return False


def run_conversion(texpath, out_folder, files_folder=None, debug_mode=False):
    """ run latexmk conversion
    """

    # make sure tex file in right place
    outpath = os.path.join(out_folder, texpath.name)
    if os.path.dirname(str(texpath)) != str(out_folder):
        logging.debug('copying tex file to: {}'.format(os.path.join(str(out_folder), texpath.name)))
        shutil.copyfile(str(texpath), os.path.join(str(out_folder), texpath.name))

    # make sure the external files folder is in right place
    if files_folder is not None:
        logging.debug('external files folder set')
        outfilespath = os.path.join(out_folder, str(files_folder.name))
        if str(files_folder) != str(outfilespath):
            logging.debug('copying external files to: {}'.format(outfilespath))
            if os.path.exists(outfilespath):
                shutil.rmtree(outfilespath)
            shutil.copytree(str(files_folder), str(outfilespath))

    # run latexmk in correct folder
    with change_dir(out_folder):
        latexmk = ['latexmk', '-xelatex', '-bibtex', '-pdf']
        latexmk += [] if debug_mode else ["--interaction=batchmode"]
        logging.info('running: ' + ' '.join(latexmk + ['<outpath>']))
        latexmk += [outpath]

        def log_latexmk_output(pipe):
            for line in iter(pipe.readline, b''):
                logging.info('latexmk: {}'.format(line.decode("utf-8").strip()))

        process = Popen(latexmk, stdout=PIPE, stderr=STDOUT)
        with process.stdout:
            log_latexmk_output(process.stdout)
        exitcode = process.wait()  # 0 means success

    return exitcode
