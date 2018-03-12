# Testcase class to store testcase data and results

import json
import os.path


class Testcase:
    def __init__(self, jsonpath):
        self.jsonpath = jsonpath
        self.execpath = ""
        self.name = ""
        self.expected_files = []
        self.options = []
        self.failed = False
        self.finished = False
        self.fail_reason = ""

        self.load_from_json()

    def load_from_json(self):
        data = {}
        try:
            fp = open(self.jsonpath)
            data = json.load(fp)
        except Exception as e:
            msg = "Could not open json file:\n\t" + self.jsonpath + "\n" + str(e)
            self.failure(msg)
            return
        else:
            fp.close()

        basename = os.path.basename(self.jsonpath)
        self.name = os.path.splitext(basename)[0]

        if "files" in data:
            files = data["files"]
        else:
            msg = "no 'files' attribute in json"
            self.failure(msg)
            return

        if len(files) == 0:
            msg = "empty 'files' attribute in json"
            self.failure(msg)
            return

        if "path" in data:
            path = data["path"]
            path = os.path.expandvars(path)
            path = os.path.expanduser(path)
            path = os.path.abspath(path)
            if not os.path.isdir(path):
                msg = "Specified execution directory does not exist:\n\t" + \
                      path
                self.failure(msg)
                return
            self.execpath = path

        if "options" in data:
            self.options = data["options"]

        self.expected_files = [self.make_file_abs(f) for f in files]

    def make_file_abs(self, f):
        if os.path.isabs(f):
            return f

        basepath = self.execpath
        if basepath != "":
            return os.path.join(basepath, f)

        return os.path.join(os.getcwd(), f)

    def failure(self, reason):
        self.failed = True
        self.finished = True
        self.fail_reason = reason

    def success(self):
        if not self.failed:
            self.finished = True
