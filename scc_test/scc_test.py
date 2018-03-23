# Test utility for scc, the YAKINDU Statechart Tools Compiler.
# It searches the current directory for files named test*.json.
# Each json file specifies one test case. test* is the testcase's name.
# A testcase contains information about:
# - path (testpath) from where to execute scc [optional]
#       The path will be expanded and made absolute, so you can do:
#           - use a relative path to the json file's location
#           - use '~' for the user's home directory
#           - use env variables in the path, like '${name}'
# - which command line options to use [optional]
# - A set of files {F} which are expected to change [mandatory]
#       The files can have an absolute path or they will be interpreted
#       either relative to the given testpath, or, if not specified,
#       to this script's working directory.
#
# This test executor needs to be able to call scc, so make sure it is on
# the PATH. The easiest way to achieve this is by creating a symlink
# /usr/local/bin/scc to the downloaded scc executable.
#
# Given file paths must either be absolute or relative to the testing
# directory, which is either specified or the current (testpath) one.
#
# The following cycle will be executed for each testcase:
# BEFORE the test:
# Check: The given json is parseable and contains at least {F}.
# Action: The test utility will cd into the given execution directory, if specified
# Action: All specified files {F} will be deleted.
#
# DURING the test:
# Check: The current working directory matches the given execution directory.
# Check: No files given in {F} exist.
# Action: scc will be called from the current working directory with the
#   specified command line options.
#   The output from scc will be saved in [testcasename].log,
#   so the result for test1.json will be found in test1.log.
#   This file will be put in the execution directory of this utility.
# Check: scc was executed correctly, by checking if [testcasename].log exists
#   and contains something.
# Check: All files {F} do exist now.
#
# AFTER the test:
# Cleanup: This utility will delete all files {F} again.
# Cleanup: The utility cd's back to the old working directory.
#
# END:
# After executing all tests, this utility will print the test results.
# The utility exits with 0 if and only if all tests succeeded, else 1.
#
# Example testcase specification in json format:
#
# {
#   "path": "~/test/test-workspace/StateMachine/",
#   "files":
#   [
#       "src/StateMachine.c",
#       "src/StateMachine.h"
#   ],
#   "options":
#   [
#       "-m",
#       "src"
#   ]
# }

from Testcase import Testcase
from SimpleReportPrinter import SimpleReportPrinter
from XMLReportExporter import XMLReportExporter

import sys
import os
import os.path
import subprocess


def wrap_list(o):
    return o if isinstance(o, list) else [o]


def cd(directory):
    os.chdir(directory)


def pwd():
    return os.getcwd()


def delete_files(files):
    files = wrap_list(files)
    for f in files:
        if os.path.isfile(f):
            try:
                os.remove(f)
            except OSError:
                pass


def files_exist(files):
    files = wrap_list(files)
    missing = []
    for f in files:
        if not os.path.isfile(f):
            missing.append(f)
    return None if len(missing) == 0 else missing


def files_do_not_exist(files):
    files = wrap_list(files)
    exist = []
    for f in files:
        if os.path.isfile(f):
            exist.append(f)
    return None if len(exist) == 0 else exist


def call_scc(logfile, options):
    scc = "scc"
    if "SCCLOC" in os.environ:
        scc = os.environ.get("SCCLOC")
    call = wrap_list(options)
    call.insert(0, scc)
    subprocess.call(call, stdout=logfile, stderr=subprocess.STDOUT)


def check_log_not_empty(logfile):
    return logfile.tell() != 0


def find_tests():
    testfiles = []
    files = os.listdir(".")

    for f in files:
        basename = os.path.basename(f)
        ext = os.path.splitext(basename)[1]
        if ext == ".json" and basename.startswith("test"):
            testfiles.append(f)

    return testfiles


def load_tests(json_files):
    return [Testcase(os.path.abspath(f)) for f in json_files]


def before_test(testcase):
    if testcase.failed:
        return

    if not testcase.execpath == "":
        cd(testcase.execpath)

    delete_files(testcase.expected_files)


def test_action(testcase, logfile):
    if testcase.failed:
        return
    if testcase.execpath != "" and testcase.execpath != pwd():
        msg = "Failed to set the working directory:\n\t" + testcase.execpath
        testcase.failure(msg)
        return

    checks = files_do_not_exist(testcase.expected_files)
    if checks is not None:
        msg = "Failed to delete expected files:\n"
        for f in checks:
            msg += "\t" + f + "\n"
        testcase.failure(msg)
        return

    try:
        call_scc(logfile, testcase.options)
    except Exception as e:
        testcase.failure("An error occured when scc was called:\n\t" + str(e))
        return

    if not check_log_not_empty(logfile):
        msg = "The logfile is empty, it seems scc was not executed:\n\t" + \
              os.path.realpath(logfile.name)
        testcase.failure(msg)
        return

    checks = files_exist(testcase.expected_files)
    if checks is not None:
        msg = "Expected file does not exist:\n"
        for f in checks:
            msg += "\t" + f + "\n"
        testcase.failure(msg)
        return


def after_test(testcase, start_dir):
    delete_files(testcase.expected_files)
    cd(start_dir)
    testcase.success()


def run():
    start_dir = pwd()

    json_files = find_tests()
    tests = load_tests(json_files)

    failed = 0

    for testcase in tests:
        logfile_name = os.path.join(start_dir, testcase.name + ".log")
        logfile = open(logfile_name, 'w')

        before_test(testcase)
        test_action(testcase, logfile)
        after_test(testcase, start_dir)
        logfile.close()

        logfile = open(logfile_name, "r")
        for line in logfile:
            print(line,end='')

        logfile.seek(0)

        if testcase.failed:
            failed += 1

    consolePrinter = SimpleReportPrinter()
    xmlPrinter = XMLReportExporter("results.xml")
    consolePrinter.add_tests(tests)
    xmlPrinter.add_tests(tests)

    print(consolePrinter.output())
    print(xmlPrinter.output())

    return failed


if __name__ == "__main__":
    sys.exit(run())
 
