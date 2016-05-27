import time


class Task:
    def __init__(self):
        self.start_time = int(time.time())
        self.end_time = None

    def set_start_time(self, start_time):
        self.start_time = start_time

    def get_start_time(self):
        return self.start_time

    def set_end_time(self):
        self.end_time = int(time.time())

    def set_json_end_time(self, end_time):
        self.end_time = end_time

    def get_end_time(self):
        return self.end_time

    def get_run_time(self):
        return self.end_time-self.start_time

    def to_json(self):
        return {
            "start_time": self.start_time,
            "end_time": self.end_time
        }
