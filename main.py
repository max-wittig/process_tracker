#!/usr/bin/python3

from setting import Setting
from process_tracker import ProcessTracker
from settings_builder import SettingsBuilder
import argparse
import threading
import sys
import time
import json

def get_args():
    parser.add_argument("-l", "--load", help="Load settings file")
    parser.add_argument("-o", "--output", help="Specify output filename")
    parser.add_argument("-i", "--included", help="Set processes that should be tracked", nargs="+")
    parser.add_argument("-e", "--excluded", help="Set processes that shouldn't be tracked", nargs="+")
    parser.add_argument("-b", "--build", help="Build settings file, based on current running processes --> excluded_processes")
    parser.add_argument("-m", "--manual", help="Manual input", action="store_true")
    options = parser.parse_args()
    return vars(options)


def get_settings_from_user():
    settings = Setting()
    settings.processes_to_track = input("processes to track: ")
    if settings.processes_to_track:
        settings.processes_to_track = settings.processes_to_track.split(" ")
    settings.excluded_processes = input("excluded processes: ")
    if settings.excluded_processes:
        settings.excluded_processes = settings.excluded_processes.split(" ")
    time_delay = input("time delay: ")
    if not time_delay:
        time_delay = 2
    save_location = input("log filename: ")
    settings.time_delay = int(time_delay)
    settings.log_filename = save_location
    return settings


def main():
    settings = Setting()
    args = get_args()
    if args["manual"]:
        settings = get_settings_from_user()
    else:
        if args["load"]:
            try:
                settings.load_from_file("settings/" + args["load"])
                print("Settings loaded from {0}".format(args["load"]))
            except:
                exit("Settings file {0} not found".format(args["load"]))
        if args["output"]:
            settings.log_filename = args["output"]
        if args["included"]:
            settings.processes_to_track = args["included"]
            print(settings.processes_to_track)
        if args["excluded"]:
            settings.excluded_processes = args["excluded"]
        if args["build"]:
            settings_builder = SettingsBuilder()
            settings_builder.build_exclude_settings()
            settings_builder.save_settings("settings/" + args["build"])
            print("Settings saved in " + args["build"])
            exit(0)

        print("time_delay=" + str(settings.time_delay))
    if settings is None:
        parser.print_help()
        exit("Settings is None")
    process_tracker = ProcessTracker(settings)
    thread = threading.Thread(target=process_tracker.start_logging, args=(settings.time_delay, ))
    """thread dies, if main dies"""
    thread.setDaemon(True)
    thread.start()
    time.sleep(2)
    print("------------------------------")
    input("Press return to stop logging\n------------------------------\n")
    process_tracker.stop_logging()
    """wait for thread to finish"""
    thread.join()
    process_tracker.write_process_list()


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Process Tracker")
    main()
