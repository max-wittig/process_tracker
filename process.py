class Process:
    """contains a task_list with task objects."""
    def __init__(self, process_name):
        self.process_name = process_name
        self.task_list = []
        self.running = True

    def add_task(self, task):
        self.task_list.append(task)

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
