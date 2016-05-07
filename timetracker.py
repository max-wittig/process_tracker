import psutil
import json
import time


class JsonWriter:
    def __init__(self):
        self.file = None
        self.filename = "log.json"

    def open_create_file(self):
        self.file = open(self.filename, "a")

    def write_process_list_to_file(self, process_list):
        self.open_create_file()
        if self.file is not None:
            json.dump(process_list, self.file, indent=2)


class TimeTracker:
    def __init__(self):
        self.process_list = []
        self.json_writer = JsonWriter()

    def start_logging(self):
        for proc in psutil.process_iter():
            process_object = {"name": proc.name(), "cpuTime": proc.cpu_percent()}
            self.process_list.append(process_object)

    def print_process_list(self):
        print(self.process_list)

    def write_process_list(self):
        self.json_writer.write_process_list_to_file(self.process_list)

if __name__ == '__main__':
    time_tracker = TimeTracker()
    json_writer = JsonWriter()

    for i in range(0, 10):
        time_tracker.start_logging()
        time.sleep(1)
    time_tracker.write_process_list()




