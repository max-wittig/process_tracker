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

    def open_create_file(self):
        self.file = open(self.filename, "w")
        """self.fileContent = self.file.read()"""

    def write_process_list_to_file(self, process_object_list):
        self.open_create_file()
        if self.file is not None:
            for process in process_object_list:
                """get process_json from object and add it to list, which can be printed"""
                self.process_list.append(process.to_json())
            json.dump(self.process_list, self.file, indent=2)

    def get_existing_process_list(self):
        if self.fileContent is not None:
            return self.fileContent
        else:
            return None


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


class Task:
    def __init__(self):
        self.start_time = time.time()
        self.end_time = None

    def set_end_time(self):
        self.end_time = time.time()

    def get_end_time(self):
        return self.end_time

    def get_run_time(self):
        return self.end_time-self.start_time

    def to_json(self):
        return {
            "start_time": self.start_time,
            "end_time": self.end_time
        }


class TimeTracker:
    def __init__(self, processes_to_track):
        self.json_reader_writer = JsonReaderWriter()
        self.running = False
        self.process_object_list = []
        self.processes_to_track = processes_to_track

    def get_object_position_with_key(self, key):
        counter = 0
        for process in self.process_object_list:
            if str(key) is process.get_process_name():
                return counter
            counter += 1

    def is_name_already_in_process_list(self, process_name):
        is_contained = False
        for current_process in self.process_object_list:
            if str(process_name) == str(current_process.get_process_name()):
                is_contained = True
        return is_contained

    def get_process_list_without_doubles(self):
        psutil_process_list = psutil.process_iter()
        return_process_list = []
        for process in psutil_process_list:
            if str(process.name()) not in return_process_list:
                return_process_list.append(process.name())
        return return_process_list

    def get_process_by_name(self, process_name):
        for current_process in self.process_object_list:
            if str(process_name) == str(current_process.get_process_name()):
                return current_process

    def get_process_index_by_name(self, process_name):
        counter = 0
        for current_process in self.process_object_list:
            if str(process_name) == str(current_process.get_process_name()):
                return counter
        print(counter)
        counter += 1

    def add_processes(self):
        """start initial process_list"""
        for process_name in self.get_process_list_without_doubles():
            if self.is_name_already_in_process_list(process_name):
                """process already in list"""
                """end_time is none --> task still running"""
                """end_time is not none -> task was terminated, create new task if running"""
                if self.process_object_list[self.get_process_index_by_name(process_name)].is_running() is False:
                    task = Task()
                    self.process_object_list[self.get_process_index_by_name(process_name)].get_task_list().append(task)
                    print("process: " + process_name + " just restarted")
                    self.get_process_by_name(process_name).set_running(True)
            else:
                """Process is not in process_object_list"""
                current_process = Process(process_name)
                """add process to list with task, which contains all the time_info"""
                task = Task()
                current_process.add_task(task)
                self.process_object_list.append(current_process)
                print("process: " + current_process.get_process_name() + " just started")

    def check_running_processes(self):
        """give process end_time if not running anymore"""
        for list_process in self.process_object_list:
            is_contained = False
            for running_process in self.get_process_list_without_doubles():
                if str(running_process) == str(list_process.get_process_name()):
                    is_contained = True
            if is_contained is False:
                """task no longer running, set endTime"""
                if list_process.get_latest_task().get_end_time() is None:
                    print("process: " + list_process.get_process_name() + " just ended")
                    list_process.set_running(False)
                    list_process.get_latest_task().set_end_time()

    def start_logging(self, delay):
        print("Logging started...")
        self.running = True

        while self.running:
            self.check_running_processes()
            self.add_processes()
            time.sleep(delay)

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
    time_tracker.write_process_list()

if __name__ == '__main__':
    main()
