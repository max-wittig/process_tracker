from json_tool import JsonTool


class Setting:
    """certain values, which can be read out of a file, which change how the program behaves are in this
    class"""
    def __init__(self):
        self.filename = None
        self.file = None
        self.processes_to_track = []
        self.time_delay = 2
        self.file_content_object = None
        self.excluded_processes = []
        self.log_filename = "log.json"

    def load_from_file(self, filename):
        self.filename = filename
        self.read_json()

    def to_json(self):
        settings = {
            "processes_to_track": self.processes_to_track,
            "time_delay": self.time_delay,
            "excluded_processes": self.excluded_processes,
            "log_filename": self.log_filename
        }
        return settings

    def parse(self):
        self.processes_to_track = self.file_content_object["processes_to_track"]
        self.time_delay = self.file_content_object["time_delay"]
        self.excluded_processes = self.file_content_object["excluded_processes"]
        self.log_filename = self.file_content_object["log_filename"]

    def read_json(self):
        json_reader = JsonTool(filename=self.filename)
        self.file_content_object = json_reader.get_json()
        self.parse()
