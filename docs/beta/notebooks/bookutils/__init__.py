# Bookutils

from typing import Any, Dict, List, Set, Optional, Union, Tuple, Type

import sys
import os

# Define the contents of this file as a package
__all__ = [
    "PrettyTable", "YouTubeVideo",
    "print_file", "print_content", "HTML",
    "show_ast", "input", "next_inputs",
    "unicode_escape", "terminal_escape", "project"
    "inheritance_conflicts", "extract_class_definition",
    "quiz", "import_notebooks", "set_fixed_seed"
]

# Setup loader such that workbooks can be imported directly
try:
    import IPython
    have_ipython = True
except:
    have_ipython = False

if have_ipython:
    from .import_notebooks import NotebookFinder  # type: ignore

# Set fixed seed
from .set_fixed_seed import set_fixed_seed
set_fixed_seed()


# Check for rich output
def rich_output() -> bool:
    try:
        get_ipython()  # type: ignore
        rich = True
    except NameError:
        rich = False

    return rich
    
# Project identifier
def project() -> Optional[str]:
    wd = os.getcwd()
    for name in [ 'fuzzingbook', 'debuggingbook' ]:
        if name in wd:
            return name

    return None

# Wrapper for YouTubeVideo
def YouTubeVideo(id: str, width: int = 640, height: int = 360) -> Any:
    """
    Replacement for IPython.YoutubeVideo, 
    with different width/height and no cookies for YouTube
    """
    if 'RENDER_HTML' in os.environ:
        # For README.md (GitHub) and PDFs:
        # Just include a (static) picture, with a link to the actual video
        import IPython.core.display
        proj = project()
        return IPython.core.display.Markdown(f'''
<a href="https://www.youtube-nocookie.com/embed/{id}" target="_blank">
<img src="https://www.{proj}.org/html/PICS/youtube.png" width={width}>
</a>
        ''')

    elif have_ipython:
        # For Jupyter: integrate a YouTube iframe
        from IPython.display import IFrame
        src = f"https://www.youtube-nocookie.com/embed/{id}"
        return IFrame(src, width, height)

    else:
        # For code: just pass
        pass


# Checking for inheritance conflicts

# Multiple inheritance is a tricky thing.  If you have two classes $A'$ and $A''$ which both inherit from $A$, the same method $m()$ of $A$ may be overloaded in both $A'$ and $A''$.  If one now inherits from _both_ $A'$ and $A''$, and calls $m()$, which of the $m()$ implementations should be called?  Python "resolves" this conflict by simply invoking the one $m()$ method in the class one inherits from first.
# To avoid such conflicts, one can check whether the order in which one inherits makes a difference.  So try this method to compare the attributes with each other; if they refer to different code, you have to resolve the conflict.

from inspect import getattr_static

def inheritance_conflicts(c1: Type[object], c2: Type[object]) -> List[str]:
    """Return attributes defined differently in classes c1 and c2"""
    class c1c2(c1, c2):  # type: ignore
        pass

    class c2c1(c2, c1):  # type: ignore
        pass

    return [attr for attr in dir(c1c2) if getattr_static(
        c1c2, attr) != getattr_static(c2c1, attr)]

# Printing files with syntax highlighting
def print_file(filename: str, **kwargs: Any) -> None:
    content = open(filename, "rb").read().decode('utf-8')
    print_content(content, filename, **kwargs)

def print_content(content: str, filename: Optional[str] = None, lexer: Optional[Any] = None, start_line_number: Optional[int] = None) -> None:
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

def getsourcelines(function: Any) -> Tuple[List[str], int]:
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

from ast import AST

# Showing ASTs
def show_ast(tree: AST) -> Optional[Any]:
    if rich_output():
        import showast  # We can import showast only when in a notebook
        return showast.show_ast(tree)
    else:
        import ast  # Textual alternative111
        print(ast.dump(tree))
        return None

# Escaping unicode characters into ASCII for user-facing strings
def unicode_escape(s: str, error: str = 'backslashreplace') -> str:
    def ascii_chr(byte: int) -> str:
        if 0 <= byte <= 127:
            return chr(byte)
        return r"\x%02x" % byte

    bytes = s.encode('utf-8', error)
    return "".join(map(ascii_chr, bytes))

# Same, but escaping unicode only if output is not a terminal
def terminal_escape(s: str) -> str:
    if rich_output():
        return s
    return unicode_escape(s)


# HTML() behaves like IPython.core.display.HTML(); but if png is True or the environment
# variable RENDER_HTML is set, it converts the HTML into a PNG image.
# This is useful for producing derived formats without HTML support (LaTeX/PDF, Word, ...)

import os
firefox = None

def HTML(data: Optional[str] = None, 
         url: Optional[str] = None, 
         filename: Optional[str] = None, 
         png: bool = False,
         headless: bool = True,
         zoom: float = 2.0) -> Any:

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
import html

def quiztext(text: Union[str, object]) -> str:
    if not isinstance(text, str):
        text = str(text)
    md_text = markdown.markdown(text)
    if md_text.startswith('<p>'):
        md_text = md_text[len('<p>'):]
    if md_text.endswith('</p>'):
        md_text = md_text[:-len('</p>')]
    return md_text

# Widget quizzes. No support for multiple-choice quizzes.
# Currently unused in favor of jsquiz(), below.
def nbquiz(question: str, options: List[str], correct_answer: int, 
    globals: Optional[Dict[str, Any]], 
    title: str = 'Quiz', debug: bool = False) -> object:
    import ipywidgets as widgets

    if isinstance(correct_answer, str):
        correct_answer = int(eval(correct_answer, globals))
  
    radio_options = [(quiztext(words), i) for i, words in enumerate(options)]
    alternatives = widgets.RadioButtons(
        options = radio_options,
        description = '',
        disabled = False
    )

    title_out =  widgets.HTML(value=f'<h4>{quiztext(title)}</h4><strong>{quiztext(question)}</strong>')

    check = widgets.Button()
    
    def clear_selection(change: Any) -> None:
        check.description = 'Submit'
        
    clear_selection(None)

    def check_selection(change: Any) -> None:
        answer = int(alternatives.value) + 1

        if answer == correct_answer:
            check.description = 'Correct!'
        else:
            check.description = 'Incorrect!'
        return
    
    check.on_click(check_selection)
    alternatives.observe(clear_selection, names='value')
    
    return widgets.VBox([title_out, alternatives, check])
    
def escape_quotes(s: str) -> str:
    return html.escape(s.replace("'", r"\'"))

# JavaScript quizzes.
def jsquiz(question: str, 
           options: List[str], 
           correct_answer: Union[str, int, List[int], Set[int]], 
           globals: Dict[str, Any], 
           title: str = "Quiz", 
           debug: bool = True) -> Any:  # should be IPython.core.display

    hint = ""
    if isinstance(correct_answer, str):
        hint = correct_answer
        correct_answer = eval(correct_answer, globals)

    answer_list: List[int] = []
    if isinstance(correct_answer, list) or isinstance(correct_answer, set):
        answer_list = list(correct_answer)
        multiple_choice = True
    elif isinstance(correct_answer, int) or isinstance(correct_answer, float):
        answer_list = [int(correct_answer)]
        multiple_choice = False
    else:
        raise TypeError("correct_answer must be list, set, int, or float")

    # Encode answer into binary
    correct_ans = 0
    for elem in answer_list:
        if isinstance(elem, str):
            elem = eval(elem, globals)

        correct_ans = correct_ans | (1 << int(elem))

    quiz_id = uuid.uuid1()

    script = '''
    <script>
    var bad_answers = new Map();

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
    function check_selection(quiz_id, correct_answer, multiple_choice, hint) {
        given_answer = answer(quiz_id);
        if (given_answer == correct_answer)
        {
            document.getElementById(quiz_id + "-submit").value = "Correct!";
            document.getElementById(quiz_id + "-hint").innerHTML = "";

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
            
            if (!bad_answers.has(quiz_id)) {
                bad_answers.set(quiz_id, 1);
            }
            else {
                bad_answers.set(quiz_id, bad_answers.get(quiz_id) + 1);
            }

            if (bad_answers.get(quiz_id) >= 2 && hint.length > 0) {
                document.getElementById(quiz_id + "-hint").innerHTML = 
                    "&nbsp;&nbsp;(Hint: <code>" + hint + "</code>)";
            }

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
        document.getElementById(quiz_id + "-hint").innerHTML = "";
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
    
    html_fragment = f'''
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
    <input id="{quiz_id}-submit" type="submit" value="Submit" onclick="check_selection('{quiz_id}', {correct_ans}, {int(multiple_choice)}, '{escape_quotes(hint)}')">
    <span class="quiz_hint" id="{quiz_id}-hint"></span>
    </div>
    '''
    return HTML(html_fragment)

# HTML quizzes. Not interactive.
def htmlquiz(question: str, 
             options: List[str], 
             correct_answer: Any, 
             globals: Optional[Dict[str, Any]] = None,
             title: str = 'Quiz') -> Any:  # should be IPython.core.display.HTML
    
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
def textquiz(question: str, options: List[str], correct_answer: Any, globals: Optional[Dict[str, Any]] = None, title: str = 'Quiz') -> None:
    menu = "".join(f'''
    {i}. {option}''' for (i, option) in enumerate(options))
    
    text = f'''{title}: {question}
    {menu}

(Hint: {correct_answer})
    '''
    print(text)

# Entry point for all of the above.
def quiz(question: str, options: List[str], 
         correct_answer: Union[str, int, List[int]],
         globals: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:
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
    
    if globals is None:
        globals = {}

    if 'RENDER_HTML' in os.environ:
        return htmlquiz(question, options, correct_answer, globals, **kwargs)

    if have_ipython:
        return jsquiz(question, options, correct_answer, globals, **kwargs)
        
    return textquiz(question, options, correct_answer, globals, **kwargs)



# Interactive inputs. We simulate them by assigning to the global variable INPUTS.

INPUTS: List[str] = []

original_input = input

def input(prompt: str) -> str:
    given_input = None
    try:
        global INPUTS
        given_input = INPUTS[0]
        INPUTS = INPUTS[1:]
    except:
        pass
    
    if given_input:
        if rich_output():
            from IPython.display import display
            display(HTML(f"<samp>{prompt}<b>{given_input}</b></samp>"))
        else:
            print(f"{prompt} {given_input}")
        return given_input
    
    return original_input(prompt)
    
def next_inputs(list: List[str] = []) -> List[str]:
    global INPUTS
    INPUTS += list
    return INPUTS

# Make sure we quit Firefox when done
import atexit
@atexit.register
def quit_webdriver() -> None:
    if firefox is not None:
        firefox.quit()
