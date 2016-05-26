import svgwrite


class Gantt:
    def __init__(self):
        self.filename = "gantt.svg"
        self.height = "10cm"
        self.width = "10cm"
        self.chart = svgwrite.Drawing(self.height, self.width, debug=True)

    def get_chart_height(self):
        return self.height

    def setup_y_line(self, maximum):
        """something"""

    def setup_x_line(self, maximum):
        self.chart.add(self.chart.line((0, 0), (10, 0), stroke=svgwrite.rgb(10, 10, 16, '%')))
        self.chart.add(self.chart.text('Test', insert=(0, 15)))

    def setup_grid(self, grid_range):
        """draw grid from range"""
        self.setup_x_line(grid_range.stop)
        self.setup_y_line(grid_range.stop)

    def save_gantt(self):
        self.chart.saveas(self.filename)

if __name__ == "__main__":
    gantt = Gantt()
    gantt.setup_grid(range(0, 1000))
    gantt.save_gantt()
