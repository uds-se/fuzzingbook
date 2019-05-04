#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/FuzzingInTheLarge.html
# Last change: 2019-05-04 16:58:23+02:00
#
#
# Copyright (c) 2018 Saarland University, CISPA, authors, and contributors
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


# # Fuzzing In the Large

if __name__ == "__main__":
    print('# Fuzzing In the Large')




if __name__ == "__main__":
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)


if __package__ is None or __package__ == "":
    import Fuzzer
else:
    from . import Fuzzer


# ## A Crash Server

if __name__ == "__main__":
    print('\n## A Crash Server')




from graphviz import Digraph

if __name__ == "__main__":
    g = Digraph()
    server = 'Crash Server'
    g.node('Crash Database', shape='cylinder')
    for i in range(1, 7):
        g.edge('Fuzzer ' + repr(i), server)
    g.edge(server, 'Crash Database')
    g


# ## Running a Crash Server

if __name__ == "__main__":
    print('\n## Running a Crash Server')




# ### Running the Given Server

if __name__ == "__main__":
    print('\n### Running the Given Server')




# ### Running your own Server

if __name__ == "__main__":
    print('\n### Running your own Server')




import os

if __name__ == "__main__":
    if not os.path.exists('FuzzManager'):
        os.system("git clone https://github.com/MozillaSecurity/FuzzManager")
        os.system("pip install -r FuzzManager/server/requirements.txt")
        os.system("cd FuzzManager/server; python manage.py migrate")


# ### Clearing the Database

if __name__ == "__main__":
    print('\n### Clearing the Database')




import sqlite3

if __name__ == "__main__":
    db_connection = sqlite3.connect("FuzzManager/server/db.sqlite3")
    db_connection.execute("DELETE FROM crashmanager_crashentry;")
    db_connection.commit()


# ### Starting the Server

if __name__ == "__main__":
    print('\n### Starting the Server')




from multiprocessing import Process

import subprocess

def run_fuzzmanager():
    def run_fuzzmanager_forever():
        proc = subprocess.Popen(['python', 'FuzzManager/server/manage.py', 'runserver'],
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

if __name__ == "__main__":
    fuzzmanager_process = run_fuzzmanager()


import time

if __name__ == "__main__":
    time.sleep(2)


# ### Logging In

if __name__ == "__main__":
    print('\n### Logging In')




if __name__ == "__main__":
    fuzzmanager_url = "http://127.0.0.1:8000"


from IPython.display import display, Image

if __package__ is None or __package__ == "":
    from fuzzingbook_utils import HTML, rich_output
else:
    from .fuzzingbook_utils import HTML, rich_output


if __package__ is None or __package__ == "":
    from GUIFuzzer import start_webdriver
else:
    from .GUIFuzzer import start_webdriver


if __name__ == "__main__":
    gui_driver = start_webdriver(headless=True, zoom=1.2)


if __name__ == "__main__":
    gui_driver.set_window_size(1400, 600)


if __name__ == "__main__":
    gui_driver.get(fuzzmanager_url)


if __name__ == "__main__":
    Image(gui_driver.get_screenshot_as_png())


if __name__ == "__main__":
    username = gui_driver.find_element_by_name("username")
    username.send_keys("demo")


if __name__ == "__main__":
    password = gui_driver.find_element_by_name("password")
    password.send_keys("demo")


if __name__ == "__main__":
    login = gui_driver.find_element_by_tag_name("button")
    login.click()


if __name__ == "__main__":
    Image(gui_driver.get_screenshot_as_png())


# ## Collecting Crashes

if __name__ == "__main__":
    print('\n## Collecting Crashes')




if __name__ == "__main__":
    import os
    os.system(r'git clone https://github.com/choller/simply-buggy')


if __name__ == "__main__":
    import os
    os.system(r'(cd simply-buggy && make)')


if __package__ is None or __package__ == "":
    from fuzzingbook_utils import print_file
else:
    from .fuzzingbook_utils import print_file


if __name__ == "__main__":
    print_file("simply-buggy/simple-crash.cpp")


from pygments.lexers.configs import IniLexer

if __name__ == "__main__":
    print_file("simply-buggy/simple-crash.fuzzmanagerconf", lexer=IniLexer())


if __name__ == "__main__":
    import os
    os.system(r'simply-buggy/simple-crash')


import subprocess

if __name__ == "__main__":
    cmd = ["simply-buggy/simple-crash"]


if __name__ == "__main__":
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


# ### Program Configurations

if __name__ == "__main__":
    print('\n### Program Configurations')




from FTB.ProgramConfiguration import ProgramConfiguration

if __name__ == "__main__":
    configuration = ProgramConfiguration.fromBinary('simply-buggy/simple-crash')
    (configuration.product, configuration.platform)


# ### Crash Info

if __name__ == "__main__":
    print('\n### Crash Info')




from FTB.Signatures.CrashInfo import CrashInfo

if __name__ == "__main__":
    cmd = ["simply-buggy/simple-crash"]
    result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)


if __name__ == "__main__":
    stderr = result.stderr.decode().splitlines()
    stderr[0:3]


if __name__ == "__main__":
    stdout = result.stdout.decode().splitlines()
    stdout


if __name__ == "__main__":
    crashInfo = CrashInfo.fromRawCrashData(stdout, stderr, configuration)
    print(crashInfo)


# ### Collector

if __name__ == "__main__":
    print('\n### Collector')




from Collector.Collector import Collector

if __name__ == "__main__":
    collector = Collector()


if __name__ == "__main__":
    collector.submit(crashInfo);


# ### Inspecting Crashes

if __name__ == "__main__":
    print('\n### Inspecting Crashes')




if __name__ == "__main__":
    gui_driver.refresh()


if __name__ == "__main__":
    Image(gui_driver.get_screenshot_as_png())


if __name__ == "__main__":
    crash = gui_driver.find_element_by_xpath('//td/a[contains(@href,"/crashmanager/crashes/")]')
    crash.click()


if __name__ == "__main__":
    Image(gui_driver.get_screenshot_as_png())


# ## Crash Buckets

if __name__ == "__main__":
    print('\n## Crash Buckets')




if __name__ == "__main__":
    Image(gui_driver.get_screenshot_as_png())


if __name__ == "__main__":
    create = gui_driver.find_element_by_xpath('//a[contains(@href,"/signatures/new/")]')
    create.click()


if __name__ == "__main__":
    gui_driver.set_window_size(1400, 1200)


if __name__ == "__main__":
    Image(gui_driver.get_screenshot_as_png())


if __name__ == "__main__":
    save = gui_driver.find_element_by_name("submit_save")
    save.click()


# ### Crash Signatures

if __name__ == "__main__":
    print('\n### Crash Signatures')




if __name__ == "__main__":
    Image(gui_driver.get_screenshot_as_png())


# ### Coarse-Grained Signatures

if __name__ == "__main__":
    print('\n### Coarse-Grained Signatures')




if __name__ == "__main__":
    print_file("simply-buggy/out-of-bounds.cpp")


import os
import random
import subprocess
import tempfile
import sys

def isascii(s):
    return all([0 <= ord(c) <= 127 for c in s])

if __name__ == "__main__":
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

if __name__ == "__main__":
    escapelines(b"Hello,\nworld!")


if __name__ == "__main__":
    escapelines(b"abc\xffABC")


if __name__ == "__main__":
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

        result = subprocess.run(current_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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


if __name__ == "__main__":
    gui_driver.get(fuzzmanager_url + "/crashmanager/crashes")


if __name__ == "__main__":
    Image(gui_driver.get_screenshot_as_png())


# ## Collecting Code Coverage

if __name__ == "__main__":
    print('\n## Collecting Code Coverage')




if __name__ == "__main__":
    print_file("simply-buggy/maze.cpp")


if __name__ == "__main__":
    import os
    os.system(r'(cd simply-buggy && make clean && make coverage)')


if __name__ == "__main__":
    import os
    os.system(r'git clone https://github.com/choller/simply-buggy $HOME/simply-buggy-server    ')


if __name__ == "__main__":
    import os
    os.system(r'python3 FuzzManager/server/manage.py setup_repository simply-buggy GITSourceCodeProvider $HOME/simply-buggy-server')


import random
import subprocess

if __name__ == "__main__":
    random.seed(0)
    cmd = ["simply-buggy/maze"]

    constants = [3735928559, 1111638594]; 

    TRIALS = 1000

    for itnum in range(0, TRIALS):
        current_cmd = []
        current_cmd.extend(cmd)

        for _ in range(0,4):
            if random.randint(0, 9) < 3:
                current_cmd.append(str(constants[random.randint(0, len(constants) - 1)]))
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


if __name__ == "__main__":
    import os
    os.system(r'grcov simply-buggy/ -t coveralls+ --commit-sha $(cd simply-buggy && git rev-parse HEAD) --token NONE -p `pwd`/simply-buggy/ > coverage.json')


if __name__ == "__main__":
    import os
    os.system(r'python3 -mCovReporter --repository simply-buggy --description "Test1" --submit coverage.json')


if __name__ == "__main__":
    gui_driver.get(fuzzmanager_url + "/covmanager")


if __name__ == "__main__":
    Image(gui_driver.get_screenshot_as_png())


if __name__ == "__main__":
    first_id = gui_driver.find_element_by_xpath('//td/a[contains(@href,"/browse")]')
    first_id.click()


if __name__ == "__main__":
    Image(gui_driver.get_screenshot_as_png())


if __name__ == "__main__":
    maze_cpp = gui_driver.find_element_by_xpath("//*[contains(text(), 'maze.cpp')]")
    maze_cpp.click()


if __name__ == "__main__":
    Image(gui_driver.get_screenshot_as_png())


import random
import subprocess

if __name__ == "__main__":
    random.seed(0)
    cmd = ["simply-buggy/maze"]

    constants = [3735928559, 1111638594, 3405695742]; # Added the missing constant here

    for itnum in range(0,1000):
        current_cmd = []
        current_cmd.extend(cmd)

        for _ in range(0,4):
            if random.randint(0, 9) < 3:
                current_cmd.append(str(constants[random.randint(0, len(constants) - 1)]))
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


# ## Lessons Learned

if __name__ == "__main__":
    print('\n## Lessons Learned')




if __name__ == "__main__":
    fuzzmanager_process.terminate()


if __name__ == "__main__":
    gui_driver.quit()


import shutil

if __name__ == "__main__":
    for temp_file in ['coverage.json', 'geckodriver.log', 'ghostdriver.log']:
        if os.path.exists(temp_file):
            os.remove(temp_file)


if __name__ == "__main__":
    home = os.path.expanduser("~")
    for temp_dir in ['coverage', 'simply-buggy', 'simply-buggy-server', 
                     os.path.join(home, 'simply-buggy-server')]:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


# ## Next Steps

if __name__ == "__main__":
    print('\n## Next Steps')




# ## Background

if __name__ == "__main__":
    print('\n## Background')




# ## Exercises

if __name__ == "__main__":
    print('\n## Exercises')




# ### Exercise 1: Automatic Crash Reporting

if __name__ == "__main__":
    print('\n### Exercise 1: Automatic Crash Reporting')



