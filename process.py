class Process:
    def __init__(self, process_name):
        self.process_name = process_name
        self.task_list = []
        self.running = True

    def set_running(self, running):
        self.running = running

    def is_running(self):
        return self.running

    def add_task(self, task):
        self.task_list.append(task)

    def get_task_list(self):
        return self.task_list

    def set_task_list(self, task_list):
        self.task_list = task_list

    def get_process_name(self):
        return self.process_name

    def to_json(self):
        json_task_list = []
        for task in self.task_list:
            json_task_list.append(task.to_json())
        process = {
            "process_name": self.process_name,
            "task_list": json_task_list
        }
        return process

    def get_latest_task(self):
        return self.task_list[-1]
