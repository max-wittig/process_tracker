import psutil
import json
import time
import threading


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
    def __init__(self, processes_to_track):
        self.process_list = []
        self.json_writer = JsonWriter()
        self.running = False

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
                is_contained = True
        return is_contained

    def start_logging(self, delay):
        print("Logging started...")
        self.running = True

        while self.running:
            for proc in psutil.process_iter():
                if '' in processes_to_track or str(proc.name()).strip(" ") in processes_to_track:
                    process_object = {"name": proc.name(),
                                      "count": 1,
                                      "startTime": time.time(),
                                      "latestRunTime": time.time()}
                    if self.is_object_already_in_process_list(process_object):
                        position = self.get_object_position_with_key(process_object["name"])
                        self.process_list[position]["count"] += 1
                        self.process_list[position]["latestRunTime"] = time.time()
                    else:
                        self.process_list.append(process_object)
            time.sleep(delay)

    def stop_logging(self):
        print("Logging stopped")
        self.running = False

    def print_process_list(self):
        print(self.process_list)

    def write_process_list(self):
        print(json_writer.filename + " written")
        self.json_writer.write_process_list_to_file(self.process_list)

if __name__ == '__main__':
    processes_to_track_string = input("Input all processes to track, separated by space\n")
    processes_to_track = processes_to_track_string.split(' ')
    print(processes_to_track)
    time_tracker = TimeTracker(processes_to_track)
    json_writer = JsonWriter()
    thread = threading.Thread(target=time_tracker.start_logging, args=(1, ))
    thread.setDaemon(True)
    thread.start()
    time.sleep(5)
    input("Press return to stop logging\n")
    time_tracker.stop_logging()
    thread.join()
    time_tracker.write_process_list()




