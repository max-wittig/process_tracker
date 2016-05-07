import psutil


class TimeTracker:
    def __init__(self):
        self.open_create_file()
        self.start_logging()

    def open_create_file(self):
        file = open("log.txt")

    def start_logging(self):
        for proc in psutil.process_iter():
            print(proc.name())


if __name__ == '__main__':
    time_tracker = TimeTracker()




