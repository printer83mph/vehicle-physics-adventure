from dataclasses import dataclass
import time

import numpy as np
import pyray as rl
from app.ui.graph import Graph


@dataclass
class TelemetryData:
    graph: Graph
    series: Graph.YSeries


def pop_and_push(arr, value):
    arr[:-1] = arr[1:]
    arr[-1] = value


class Telemetry:
    SAMPLES = 200

    def __init__(self, car, SCREEN_WIDTH, SCREEN_HEIGHT):
        GRAPH_WIDTH = 200
        GRAPH_HEIGHT = 200

        self.car = car

        current_time = time.time()
        self.time_series = np.linspace(
            current_time - 1.0, current_time, Telemetry.SAMPLES
        )

        # Speed creation
        speed_graph: Graph = Graph(
            position=(
                SCREEN_WIDTH - GRAPH_WIDTH,
                0,
            ),  # position of top left corner
            size=(200, 200),
            y_min=-100.0,  # min y value shown
            y_max=500.0,  # max y value shown
            line_spacing=(1.0, 100.0),  # space between each background line
            line_offset=(0.0, 0.0),  # base offset for background lines
        )

        # init y series
        speed_series = Graph.YSeries(
            color=rl.RED,
            thickness=2,
            values=np.zeros(Telemetry.SAMPLES, np.float64),
        )

        speed_graph.x_series = self.time_series
        speed_graph.add_series(speed_series)
        self.speed = TelemetryData(graph=speed_graph, series=speed_series)

        # Angular velocity creation
        angular_velocity_graph: Graph = Graph(
            position=(
                SCREEN_WIDTH - GRAPH_WIDTH,
                GRAPH_HEIGHT,
            ),  # position of top left corner
            size=(200, 200),
            y_min=-5.0,  # min y value shown
            y_max=5.0,  # max y value shown
            line_spacing=(1.0, 1.0),  # space between each background line
            line_offset=(0.0, 0.0),  # base offset for background lines
        )

        angular_series = Graph.YSeries(
            color=rl.BLUE,
            thickness=2,
            values=np.zeros(Telemetry.SAMPLES, np.float64),
        )

        angular_velocity_graph.x_series = self.time_series
        angular_velocity_graph.add_series(angular_series)
        self.angular_velocity = TelemetryData(
            graph=angular_velocity_graph, series=angular_series
        )

        # Acceleration creation
        acceleration_graph: Graph = Graph(
            position=(
                SCREEN_WIDTH - GRAPH_WIDTH,
                2 * GRAPH_HEIGHT,
            ),  # position of top left corner
            size=(200, 200),
            y_min=-400.0,  # min y value shown
            y_max=1600.0,  # max y value shown
            line_spacing=(1.0, 100.0),  # space between each background line
            line_offset=(0.0, 0.0),  # base offset for background lines
        )

        acceleration_series = Graph.YSeries(
            color=rl.GREEN,
            thickness=2,
            values=np.zeros(Telemetry.SAMPLES, np.float64),
        )

        acceleration_graph.x_series = self.time_series
        acceleration_graph.add_series(acceleration_series)
        self.acceleration = TelemetryData(
            graph=acceleration_graph, series=acceleration_series
        )

    def tick(self):
        current_time = time.time()
        car_velocity = self.car.velocity

        # Time logging
        pop_and_push(self.time_series, current_time)

        # Speed logging
        speed = np.linalg.norm(car_velocity)
        pop_and_push(self.speed.series.values, speed)

        # Angular velocity logging
        pop_and_push(self.angular_velocity.series.values, self.car.angular_velocity)

        # Acceleration logging
        pop_and_push(self.acceleration.series.values, self.car.tracked_acceleration)

    def draw(self):
        self.speed.graph.draw()
        self.angular_velocity.graph.draw()
        self.acceleration.graph.draw()
