import json


class JsonReaderWriter:
    def __init__(self):
        self.file = None
        self.filename = "log.json"
        self.fileContent = ""
        self.process_list = []

    def open_file(self):
        self.fileContent = self.file.read()

    def create_file(self):
        self.file = open(self.filename, "w")

    def write_process_list_to_file(self, process_object_list):
        self.create_file()
        if self.file is not None:
            for process in process_object_list:
                """get process_json from object and add it to list, which can be printed"""
                self.process_list.append(process.to_json())
            json.dump(self.process_list, self.file, indent=2)

    def get_existing_process_list(self):
        if self.fileContent is not None:
            return json.load(self.fileContent)
        else:
            return None

