# scctests
Test utility for scc, the YAKINDU Statechart Tools Compiler.
It searches the current directory for files named test*.json.
Each json file specifies one test case. test* is the testcase's name.
A testcase contains information about:
 - path (testpath) from where to execute scc [optional]
      The path will be expanded and made absolute, so you can do:
          - use a relative path to the json file's location
          - use '~' for the user's home directory
          - use env variables in the path, like '${name}'
 - which command line options to use [optional]
 - A set of files {F} which are expected to change [mandatory]
      The files can have an absolute path or they will be interpreted
      either relative to the given testpath, or, if not specified,
      to this script's working directory.

This test executor needs to be able to call scc, so make sure it is on
the PATH. The easiest way to achieve this is by creating a symlink
/usr/local/bin/scc to the downloaded scc executable.

Another possibility is to set the environment variable SCCLOC to the 
absolute path to the scc executable.

Given file paths must either be absolute or relative to the testing
directory, which is either specified or the current (testpath) one.

The following cycle will be executed for each testcase:
BEFORE the test:
Check: The given json is parseable and contains at least {F}.
Action: The test utility will cd into the given execution directory, if specified
Action: All specified files {F} will be deleted.

DURING the test:
Check: The current working directory matches the given execution directory.
Check: No files given in {F} exist.
Action: scc will be called from the current working directory with the
  specified command line options.
  The output from scc will be saved in [testcasename].log,
  so the result for test1.json will be found in test1.log.
  This file will be put in the execution directory of this utility.
Check: scc was executed correctly, by checking if [testcasename].log exists
  and contains something.
Check: All files {F} do exist now.

AFTER the test:
Cleanup: This utility will delete all files {F} again.
Cleanup: The utility cd's back to the old working directory.

END:
After executing all tests, this utility will print the test results.
The utility exits with 0 if and only if all tests succeeded, else 1.

Example testcase specification in json format:

```
{
  "path": "~/test/test-workspace/StateMachine/",
  "files":
  [
      "src/StateMachine.c",
      "src/StateMachine.h"
  ],
  "options":
  [
      "-m",
      "src"
  ]
}
```
