import psutil
import json
import time
import threading


class JsonReaderWriter:
    def __init__(self):
        self.file = None
        self.filename = "log.json"
        self.fileContent = ""
        self.process_list = []

    def create_json_object(self, process_object_list):
        for process in process_object_list:
            self.process_list.append(process.process_name)

    def open_create_file(self):
        self.file = open(self.filename, "w")
        """self.fileContent = self.file.read()"""

    def write_process_list_to_file(self, process_object_list):
        self.open_create_file()
        if self.file is not None:
            json.dump(process_object_list, self.file, indent=2)

    def get_existing_process_list(self):
        if self.fileContent is not None:
            return self.fileContent
        else:
            return None


class Process:
    def __init__(self, process_name):
        self.process_name = process_name
        self.task_list = []

    def add_task(self, task):
        self.task_list.append(task)

    def get_task_list(self):
        return self.task_list

    def get_process_name(self):
        return self.process_name


class Task:
    def __init__(self, start_time, end_time):
        self.startTime = start_time
        self.endTime = end_time


class TimeTracker:
    def __init__(self, processes_to_track):
        self.process_list = []
        self.json_reader_writer = JsonReaderWriter()
        self.running = False
        self.process_object_list = []
        self.processes_to_track = processes_to_track

    def get_object_position_with_key(self, key):
        counter = 0
        for proc in self.process_list:
            if proc["name"] in str(key):
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
                process_name = proc.name()
                current_process = Process(process_name)
                if current_process not in self.process_object_list:
                    """add process to list"""
                    self.process_object_list.append(current_process)

        time.sleep(delay)
        print(self.process_object_list)

    def stop_logging(self):
        print("Logging stopped")
        self.running = False

    def print_process_list(self):
        print(self.process_object_list)

    def write_process_list(self):
        print(self.json_reader_writer.filename + " written")
        self.json_reader_writer.write_process_list_to_file(self.process_object_list)


def main():
    processes_to_track_string = input("Input all processes to track, separated by space\n")
    processes_to_track = processes_to_track_string.split(' ')
    print(processes_to_track)
    if processes_to_track[0] is '':
        processes_to_track = None
    time_tracker = TimeTracker(processes_to_track)
    thread = threading.Thread(target=time_tracker.start_logging, args=(1, ))
    """thread dies, if main dies"""
    thread.setDaemon(True)
    thread.start()
    time.sleep(2)
    input("Press return to stop logging\n")
    time_tracker.stop_logging()
    """wait for thread to finish"""
    thread.join()
    #time_tracker.print_process_list()
    time_tracker.write_process_list()

if __name__ == '__main__':
    main()
