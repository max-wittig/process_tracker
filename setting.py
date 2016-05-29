import json


class Setting:
    def __init__(self, filename):
        self.filename = filename
        self.file = None
        self.processes_to_track = []
        self.time_delay = 5
        self.file_content_object = None
        self.read_json()

    def get_processes_to_track(self):
        return self.processes_to_track

    def get_time_delay(self):
        return self.time_delay

    def parse(self):
        self.processes_to_track = self.file_content_object["processes_to_track"]
        self.time_delay = self.file_content_object["time_delay"]

    def read_json(self):
        self.file = open("settings/" + self.filename)
        self.file_content_object = json.loads(self.file.read())
        self.parse()
