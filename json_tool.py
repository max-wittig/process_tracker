import json
from process import Process
from task import Task


class JsonTool:
    """manages different json outputs"""
    def __init__(self, filename="log.json"):
        self.file = None
        self.process_list = []
        self.filename = filename

    def get_file_content(self):
        with open(self.filename) as f:
            return f

    def get_json(self):
            return json.load(self.get_file_content())

    def write_process_list_to_file(self, process_object_list):
        with open(self.filename, "w") as f:
            for process in process_object_list:
                """get process_json from object and add it to list, which can be printed"""
                self.process_list.append(process.to_json())
            json.dump(self.process_list, f, indent=2)

    def write_settings_to_file(self, settings):
        with open(self.filename, "w") as f:
            json.dump(settings.to_json(), f, indent=2)

    def get_existing_process_list(self):
        if self.get_file_content() is not None:
            process_object_list = []
            for json_process in json.loads(self.get_file_content()):
                process = Process(json_process['process_name'])
                json_task_list = json_process['task_list']
                task_list = []
                for json_task in json_task_list:
                    task = Task()
                    task.start_time = json_task['start_time']
                    task.end_time = json_task['end_time']
                    task_list.append(task)
                process.task_list = task_list
                process_object_list.append(process)
            return process_object_list
        else:
            return None

