import os
import shutil
import tempfile

from ipypublish.main import publish
from ipypublish.scripts import nbmerge, nbexport, pdfexport
from jsonextended.utils import MockPath
from nose.tools import eq_


class TestMain(object):
    def setup(self):
        self.file1 = MockPath('2test.ipynb', is_file=True,
                              content=r"""{
 "cells": [
      {
       "cell_type": "markdown",
       "metadata": {},
       "source": ["# a title\n","\n","some text\n"]
      },
      {
       "cell_type": "code",
       "execution_count": 2,
       "metadata": {},
       "source": [
            "a=1\n",
            "print(a)"
           ],
           "outputs": [
            {
             "name": "stdout",
             "output_type": "stream",
             "text": ["1\n"]
            }
           ]
      }
     ],
 "metadata": {
      "test_name": "notebook1",
      "kernelspec": {
       "display_name": "Python 3",
       "language": "python",
       "name": "python3"
      },
      "language_info": {
       "codemirror_mode": {
        "name": "ipython",
        "version": 3
       },
       "file_extension": ".py",
       "mimetype": "text/x-python",
       "name": "python",
       "nbconvert_exporter": "python",
       "pygments_lexer": "ipython3",
       "version": "3.6.1"
      }},
     "nbformat": 4,
     "nbformat_minor": 2
}""")
        self.file2 = MockPath('1test.ipynb', is_file=True,
                              content=r"""{
 "cells": [
      {
       "cell_type": "markdown",
       "metadata": {},
       "source": ["hallo"]
      },
      {
       "cell_type": "code",
       "execution_count": 2,
       "metadata": {},
       "source": [
            "a=1\n",
            "print(a)"
           ],
           "outputs": [
            {
             "name": "stdout",
             "output_type": "stream",
             "text": ["1\n"]
            }
           ]
      }
     ],
 "metadata": {
      "test_name": "notebook2",
      "kernelspec": {
       "display_name": "Python 3",
       "language": "python",
       "name": "python3"
      },
      "language_info": {
       "codemirror_mode": {
        "name": "ipython",
        "version": 3
       },
       "file_extension": ".py",
       "mimetype": "text/x-python",
       "name": "python",
       "nbconvert_exporter": "python",
       "pygments_lexer": "ipython3",
       "version": "3.6.1"
      }},
     "nbformat": 4,
     "nbformat_minor": 2
}""")

        self.file_with_bib = MockPath('test_with_bib.ipynb', is_file=True,
                                      content=r"""{
 "cells": [
      {
       "cell_type": "markdown",
       "metadata": {},
       "source": ["citation.\\cite{zelenyak_molecular_2016}"]
      },
      {
       "cell_type": "code",
       "execution_count": 2,
       "metadata": {},
       "source": [
            "a=1\n",
            "print(a)"
           ],
           "outputs": [
            {
             "name": "stdout",
             "output_type": "stream",
             "text": ["1\n"]
            }
           ]
      }
     ],
 "metadata": {
      "test_name": "notebook2",
      "ipub": {"bibliography":"test.bib"},
      "kernelspec": {
       "display_name": "Python 3",
       "language": "python",
       "name": "python3"
      },
      "language_info": {
       "codemirror_mode": {
        "name": "ipython",
        "version": 3
       },
       "file_extension": ".py",
       "mimetype": "text/x-python",
       "name": "python",
       "nbconvert_exporter": "python",
       "pygments_lexer": "ipython3",
       "version": "3.6.1"
      }},
     "nbformat": 4,
     "nbformat_minor": 2
}""")

        self.bibfile = MockPath('test.bib', is_file=True,
                                content=r"""
@article{kirkeminde_thermodynamic_2012,
  title = {Thermodynamic Control of Iron Pyrite Nanocrystal Synthesis with High Photoactivity and Stability},
  volume = {1},
  issn = {2050-7496},
  doi = {10.1039/C2TA00498D},
  abstract = {Non-toxic, earth abundant nanostructured semiconductors have received extensive attention recently. One of the more highly studied materials has been iron pyrite (FeS2) due to its many different promising applications. Herein, we report the thermodynamically-controlled synthesis of FeS2 nanocrystals, dependent on the reaction temperature and chemical precursors, and a Lewis acid/base model to explain the shape-controlled synthesis. The surface facet-controlled photocatalytic activity and photostability were studied and explained. This work further advances the synthesis with pyrite structure control and surface facet-dictated applications, such as photovoltaics, photocatalysts and photoelectrochemical cells.},
  timestamp = {2017-07-06T00:26:10Z},
  langid = {english},
  number = {1},
  journaltitle = {Journal of Materials Chemistry A},
  shortjournal = {J. Mater. Chem. A},
  author = {Kirkeminde, Alec and Ren, Shenqiang},
  urldate = {2017-06-18},
  date = {2012-11-29},
  pages = {49--54}
}

@article{zelenyak_molecular_2016,
  title = {Molecular Dynamics Study of Perovskite Structures with Modified Interatomic Interaction Potentials},
  volume = {50},
  issn = {0018-1439, 1608-3148},
  doi = {10.1134/S0018143916050209},
  abstract = {The structure of compounds with the perovskite structure ABX3.},
  timestamp = {2017-07-06T00:19:33Z},
  langid = {english},
  number = {5},
  journaltitle = {High Energy Chemistry},
  shortjournal = {High Energy Chem},
  author = {Zelenyak, T. Yu and Kholmurodov, Kh T. and Tameev, A. R. and Vannikov, A. V. and Gladyshev, P. P.},
  urldate = {2017-07-06},
  date = {2016-09-01},
  pages = {400--405}
}
""")

        self.directory = MockPath('dir1', structure=[self.file1, self.file2])

    def test_nbmerge_one_notebook(self):
        nb, path = nbmerge.merge_notebooks(self.file1)
        eq_(nb.metadata.test_name, "notebook1")
        eq_(len(nb.cells), 2)

    def test_nbmerge_two_notebooks(self):
        nb, path = nbmerge.merge_notebooks(self.directory)
        eq_(nb.metadata.test_name, "notebook2")
        eq_(len(nb.cells), 4)

    def test_nbexport_latex_empty(self):
        template = ''
        config = {}
        nb, path = nbmerge.merge_notebooks(self.file1)
        (body, resources), exe = nbexport.export_notebook(nb, 'Latex', config, template)
        eq_(exe, '.tex')
        eq_(body, '')

    def test_nbexport_latex_mkdown1(self):
        template = """
((* block markdowncell scoped *))
test123
((* endblock markdowncell *))
        """
        config = {}
        nb, path = nbmerge.merge_notebooks(self.file1)
        (body, resources), exe = nbexport.export_notebook(nb, 'Latex', config, template)
        eq_(exe, '.tex')
        eq_(body.strip(), 'test123')

    def test_nbexport_latex_mkdown2(self):
        template = """
((*- extends 'display_priority.tplx' -*))
((* block markdowncell scoped *))
(((cell.source)))
((* endblock markdowncell *))
        """
        config = {}
        nb, path = nbmerge.merge_notebooks(self.file1)
        (body, resources), exe = nbexport.export_notebook(nb, 'Latex', config, template)
        eq_(exe, '.tex')
        eq_(body.strip(), '# a title\n\nsome text')

    def test_nbexport_html_empty(self):
        template = ''
        config = {}
        nb, path = nbmerge.merge_notebooks(self.file1)
        (body, resources), exe = nbexport.export_notebook(nb, 'HTML', config, template)
        eq_(exe, '.html')
        eq_(body, '')

    def test_nbexport_html_mkdown1(self):
        template = """
{% block markdowncell scoped %}
test123
{% endblock markdowncell %}
        """
        config = {}
        nb, path = nbmerge.merge_notebooks(self.file1)
        (body, resources), exe = nbexport.export_notebook(nb, 'HTML', config, template)
        eq_(exe, '.html')
        eq_(body.strip(), 'test123')

    def test_nbexport_html_mkdown2(self):
        template = """
{%- extends 'display_priority.tpl' -%}
{% block markdowncell scoped %}
{{cell.source}}
{% endblock markdowncell %}
        """
        config = {}
        nb, path = nbmerge.merge_notebooks(self.file1)
        (body, resources), exe = nbexport.export_notebook(nb, 'HTML', config, template)
        eq_(exe, '.html')
        eq_(body.strip(), '# a title\n\nsome text')

    def test_pdf_export(self):

        tex_content = """
\begin{document}

\end{document}
"""
        out_folder = tempfile.mkdtemp()
        tex_path = os.path.join(out_folder, 'test.tex')
        pdf_path = os.path.join(out_folder, 'test.pdf')
        try:
            with open(tex_path, 'w') as f:
                f.write(tex_content)
            pdfexport.export_pdf(tex_path, out_folder)
            assert os.path.exists(pdf_path)
        finally:
            shutil.rmtree(out_folder)

    def test_publish_file1_latex(self):

        out_folder = tempfile.mkdtemp()
        tex_path = os.path.join(out_folder, '2test.tex')
        try:
            publish(self.file1, outpath=out_folder)
            assert os.path.exists(tex_path)
        finally:
            shutil.rmtree(out_folder)

    def test_publish_folder1_latex(self):

        out_folder = tempfile.mkdtemp()
        tex_path = os.path.join(out_folder, 'dir1.tex')
        try:
            publish(self.directory, outpath=out_folder)
            assert os.path.exists(tex_path)
        finally:
            shutil.rmtree(out_folder)

    def test_publish_file1_pdf(self):

        out_folder = tempfile.mkdtemp()
        tex_path = os.path.join(out_folder, '2test.tex')
        pdf_path = os.path.join(out_folder, '2test.pdf')
        try:
            publish(self.file1, outpath=out_folder, create_pdf=True)
            assert os.path.exists(tex_path)
            assert os.path.exists(pdf_path)
        finally:
            shutil.rmtree(out_folder)

            # def test_publish_withbib(self):

    # out_folder = tempfile.mkdtemp()
    #     tex_path = os.path.join(out_folder,'test_with_bib.tex')
    #     pdf_path = os.path.join(out_folder,'test_with_bib.pdf')
    #     with self.file_with_bib.maketemp() as file_with_bib_dir:
    #
    #         try:
    #             publish(file_with_bib_dir.name,outpath=out_folder,create_pdf=True)
    #             assert os.path.exists(tex_path)
    #             assert os.path.exists(pdf_path)
    #         finally:
    #             shutil.rmtree(out_folder)

    def test_publish_file1_html(self):

        out_folder = tempfile.mkdtemp()
        html_path = os.path.join(out_folder, '2test.html')
        try:
            publish(self.file1, outformat='html_ipypublish_main', outpath=out_folder)
            assert os.path.exists(html_path)
        finally:
            shutil.rmtree(out_folder)

    def test_publish_file1_slides(self):

        out_folder = tempfile.mkdtemp()
        html_path = os.path.join(out_folder, '2test.slides.html')
        try:
            publish(self.file1, outformat='slides_ipypublish_main', outpath=out_folder)
            assert os.path.exists(html_path)
        finally:
            shutil.rmtree(out_folder)

    def test_publish_run_all_plugins(self):
        from ipypublish.scripts import export_plugins
        for plugin_name in export_plugins.get().keys():
            out_folder = tempfile.mkdtemp()
            try:
                publish(self.file1, outformat=plugin_name, outpath=out_folder)
            finally:
                shutil.rmtree(out_folder)

                # TODO files with internal files
                # TODO files with external files
