from SimpleReportPrinter import SimpleReportPrinter
from xml.etree.ElementTree import Element, ElementTree


class XMLReportExporter(SimpleReportPrinter):
    def __init__(self, xmlFile):
        super().__init__()
        self.xmlFile = xmlFile
        self.root = Element("testsuite")
        self.root.set("name", "SCC tests")
        self.root.set("time", "")
        self.tree = ElementTree(self.root)

    def add_test(self, testcase):
        tc = Element("testcase")
        tc.set("name", testcase.name)
        tc.set("classname", testcase.name)
        tc.set("time", "0.42")
        if testcase.failed:
            failure = Element("failure")
            failure.text = testcase.fail_reason
            tc.append(failure)
        self.root.append(tc)

    def add_tests(self, testcases):
        for test in testcases:
            self.add_test(test)

    def output(self):
        self.tree.write(self.xmlFile)
        return "XML saved to " + str(self.xmlFile)
