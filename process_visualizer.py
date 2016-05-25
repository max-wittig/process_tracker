import pygal
import sys
from json_tool import JsonReaderWriter


class ProcessVisualizer:
    def __init__(self, process_object_list):
        self.line_chart = pygal.Line()
        self.process_object_list = process_object_list
        self.filename = "chart.svg"

    def get_max_range(self):
        max_start_time = 0
        for process in self.process_object_list:
            task_list = process.get_task_list()
            for task in task_list:
                start_time = task.get_start_time()
                if start_time > max_start_time:
                    max_start_time = start_time
        return max_start_time

    def get_min_range(self):
        min_start_time = sys.float_info.max
        for process in self.process_object_list:
            task_list = process.get_task_list()
            for task in task_list:
                start_time = task.get_start_time()
                if start_time < min_start_time:
                    min_start_time = start_time
        return min_start_time

    def get_range(self):
        min_range = self.get_min_range()
        max_range = self.get_max_range()
        return range(int(min_range), int(max_range))

    def setup_line_chart(self):
        self.line_chart.title = "Process Runtime"
        self.line_chart.x_labels = map(str, self.get_range())

    def insert_data_from_process_list(self):
        for process in self.process_object_list:
            tasks = process.get_task_list()
            for task in tasks:
                self.line_chart.add(process.get_process_name(), [])

    def save_svg_to_file(self):
        self.line_chart.render_to_file(self.filename)

    def visualize_data(self):
        self.setup_line_chart()
        self.insert_data_from_process_list()
        self.save_svg_to_file()


def main():
    json_reader = JsonReaderWriter()
    json_reader.open_file()
    process_object_list = json_reader.get_existing_process_list()
    print(process_object_list[1].get_task_list())
    process_visualizer = ProcessVisualizer(process_object_list)
    process_visualizer.visualize_data()


if __name__ == '__main__':
    main()
