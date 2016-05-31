#!/usr/bin/python3
import getopt
import sys
import psutil
import threading
import time
from task import Task
from process import Process
from json_tool import JsonReaderWriter
from setting import Setting


class TimeTracker:
    def __init__(self, settings):
        self.filename = settings.get_log_filename()
        self.json_reader_writer = JsonReaderWriter(self.filename)
        self.running = False
        self.process_object_list = []
        self.processes_to_track = settings.get_processes_to_track()
        self.excluded_processes = settings.get_excluded_processes()

    def is_name_already_in_process_list(self, process_name):
        is_contained = False
        for current_process in self.process_object_list:
            if str(process_name) == str(current_process.get_process_name()):
                is_contained = True
        return is_contained

    def user_include_filter_processes(self, return_process_list):
        filtered_list = []
        for process in return_process_list:
            for u_process in self.processes_to_track:
                if process == u_process:
                    filtered_list.append(process)
        return filtered_list

    def user_exclude_filter_processes(self, return_process_list):
        filtered_list = return_process_list
        for process in return_process_list:
            for u_process in self.excluded_processes:
                if process == u_process:
                    filtered_list.remove(process)
        return filtered_list

    """gets processes from process_iter and kills double processes"""
    def get_process_list_without_doubles(self):
        psutil_process_list = psutil.process_iter()
        return_process_list = []
        for process in psutil_process_list:
            if str(process.name()) not in return_process_list:
                return_process_list.append(process.name())

        """excluded processes are priority"""
        if len(self.excluded_processes) > 0:
            return self.user_exclude_filter_processes(return_process_list)
        elif len(self.processes_to_track) > 0:
            """filters out processes, which the user doesn't want to see"""
            return self.user_include_filter_processes(return_process_list)
        else:
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
                for process in self.process_object_list:
                    if process.is_running() is False:
                        if process.get_process_name() == process_name:
                            task = Task()
                            process.get_task_list().append(task)
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
                    list_process.get_latest_task().set_end_time()
                    list_process.set_running(False)

    def start_logging(self, delay):
        print("Logging started...")
        self.running = True

        while self.running:
            self.check_running_processes()
            self.add_processes()
            time.sleep(delay)

    def add_end_time_to_all_tasks(self):
        for process in self.process_object_list:
            for task in process.get_task_list():
                if task.get_end_time() is None:
                    task.set_end_time()

    def stop_logging(self):
        self.add_end_time_to_all_tasks()
        print("Logging stopped")
        self.running = False

    def print_process_list(self):
        print(self.process_object_list)

    def write_process_list(self):
        print(self.json_reader_writer.filename + " written")
        self.json_reader_writer.write_process_list_to_file(self.process_object_list)


def show_help():
    print("\n")
    print("--------USAGE--------")
    print("-h --help                                          : prints this help page")
    print("-l <arg> --load <arg>                              : load settings file from <arg>")
    print("-o <arg> --output <arg>                            : specify output filename")
    print("-i arg1 arg2 arg3 ... --include arg1 arg2 arg3 ... : set processes that should be tracked")
    print("-e arg1 arg2 arg3 ... --exclude arg1 arg2 arg3 ... : set processes that shouldn't be tracked")
    print("---------------------")
    print("\n")
    sys.exit(0)



def main():
    settings = Setting()
    filename = "log.json"
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hl:o:i:e:", ["help", "load=", "output=", "included="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            show_help()
        elif o in ("-l", "--load"):
            try:
                settings.load_from_file(a)
                print(a)
            except:
                print("settings file not found")
                exit(1)
        elif o in ("-o", "--output"):
            settings.set_log_filename(a)
        elif o in ("-i", "--included"):
            processes_to_track = a.split(' ')
            settings.set_processes_to_track(processes_to_track)
        elif o in ("-e", "--excluded"):
            excluded_processes = a.split(' ')
            settings.set_excluded_processes(excluded_processes)
        else:
            assert False, "unhandled option"

    print("time_delay=" + str(settings.get_time_delay()))
    time_tracker = TimeTracker(settings)
    thread = threading.Thread(target=time_tracker.start_logging, args=(settings.get_time_delay(), ))
    """thread dies, if main dies"""
    thread.setDaemon(True)
    thread.start()
    time.sleep(2)
    print("------------------------------")
    input("Press return to stop logging\n------------------------------\n")
    time_tracker.stop_logging()
    """wait for thread to finish"""
    thread.join()
    time_tracker.write_process_list()

if __name__ == '__main__':
    main()
