import psutil
import time
from task import Task
from process import Process
from json_tool import JsonTool


class ProcessTracker:
    def __init__(self, settings):
        """main class of program"""
        self.filename = settings.log_filename
        self.json_reader_writer = JsonTool("logs/" + self.filename)
        self.running = False
        self.process_object_list = []
        self.settings = settings

    def is_name_already_in_process_list(self, process_name):
        """returns boolean value, which checks if process is contained, based on name"""
        is_contained = False
        for current_process in self.process_object_list:
            if str(process_name) == str(current_process.process_name):
                is_contained = True
        return is_contained

    def user_include_filter_processes(self, return_process_list):
        """returns a filtered list, where processes which are not on self.included_processes are filtered out"""
        filtered_list = []
        for process in return_process_list:
            for u_process in self.settings.get_processes_to_track():
                if process == u_process:
                    filtered_list.append(process)
        return filtered_list

    def user_exclude_filter_processes(self, return_process_list):
        """returns a filtered list, where processes from self.excluded_processes are filtered out"""
        filtered_list = return_process_list.copy()
        for process in return_process_list:
            for u_process in self.settings.excluded_processes:
                if process == u_process:
                    filtered_list.remove(process)
        return filtered_list

    def get_process_list_without_doubles(self):
        """gets processes from process_iter and filters out double processes"""
        psutil_process_list = psutil.process_iter()
        return_process_list = []
        for process in psutil_process_list:
            if str(process.name()) not in return_process_list:
                return_process_list.append(process.name())

        """excluded processes are priority"""
        if len(self.settings.excluded_processes) > 0:
            return self.user_exclude_filter_processes(return_process_list)
        elif len(self.settings.processes_to_track) > 0:
            """filters out processes, which the user doesn't want to see"""
            return self.user_include_filter_processes(return_process_list)
        else:
            return return_process_list

    def get_process_by_name(self, process_name):
        """gets process from process_object_list"""
        for current_process in self.process_object_list:
            if str(process_name) == str(current_process.process_name):
                return current_process

    def get_process_index_by_name(self, process_name):
        counter = 0
        for current_process in self.process_object_list:
            if str(process_name) == str(current_process.process_name):
                return counter
        print(counter)
        counter += 1

    def add_processes(self):
        """add current running processes to process_list
            if process already in list, add task to process
        """
        for process_name in self.get_process_list_without_doubles():
            if self.is_name_already_in_process_list(process_name):
                """process already in list"""
                """end_time is none --> task still running"""
                """end_time is not none -> task was terminated, create new task if running"""
                for process in self.process_object_list:
                    if process.running is False:
                        if process.process_name == process_name:
                            task = Task()
                            process.task_list.append(task)
                            print("process: " + process_name + " just restarted")
                            self.get_process_by_name(process_name).running = True
            else:
                """Process is not in process_object_list"""
                current_process = Process(process_name)
                """add process to list with task, which contains all the time_info"""
                task = Task()
                current_process.add_task(task)
                self.process_object_list.append(current_process)
                print("process: " + current_process.process_name + " just started")

    def check_running_processes(self):
        """compares running processes with processes from self.process_list
            if not running sets end_time and running to false"""
        for list_process in self.process_object_list:
            is_contained = False
            for running_process in self.get_process_list_without_doubles():
                if str(running_process) == str(list_process.process_name):
                    is_contained = True
            if is_contained is False:
                """task no longer running, set endTime"""
                if list_process.get_latest_task().end_time is None:
                    print("process: " + list_process.process_name + " just ended")
                    list_process.get_latest_task().set_end_time()
                    list_process.running = False

    def start_logging(self, delay):
        """starts loop that, runs until user hits enter key
        delay is sleep time of the loop"""
        print("Logging started...")
        self.running = True

        while self.running:
            self.check_running_processes()
            self.add_processes()
            time.sleep(delay)

    def add_end_time_to_all_tasks(self):
        """is started, before thread ends and gives task that haven't got an end_time one"""
        for process in self.process_object_list:
            for task in process.task_list:
                if task.end_time is None:
                    task.set_end_time()

    def stop_logging(self):
        """triggered by user action --> enter key"""
        self.add_end_time_to_all_tasks()
        print("Logging stopped")
        self.running = False

    def print_process_list(self):
        """console output of process_list"""
        print(self.process_object_list)

    def write_process_list(self):
        """console output of json_filename
            calls method in json_tool which writes it to file"""
        print(self.json_reader_writer.filename + " written")
        self.json_reader_writer.write_process_list_to_file(self.process_object_list)


