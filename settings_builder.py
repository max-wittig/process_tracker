from setting import Setting
from process_tracker import ProcessTracker
from json_tool import JsonTool
import time


class SettingsBuilder:
    """builds excluded_processes list, if user issued -b argument"""
    def __init__(self):
        self.settings = Setting()
        self.process_tracker = ProcessTracker(self.settings)

    def print_user_output(self):
        print("---------------------------------------------------")
        input("Close all programs you want to track and hit enter!\n")

    def set_all_current_processes_to_be_excluded(self, build_time=2):
        """changes settings object to contain all running processes in exluded_processes
        build_time is how often / how long the building should take
        --> longer time --> more processes are in settings file
        """
        to_be_excluded = []
        for i in range(0, build_time):
            for process in self.process_tracker.get_process_list_without_doubles():
                if process not in to_be_excluded:
                    to_be_excluded.append(process)
            time.sleep(1)
        to_be_excluded = self.process_tracker.get_process_list_without_doubles()
        self.settings.excluded_processes = to_be_excluded

    def build_exclude_settings(self, build_time=10):
        self.print_user_output()
        self.set_all_current_processes_to_be_excluded(build_time=build_time)

    def save_settings(self, filename):
        """writes settings to filename with excluded processes and default values"""
        json_writer = JsonTool(filename=filename)
        json_writer.write_settings_to_file(self.settings)
