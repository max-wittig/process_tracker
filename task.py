import time


class Task:
    """Task tracks end and start_time and is contained in a task_list of a process"""
    def __init__(self):
        self.start_time = int(time.time())
        self.end_time = None

    def set_end_time(self):
        self.end_time = int(time.time())

    def get_run_time(self):
        return self.end_time-self.start_time

    def to_json(self):
        return {
            "start_time": self.start_time,
            "end_time": self.end_time
        }
