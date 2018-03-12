# Prints the test result to the console.


class SimpleReportPrinter:
    def __init__(self):
        self.tests = []
        self.result = ""

    def add_test(self, testcase):
        self.tests.append(testcase)

    def add_tests(self, testcases):
        self.tests += testcases

    def output(self):
        failed = 0
        self.print("---- TEST RESULTS ----\n")
        for testcase in self.tests:
            self.print_test_result(testcase)
            if testcase.failed:
                failed += 1

        if failed > 0:
            self.print("{}/{} tests failed.".format(failed, len(self.tests)))

        else:
            if len(self.tests) > 0:
                self.print("All {} tests succeeded.".format(len(self.tests)))
            else:
                self.print("No tests found.")

        return self.result

    def print_test_result(self, testcase):
        if not testcase.failed:
            self.print("[ OK ] " + testcase.name)
        else:
            self.print("[FAIL] " + testcase.name + "\n" + testcase.fail_reason + "\n")

    def print(self, s):
        self.result += s + "\n"
