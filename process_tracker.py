#!/usr/bin/python3

import psutil
import threading
import time
from task import Task
from process import Process
from json_tool import JsonReaderWriter
from setting import Setting


class TimeTracker:
    def __init__(self, processes_to_track):
        self.json_reader_writer = JsonReaderWriter()
        self.running = False
        self.process_object_list = []
        self.processes_to_track = processes_to_track

    def is_name_already_in_process_list(self, process_name):
        is_contained = False
        for current_process in self.process_object_list:
            if str(process_name) == str(current_process.get_process_name()):
                is_contained = True
        return is_contained

    def user_filter_processes(self, return_process_list):
        filtered_list = []
        for process in return_process_list:
            for u_process in self.processes_to_track:
                if process == u_process:
                    filtered_list.append(process)
        return filtered_list

    """gets processes from process_iter and kills double processes"""
    def get_process_list_without_doubles(self):
        psutil_process_list = psutil.process_iter()
        return_process_list = []
        for process in psutil_process_list:
            if str(process.name()) not in return_process_list:
                return_process_list.append(process.name())

        if self.processes_to_track is not None:
            """filters out processes, which the user doesn't want to see"""
            return self.user_filter_processes(return_process_list)
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


def main():
    processes_to_track_string = input("Input all processes to track, separated by space\n")
    processes_to_track = processes_to_track_string.split(' ')
    time_delay = 5
    if "settings_load" == processes_to_track[0]:
        """opens settings file with array and programs to track in it"""
        try:
            settings = Setting(processes_to_track[1])
            processes_to_track = settings.get_processes_to_track()
            time_delay = settings.get_time_delay()
        except:
            print("Invalid settings json")
            main()

    if processes_to_track[0] == '':
        processes_to_track = None

    print(processes_to_track)
    print("time_delay=" + str(time_delay))
    time_tracker = TimeTracker(processes_to_track)
    thread = threading.Thread(target=time_tracker.start_logging, args=(time_delay, ))
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
