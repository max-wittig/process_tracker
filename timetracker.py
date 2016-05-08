import psutil
import json
import time


class JsonWriter:
    def __init__(self):
        self.file = None
        self.filename = "log.json"

    def open_create_file(self):
        self.file = open(self.filename, "w")

    def write_process_list_to_file(self, process_list):
        self.open_create_file()
        if self.file is not None:
            json.dump(process_list, self.file, indent=2)


class TimeTracker:
    def __init__(self):
        self.process_list = []
        self.json_writer = JsonWriter()

    def get_object_position_with_key(self, key):
        counter = 0
        for process in self.process_list:
            if process["name"] in str(key):
                return counter
            counter += 1

    def is_object_already_in_process_list(self, object_to_check):
        is_contained = False
        for thing in self.process_list:
            if str(thing["name"]) in str(object_to_check["name"]):
                print(thing["name"] + "==" + object_to_check["name"])
                is_contained = True
        return is_contained

    def start_logging(self):
        for proc in psutil.process_iter():
            process_object = {"name": proc.name(), "count": 1}
            if self.is_object_already_in_process_list(process_object):
                self.process_list[self.get_object_position_with_key(process_object["name"])]["count"] += 1
            else:
                self.process_list.append(process_object)

    def print_process_list(self):
        print(self.process_list)

    def write_process_list(self):
        self.json_writer.write_process_list_to_file(self.process_list)

if __name__ == '__main__':
    time_tracker = TimeTracker()
    json_writer = JsonWriter()

for i in range(0, 1000):
    time_tracker.start_logging()
    time.sleep(1)
    time_tracker.write_process_list()




