#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Fuzzing in the Large" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/FuzzingInTheLarge.html
# Last change: 2021-06-08 12:04:14+02:00
#
# Copyright (c) 2021 CISPA Helmholtz Center for Information Security
# Copyright (c) 2018-2020 Saarland University, authors, and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

r'''
The Fuzzing Book - Fuzzing in the Large

This file can be _executed_ as a script, running all experiments:

    $ python FuzzingInTheLarge.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.FuzzingInTheLarge import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/FuzzingInTheLarge.html

The Python `FuzzManager` package allows for programmatic submission of failures from a large number of (fuzzed) programs.  One can query crashes and their details, collect them into buckets to ensure thay will be treated the same, and also retrieve coverage information for debugging both programs and their tests.


For more details, source, and documentation, see
"The Fuzzing Book - Fuzzing in the Large"
at https://www.fuzzingbook.org/html/FuzzingInTheLarge.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Fuzzing in the Large
# ====================

if __name__ == '__main__':
    print('# Fuzzing in the Large')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from . import Fuzzer

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Collecting Crashes from Multiple Fuzzers
## ----------------------------------------

if __name__ == '__main__':
    print('\n## Collecting Crashes from Multiple Fuzzers')



from graphviz import Digraph

if __name__ == '__main__':
    g = Digraph()
    server = 'Crash Server'
    g.node('Crash Database', shape='cylinder')
    for i in range(1, 7):
        g.edge('Fuzzer ' + repr(i), server)
    g.edge(server, 'Crash Database')
    g

## Running a Crash Server
## ----------------------

if __name__ == '__main__':
    print('\n## Running a Crash Server')



### Setting up the Server

if __name__ == '__main__':
    print('\n### Setting up the Server')



import os
import shutil

if __name__ == '__main__':
    if os.path.exists('FuzzManager'):
        shutil.rmtree('FuzzManager')

if __name__ == '__main__':
    import os
    os.system(f'git clone https://github.com/MozillaSecurity/FuzzManager')

if __name__ == '__main__':
    import os
    os.system(f'pip install -r FuzzManager/server/requirements.txt > /dev/null')

if __name__ == '__main__':
    import os
    os.system(f'cd FuzzManager/server; python ./manage.py migrate > /dev/null')

if __name__ == '__main__':
    import os
    os.system(f'(cd FuzzManager/server; echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(\'demo\', \'demo@fuzzingbook.org\', \'demo\')" | python manage.py shell)')

import subprocess
import sys

if __name__ == '__main__':
    result = subprocess.run(['python', 
                             'FuzzManager/server/manage.py',
                             'get_auth_token',
                             'demo'], 
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    err = result.stderr.decode('ascii')
    if len(err) > 0:
        print(err, file=sys.stderr, end="")

if __name__ == '__main__':
    token = result.stdout
    token = token.decode('ascii').strip()
    token

if __name__ == '__main__':
    assert len(token) > 10, "Invalid token " + repr(token)

if __name__ == '__main__':
    home = os.path.expanduser("~")
    conf = os.path.join(home, ".fuzzmanagerconf")

if __name__ == '__main__':
    fuzzmanagerconf = """
[Main]
sigdir = /home/example/fuzzingbook
serverhost = 127.0.0.1
serverport = 8000
serverproto = http
serverauthtoken = %s
tool = fuzzingbook
""" % token

if __name__ == '__main__':
    with open(conf, "w") as file:
        file.write(fuzzmanagerconf)

from pygments.lexers.configs import IniLexer

from .bookutils import print_file

if __name__ == '__main__':
    print_file(conf, lexer=IniLexer())

### Starting the Server

if __name__ == '__main__':
    print('\n### Starting the Server')



from multiprocessing import Process

import subprocess

def run_fuzzmanager():
    def run_fuzzmanager_forever():
        proc = subprocess.Popen(['python', 'FuzzManager/server/manage.py',
                                 'runserver'],
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)

        while True:
            line = proc.stdout.readline()
            print(line, end='')

    fuzzmanager_process = Process(target=run_fuzzmanager_forever)
    fuzzmanager_process.start()

    return fuzzmanager_process

if __name__ == '__main__':
    fuzzmanager_process = run_fuzzmanager()

import time

if __name__ == '__main__':
    time.sleep(2)

### Logging In

if __name__ == '__main__':
    print('\n### Logging In')



if __name__ == '__main__':
    fuzzmanager_url = "http://127.0.0.1:8000"

if __name__ == '__main__':
    from IPython.display import display, Image

from .bookutils import HTML, rich_output

from .GUIFuzzer import start_webdriver  # minor dependency

if __name__ == '__main__':
    gui_driver = start_webdriver(headless=True, zoom=1.2)

if __name__ == '__main__':
    gui_driver.set_window_size(1400, 600)

if __name__ == '__main__':
    gui_driver.get(fuzzmanager_url)

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

if __name__ == '__main__':
    username = gui_driver.find_element_by_name("username")
    username.send_keys("demo")

if __name__ == '__main__':
    password = gui_driver.find_element_by_name("password")
    password.send_keys("demo")

if __name__ == '__main__':
    login = gui_driver.find_element_by_tag_name("button")
    login.click()
    time.sleep(1)

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

## Collecting Crashes
## ------------------

if __name__ == '__main__':
    print('\n## Collecting Crashes')



if __name__ == '__main__':
    import os
    os.system(f'git clone https://github.com/choller/simply-buggy')

if __name__ == '__main__':
    import os
    os.system(f'(cd simply-buggy && make)')

from .bookutils import print_file

if __name__ == '__main__':
    print_file("simply-buggy/simple-crash.cpp")

if __name__ == '__main__':
    print_file("simply-buggy/simple-crash.fuzzmanagerconf", lexer=IniLexer())

if __name__ == '__main__':
    import os
    os.system(f'simply-buggy/simple-crash')

import subprocess

if __name__ == '__main__':
    cmd = ["simply-buggy/simple-crash"]

if __name__ == '__main__':
    result = subprocess.run(cmd, stderr=subprocess.PIPE)
    stderr = result.stderr.decode().splitlines()
    crashed = False

    for line in stderr:
        if "ERROR: AddressSanitizer" in line:
            crashed = True
            break

    if crashed:
        print("Yay, we crashed!")
    else:
        print("Move along, nothing to see...")

### Program Configurations

if __name__ == '__main__':
    print('\n### Program Configurations')



if __name__ == '__main__':
    from .FTB.ProgramConfiguration import ProgramConfiguration

if __name__ == '__main__':
    configuration = ProgramConfiguration.fromBinary('simply-buggy/simple-crash')
    (configuration.product, configuration.platform)

### Crash Info

if __name__ == '__main__':
    print('\n### Crash Info')



if __name__ == '__main__':
    from .FTB.Signatures.CrashInfo import CrashInfo

if __name__ == '__main__':
    cmd = ["simply-buggy/simple-crash"]
    result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

if __name__ == '__main__':
    stderr = result.stderr.decode().splitlines()
    stderr[0:3]

if __name__ == '__main__':
    stdout = result.stdout.decode().splitlines()
    stdout

if __name__ == '__main__':
    crashInfo = CrashInfo.fromRawCrashData(stdout, stderr, configuration)
    print(crashInfo)

### Collector

if __name__ == '__main__':
    print('\n### Collector')



if __name__ == '__main__':
    from .Collector.Collector import Collector

if __name__ == '__main__':
    collector = Collector()

if __name__ == '__main__':
    collector.submit(crashInfo);

### Inspecting Crashes

if __name__ == '__main__':
    print('\n### Inspecting Crashes')



if __name__ == '__main__':
    gui_driver.refresh()

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

if __name__ == '__main__':
    crash = gui_driver.find_element_by_xpath('//td/a[contains(@href,"/crashmanager/crashes/")]')
    crash.click()
    time.sleep(1)

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

## Crash Buckets
## -------------

if __name__ == '__main__':
    print('\n## Crash Buckets')



if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

if __name__ == '__main__':
    create = gui_driver.find_element_by_xpath('//a[contains(@href,"/signatures/new/")]')
    create.click()
    time.sleep(1)

if __name__ == '__main__':
    gui_driver.set_window_size(1400, 1200)

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

if __name__ == '__main__':
    save = gui_driver.find_element_by_name("submit_save")
    save.click()
    time.sleep(1)

### Crash Signatures

if __name__ == '__main__':
    print('\n### Crash Signatures')



if __name__ == '__main__':
    gui_driver.set_window_size(1400, 800)
    Image(gui_driver.get_screenshot_as_png())

### Coarse-Grained Signatures

if __name__ == '__main__':
    print('\n### Coarse-Grained Signatures')



if __name__ == '__main__':
    print_file("simply-buggy/out-of-bounds.cpp")

import os
import random
import subprocess
import tempfile
import sys

#### Excursion: `escapelines()` implementatipn

if __name__ == '__main__':
    print('\n#### Excursion: `escapelines()` implementatipn')



def isascii(s):
    return all([0 <= ord(c) <= 127 for c in s])

if __name__ == '__main__':
    isascii('Hello,')

def escapelines(bytes):
    def ascii_chr(byte):
        if 0 <= byte <= 127:
            return chr(byte)
        return r"\x%02x" % byte

    def unicode_escape(line):
        ret = "".join(map(ascii_chr, line))
        assert isascii(ret)
        return ret

    return [unicode_escape(line) for line in bytes.splitlines()]

if __name__ == '__main__':
    escapelines(b"Hello,\nworld!")

if __name__ == '__main__':
    escapelines(b"abc\xffABC")

#### End of Excursion

if __name__ == '__main__':
    print('\n#### End of Excursion')



if __name__ == '__main__':
    cmd = ["simply-buggy/out-of-bounds"]

    # Connect to crash server
    collector = Collector()

    random.seed(2048)

    crash_count = 0
    TRIALS = 20

    for itnum in range(0, TRIALS):
        rand_len = random.randint(1, 1024)
        rand_data = bytes([random.randrange(0, 256) for i in range(rand_len)])

        (fd, current_file) = tempfile.mkstemp(prefix="fuzztest", text=True)
        os.write(fd, rand_data)
        os.close(fd)

        current_cmd = []
        current_cmd.extend(cmd)
        current_cmd.append(current_file)

        result = subprocess.run(current_cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        stdout = []   # escapelines(result.stdout)
        stderr = escapelines(result.stderr)
        crashed = False

        for line in stderr:
            if "ERROR: AddressSanitizer" in line:
                crashed = True
                break

        print(itnum, end=" ")

        if crashed:
            sys.stdout.write("(Crash) ")

            # This reads the simple-crash.fuzzmanagerconf file
            configuration = ProgramConfiguration.fromBinary(cmd[0])

            # This reads and parses our ASan trace into a more generic format,
            # returning us a generic "CrashInfo" object that we can inspect
            # and/or submit to the server.
            crashInfo = CrashInfo.fromRawCrashData(stdout, stderr, configuration)

            # Submit the crash
            collector.submit(crashInfo, testCase = current_file)

            crash_count += 1

        os.remove(current_file)

    print("")
    print("Done, submitted %d crashes after %d runs." % (crash_count, TRIALS))

if __name__ == '__main__':
    gui_driver.get(fuzzmanager_url + "/crashmanager/crashes")

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

## Collecting Code Coverage
## ------------------------

if __name__ == '__main__':
    print('\n## Collecting Code Coverage')



if __name__ == '__main__':
    print_file("simply-buggy/maze.cpp")

if __name__ == '__main__':
    import os
    os.system(f'(cd simply-buggy && make clean && make coverage)')

if __name__ == '__main__':
    import os
    os.system(f'git clone https://github.com/choller/simply-buggy $HOME/simply-buggy-server    ')

if __name__ == '__main__':
    import os
    os.system(f'python3 FuzzManager/server/manage.py setup_repository simply-buggy GITSourceCodeProvider $HOME/simply-buggy-server')

import random
import subprocess

if __name__ == '__main__':
    random.seed(0)
    cmd = ["simply-buggy/maze"]

    constants = [3735928559, 1111638594]; 

    TRIALS = 1000

    for itnum in range(0, TRIALS):
        current_cmd = []
        current_cmd.extend(cmd)

        for _ in range(0, 4):
            if random.randint(0, 9) < 3:
                current_cmd.append(str(constants[
                    random.randint(0, len(constants) - 1)]))
            else:
                current_cmd.append(str(random.randint(-2147483647, 2147483647)))

        result = subprocess.run(current_cmd, stderr=subprocess.PIPE)
        stderr = result.stderr.decode().splitlines()
        crashed = False

        if stderr and "secret" in stderr[0]:
            print(stderr[0])

        for line in stderr:
            if "ERROR: AddressSanitizer" in line:
                crashed = True
                break

        if crashed:
            print("Found the bug!")
            break

    print("Done!")

if __name__ == '__main__':
    import os
    os.system(f'export PATH=$HOME/.cargo/bin:$PATH; grcov simply-buggy/ -t coveralls+ --commit-sha $(cd simply-buggy && git rev-parse HEAD) --token NONE -p `pwd`/simply-buggy/ > coverage.json')

if __name__ == '__main__':
    import os
    os.system(f'python3 -mCovReporter --repository simply-buggy --description "Test1" --submit coverage.json')

if __name__ == '__main__':
    gui_driver.get(fuzzmanager_url + "/covmanager")

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

if __name__ == '__main__':
    first_id = gui_driver.find_element_by_xpath('//td/a[contains(@href,"/browse")]')
    first_id.click()
    time.sleep(1)

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

if __name__ == '__main__':
    maze_cpp = gui_driver.find_element_by_xpath("//*[contains(text(), 'maze.cpp')]")
    maze_cpp.click()
    time.sleep(1)

if __name__ == '__main__':
    gui_driver.set_window_size(1400, 1400)
    Image(gui_driver.get_screenshot_as_png())

if __name__ == '__main__':
    random.seed(0)
    cmd = ["simply-buggy/maze"]

    # Added the missing constant here
    constants = [3735928559, 1111638594, 3405695742]

    for itnum in range(0,1000):
        current_cmd = []
        current_cmd.extend(cmd)

        for _ in range(0,4):
            if random.randint(0, 9) < 3:
                current_cmd.append(str(
                    constants[random.randint(0, len(constants) - 1)]))
            else:
                current_cmd.append(str(random.randint(-2147483647, 2147483647)))

        result = subprocess.run(current_cmd, stderr=subprocess.PIPE)
        stderr = result.stderr.decode().splitlines()
        crashed = False

        if stderr:
            print(stderr[0])

        for line in stderr:
            if "ERROR: AddressSanitizer" in line:
                crashed = True
                break

        if crashed:
            print("Found the bug!")
            break

    print("Done!")

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Lessons Learned
## ---------------

if __name__ == '__main__':
    print('\n## Lessons Learned')



if __name__ == '__main__':
    fuzzmanager_process.terminate()

if __name__ == '__main__':
    gui_driver.quit()

import shutil

if __name__ == '__main__':
    for temp_file in ['coverage.json', 'geckodriver.log', 'ghostdriver.log']:
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == '__main__':
    home = os.path.expanduser("~")
    for temp_dir in ['coverage', 'simply-buggy', 'simply-buggy-server', 
                     os.path.join(home, 'simply-buggy-server'),
                    'FuzzManager']:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

## Next Steps
## ----------

if __name__ == '__main__':
    print('\n## Next Steps')



## Background
## ----------

if __name__ == '__main__':
    print('\n## Background')



## Exercises
## ---------

if __name__ == '__main__':
    print('\n## Exercises')



### Exercise 1: Automatic Crash Reporting

if __name__ == '__main__':
    print('\n### Exercise 1: Automatic Crash Reporting')


