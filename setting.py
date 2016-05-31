import json


class Setting:
    def __init__(self):
        self.filename = None
        self.file = None
        self.processes_to_track = []
        self.time_delay = 5
        self.file_content_object = None
        self.excluded_processes = []

    def load_from_file(self, filename):
        self.filename = filename
        self.read_json()

    def get_processes_to_track(self):
        return self.processes_to_track

    def get_time_delay(self):
        return self.time_delay

    def get_excluded_processes(self):
        return self.excluded_processes

    def parse(self):
        self.processes_to_track = self.file_content_object["processes_to_track"]
        self.time_delay = self.file_content_object["time_delay"]
        self.excluded_processes = self.file_content_object["excluded_processes"]

    def read_json(self):
        self.file = open("settings/" + self.filename)
        self.file_content_object = json.loads(self.file.read())
        self.parse()
