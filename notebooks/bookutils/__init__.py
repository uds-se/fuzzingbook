# Bookutils

# Define the contents of this file as a package
__all__ = ["PrettyTable", "YouTubeVideo",
           "print_file", "print_content", "HTML",
           "show_ast",
           "unicode_escape", "terminal_escape", 
           "inheritance_conflicts", "extract_class_definition", "quiz"]

# Setup loader such that workbooks can be imported directly
try:
    import IPython
    have_ipython = True
except:
    have_ipython = False

if have_ipython:
    from . import import_notebooks
    
# Set fixed seed
from . import set_fixed_seed
set_fixed_seed.set_fixed_seed()


# Check for rich output
try:
    _rich_output = get_ipython().__class__.__name__
except NameError:
    _rich_output = False

def rich_output():
    return _rich_output


# Wrapper for YouTubeVideo
def YouTubeVideo(id, width=640, height=360):
    """Replacement for IPython.YoutubeVideo, 
    with different width/height and no cookies for YouTube"""
    if have_ipython:
        from IPython.display import IFrame
        src = f"https://www.youtube-nocookie.com/embed/{id}"
        return IFrame(src, width, height)
    else:
        pass


# Checking for inheritance conflicts

# Multiple inheritance is a tricky thing.  If you have two classes $A'$ and $A''$ which both inherit from $A$, the same method $m()$ of $A$ may be overloaded in both $A'$ and $A''$.  If one now inherits from _both_ $A'$ and $A''$, and calls $m()$, which of the $m()$ implementations should be called?  Python "resolves" this conflict by simply invoking the one $m()$ method in the class one inherits from first.
# To avoid such conflicts, one can check whether the order in which one inherits makes a difference.  So try this method to compare the attributes with each other; if they refer to different code, you have to resolve the conflict.

from inspect import getattr_static, getsource

def inheritance_conflicts(c1, c2):
    """Return attributes defined differently in classes c1 and c2"""
    class c1c2(c1, c2):
        pass

    class c2c1(c2, c1):
        pass

    return [attr for attr in dir(c1c2) if getattr_static(
        c1c2, attr) != getattr_static(c2c1, attr)]


# Given a class, extract the final definitions of all methods defined so far.

def extract_class_definition(cls, log=False):
    eldest = [c for c in cls.mro()
                if c.__name__ == cls.__name__ and
                   cls.__name__ not in {i.__name__ for i in c.__bases__}]
    n_parents = sum([[j.__name__ for j in i.__bases__] for i in eldest], [])
    s_parents = '(%s)' % ', '.join(set(n_parents)) if n_parents else ''
    buf = ["class %s%s:" % (cls.__name__, s_parents)]
    seen = set()
    i = 0
    for curcls in cls.mro():
        i += 1
        if log: print('Parent: %d' % i, curcls.__name__)
        if curcls.__name__ != cls.__name__: continue
        for fn_name in dir(curcls):
            if log: print('\t:', fn_name)
            if fn_name in seen: continue
            if fn_name == '__new__':
                continue
            fn = curcls.__dict__.get(fn_name)
            if fn is None:
                continue
            if ('function' in str(type(fn))):
                seen.add(fn_name)
                buf.append(getsource(fn))
    return '\n'.join(buf)

# Printing files with syntax highlighting
def print_file(filename, **kwargs):
    content = open(filename, "rb").read().decode('utf-8')
    print_content(content, filename, **kwargs)

def print_content(content, filename=None, lexer=None, start_line_number=None):
    from pygments import highlight, lexers, formatters
    from pygments.lexers import get_lexer_for_filename, guess_lexer

    if rich_output():
        if lexer is None:
            if filename is None:
                lexer = guess_lexer(content)
            else:
                lexer = get_lexer_for_filename(filename)

        colorful_content = highlight(
            content, lexer,
            formatters.TerminalFormatter())
        content = colorful_content.rstrip()

    if start_line_number is None:
        print(content, end="")
    else:
        content_list = content.split("\n")
        no_of_lines = len(content_list)
        size_of_lines_nums = len(str(start_line_number + no_of_lines))
        for i, line in enumerate(content_list):
            content_list[i] = ('{0:' + str(size_of_lines_nums) + '} ').format(i + start_line_number) + " " + line
        content_with_line_no = '\n'.join(content_list)
        print(content_with_line_no, end="")

def getsourcelines(function):
    """A replacement for inspect.getsourcelines(), but with syntax highlighting"""
    import inspect
    
    source_lines, starting_line_number = \
       inspect.getsourcelines(function)
       
    if not rich_output():
        return source_lines, starting_line_number
        
    from pygments import highlight, lexers, formatters
    from pygments.lexers import get_lexer_for_filename
    
    lexer = get_lexer_for_filename('.py')
    colorful_content = highlight(
        "".join(source_lines), lexer,
        formatters.TerminalFormatter())
    content = colorful_content.strip()
    return [line + '\n' for line in content.split('\n')], starting_line_number

# Showing ASTs
def show_ast(tree):
    if rich_output():
        import showast  # We can import showast only when in a notebook
        return showast.show_ast(tree)
    else:
        import ast  # Textual alternative
        print(ast.dump(tree))

# Escaping unicode characters into ASCII for user-facing strings
def unicode_escape(s, error="backslashreplace"):
    def ascii_chr(byte):
        if 0 <= byte <= 127:
            return chr(byte)
        return r"\x%02x" % byte

    bytes = s.encode('utf-8', error)
    return "".join(map(ascii_chr, bytes))

# Same, but escaping unicode only if output is not a terminal
def terminal_escape(s):
    if rich_output():
        return s
    return unicode_escape(s)


# HTML() behaves like IPython.core.display.HTML(); but if png is True or the environment
# variable RENDER_HTML is set, it converts the HTML into a PNG image.
# This is useful for producing derived formats without HTML support (LaTeX/PDF, Word, ...)

import os
firefox = None

def HTML(data=None, url=None, filename=None, png=False, headless=True, zoom=2.0):
    if not png and not 'RENDER_HTML' in os.environ:
        # Standard behavior
        import IPython.core.display
        return IPython.core.display.HTML(data=data, url=url, filename=filename)

    # Import only as needed; avoids unnecessary dependencies
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
    from IPython.core.display import Image
    import tempfile

    # Get a webdriver
    global firefox
    if firefox is None:
        options = Options()
        options.headless = headless
        profile = FirefoxProfile()
        profile.set_preference("layout.css.devPixelsPerPx", repr(zoom))
        firefox = webdriver.Firefox(firefox_profile=profile, options=options)

    # Create a URL argument
    if data is not None:
        has_html = data.find('<html')
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.html') as fp:
            if has_html:
                fp.write(data.encode('utf8'))
            else:
                fp.write(('<html>' + data + '</html>').encode('utf8'))
            fp.flush()
            return HTML(filename=fp.name, png=True)

    if filename is not None:
        return HTML(url='file://' + filename, png=True)

    assert url is not None

    # Render URL as PNG
    firefox.get(url)
    return Image(firefox.get_screenshot_as_png())
    
    
# Quizzes
# Usage: quiz('Which of these is not a fruit?', 
#             ['apple', 'banana', 'pear', 'tomato'], '27 / 9')
import uuid

import markdown
def quiztext(text):
    md_text = markdown.markdown(text)
    if md_text.startswith('<p>'):
        md_text = md_text[len('<p>'):]
    if md_text.endswith('</p>'):
        md_text = md_text[:-len('</p>')]
    return md_text

# Widget quizzes. No support for multiple-choice quizzes.
# Currently unused in favor of jsquiz(), below.
def nbquiz(question, options, correct_answer, title='Quiz', debug=False):
    import ipywidgets as widgets

    if isinstance(correct_answer, str):
        correct_answer = int(eval(correct_answer))
  
    radio_options = [(quiztext(words), i) for i, words in enumerate(options)]
    alternatives = widgets.RadioButtons(
        options = radio_options,
        description = '',
        disabled = False
    )

    title_out =  widgets.HTML(value=f'<h4>{quiztext(title)}</h4><strong>{quiztext(question)}</strong>')

    check = widgets.Button()
    
    def clear_selection(change):
        check.description = 'Submit'
        
    clear_selection(None)

    def check_selection(change):
        answer = int(alternatives.value) + 1

        if answer == correct_answer:
            check.description = 'Correct!'
        else:
            check.description = 'Incorrect!'
        return
    
    check.on_click(check_selection)
    alternatives.observe(clear_selection, names='value')
    
    return widgets.VBox([title_out, alternatives, check])

# JavaScript quizzes.
def jsquiz(question, options, correct_answer, title='Quiz', debug=True):
    if isinstance(correct_answer, list) or isinstance(correct_answer, set):
        answer_list = list(correct_answer)
        multiple_choice = True
    else:
        answer_list = [correct_answer]
        multiple_choice = False
        

    # Encode answer into binary
    correct_ans = 0
    for elem in answer_list:
        if isinstance(elem, str):
            elem = eval(elem)
        correct_ans = correct_ans | (1 << int(elem))

    quiz_id = uuid.uuid1()

    script = '''
    <script>
    function answer(quiz_id) {
        ans = 0;
        for (i = 1;; i++) {
            checkbox = document.getElementById(quiz_id + "-" + i.toString());
            if (!checkbox)
                break;
            if (checkbox.checked)
                ans |= (1 << i);
        }
        return ans;
    }
    function check_selection(quiz_id, correct_answer, multiple_choice) {
        given_answer = answer(quiz_id);
        if (given_answer == correct_answer)
        {
            document.getElementById(quiz_id + "-submit").value = "Correct!";
            for (i = 1;; i++) {
                checkbox = document.getElementById(quiz_id + "-" + i.toString());
                label = document.getElementById(quiz_id + "-" + i.toString() + "-label")
                if (!checkbox)
                    break;
    
                if (checkbox.checked) {
                    label.style.fontWeight = "bold";
                }
                else {
                    label.style.textDecoration = "line-through";
                }
            }
        }
        else 
        {
            document.getElementById(quiz_id + "-submit").value = "Try again";
            if (!multiple_choice) {
                for (i = 1;; i++) {
                    checkbox = document.getElementById(quiz_id + "-" + i.toString());
                    label = document.getElementById(quiz_id + "-" + i.toString() + "-label")

                    if (!checkbox)
                        break;
                    if (checkbox.checked) {
                        label.style.textDecoration = "line-through";
                    }
                }
            }
        }
    }
    function clear_selection(quiz_id) {
        document.getElementById(quiz_id + "-submit").value = "Submit";
    }
    </script>
    '''
    
    if multiple_choice:
        input_type = "checkbox"
        instructions = "Check all that apply."
    else:
        input_type = "radio"
        instructions = "Pick a choice."
        
    menu = "".join(f'''
        <input type="{input_type}" name="{quiz_id}" id="{quiz_id}-{i + 1}" onclick="clear_selection('{quiz_id}')">
        <label id="{quiz_id}-{i + 1}-label" for="{quiz_id}-{i + 1}">{quiztext(option)}</label><br>
    ''' for (i, option) in enumerate(options))
    
    html = f'''
    {script}
    <div class="quiz">
    <h3 class="quiz_title">{quiztext(title)}</h3>
    <p>
    <div class="quiz_question">{quiztext(question)}</div>
    </p>
    <p>
    <div class="quiz_options" title="{quiztext(instructions)}">
    {menu}
    </div>
    </p>
    <input id="{quiz_id}-submit" type="submit" value="Submit" onclick="check_selection('{quiz_id}', {correct_ans}, {int(multiple_choice)})">
    </div>
    '''
    return HTML(html)

# HTML quizzes. Not interactive.
def htmlquiz(question, options, correct_answer, title='Quiz'):
    menu = "".join(f'''
    <li> {quiztext(option)} </li>
    ''' for (i, option) in enumerate(options))
    
    html = f'''
    <h2>{quiztext(title)}</h2>
    <strong>{quiztext(question)}</strong><br/>
    <ol>
    {quiztext(menu)}
    </ol>
    <small>(Hint: {quiztext(correct_answer)})</small>
    '''
    return HTML(html)

# Text quizzes. Not interactive.
def textquiz(question, options, correct_answer, title='Quiz'):
    menu = "".join(f'''
    {i}. {option}''' for (i, option) in enumerate(options))
    
    text = f'''{title}: {question}
    {menu}

(Hint: {correct_answer})
    '''
    print(text)

# Entry point for all of the above.
def quiz(question, options, correct_answer, **kwargs):
    """Display a quiz. 
    `question` is a question string to be asked.
    `options` is a list of strings with possible answers.
    `correct_answer` is either
      * a single correct answer (number 1..) -> radio buttons will be shown; or
      * a ist of correct answers -> multiple checkboxes will be shown.
    Correct answers can also come as strings containing expressions;
      these will be displayed as is and evaluated for the correct values.
    `title` is the title to be displayed.
    """

    if 'RENDER_HTML' in os.environ:
        return htmlquiz(question, options, correct_answer, **kwargs)

    if have_ipython:
        return jsquiz(question, options, correct_answer, **kwargs)
        
    return textquiz(question, options, correct_answer, **kwargs)



# Interactive inputs. We simulate them by assigning to the global variable INPUTS.

INPUTS = []

original_input = input

def input(prompt):
    given_input = None
    try:
        global INPUTS
        given_input = INPUTS[0]
        INPUTS = INPUTS[1:]
    except:
        pass
    
    if given_input:
        if rich_output():
            display(HTML(f"<samp>{prompt}<b>{given_input}</b></samp>"))
        else:
            print(f"{prompt} {given_input}")
        return given_input
    
    return original_input(prompt)
    
def next_inputs(list=[]):
    global INPUTS
    INPUTS += list
    return INPUTS

# Make sure we quit Firefox when done
import atexit
@atexit.register
def quit_webdriver():
    if firefox is not None:
        firefox.quit()
