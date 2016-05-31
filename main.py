#!/usr/bin/python3
from setting import Setting
from process_tracker import ProcessTracker
from settings_builder import SettingsBuilder
import threading
import sys
import getopt
import time


def show_help():
    print("\n")
    print("--------USAGE--------")
    print("-h --help                                              : prints this help page")
    print("-l <arg> --load <arg>                                  : load settings file from <arg>")
    print("-o <arg> --output <arg>                                : specify output filename")
    print("-i 'arg1 arg2 arg3' ... --include 'arg1 arg2 arg3' ... : set processes that should be tracked")
    print("-e 'arg1 arg2 arg3' ... --exclude 'arg1 arg2 arg3' ... : set processes that shouldn't be tracked")
    print("---------------------")
    print("\n")
    sys.exit(0)


def main():
    settings = Setting()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hl:o:i:e:b:",
                                   ["help", "load=", "output=", "included=", "excluded=", "build="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            show_help()
        elif o in ("-l", "--load"):
            try:
                settings.load_from_file("settings/" + a)
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
        elif o in ("-b", "--build"):
            settings_builder = SettingsBuilder()
            settings_builder.build_exclude_settings()
            settings_builder.save_settings("settings/" + a)
            print("settings saved in " + a)
            sys.exit(0)

        else:
            assert False, "unhandled option"

    print("time_delay=" + str(settings.get_time_delay()))
    process_tracker = ProcessTracker(settings)
    thread = threading.Thread(target=process_tracker.start_logging, args=(settings.get_time_delay(), ))
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
    main()
