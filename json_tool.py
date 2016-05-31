import json
from process import Process
from task import Task


class JsonReaderWriter:
    def __init__(self, filename="log.json"):
        self.file = None
        self.fileContent = ""
        self.process_list = []
        self.filename = filename

    def open_file(self):
        self.file = open(self.filename, "r")

    def create_file(self):
        self.file = open(self.filename, "w")

    def get_file_content(self):
        self.fileContent = self.file.read()
        return self.fileContent

    def get_json(self):
        return json.loads(self.get_file_content())

    def write_process_list_to_file(self, process_object_list):
        self.create_file()
        if self.file is not None:
            for process in process_object_list:
                """get process_json from object and add it to list, which can be printed"""
                self.process_list.append(process.to_json())
            json.dump(self.process_list, self.file, indent=2)

    def write_settings_to_file(self, settings):
        self.create_file()
        json.dump(settings.to_json(), self.file, indent=2)

    def get_existing_process_list(self):
        if self.fileContent is not None:
            process_object_list = []
            for json_process in json.loads(self.fileContent):
                process = Process(json_process['process_name'])
                json_task_list = json_process['task_list']
                task_list = []
                for json_task in json_task_list:
                    task = Task()
                    task.set_start_time(json_task['start_time'])
                    task.set_json_end_time(json_task['end_time'])
                    task_list.append(task)
                process.set_task_list(task_list)
                process_object_list.append(process)
            return process_object_list
        else:
            return None

