import psutil


class TimeTracker:
    def __init__(self):
        self.open_create_file()
        self.start_logging()
        self.file = None

    def open_create_file(self):
        self.file = open("log.txt", "a")

    def start_logging(self):
        for proc in psutil.process_iter():
            self.file.write(proc.name())


if __name__ == '__main__':
    time_tracker = TimeTracker()




