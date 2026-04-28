from dataclasses import dataclass
import time

import numpy as np
import pyray as rl
from app.entities.naivevehicle import NaiveVehicle
from app.scene import Scene
from app.ui.graph import Graph


@dataclass
class TelemetryData:
    graph: Graph
    series: Graph.YSeries


class Telemetry:
    SAMPLES = 100

    def __init__(self, car, SCREEN_WIDTH, SCREEN_HEIGHT):
        GRAPH_WIDTH = 200
        GRAPH_HEIGHT = 200

        self.car = car

        speed_graph: Graph = Graph(
            position=(
                SCREEN_WIDTH - GRAPH_WIDTH,
                0,
            ),  # position of top left corner
            size=(200, 200),
            y_min=0.0,  # min y value shown
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

        current_time = time.time()
        speed_graph.x_series = np.linspace(
            current_time - 1.0, current_time, Telemetry.SAMPLES
        )

        speed_graph.add_series(speed_series)
        self.speed = TelemetryData(graph=speed_graph, series=speed_series)

    def update_graph(self, scene: Scene):
        current_time = time.time()

        car_velocity = self.car.velocity
        car_speed = np.linalg.norm(car_velocity)

        self.speed.graph.x_series[:-1] = self.speed.graph.x_series[1:]
        self.speed.graph.x_series[-1] = current_time

        self.speed.series.values[:-1] = self.speed.series.values[1:]
        self.speed.series.values[-1] = car_speed

    def draw(self, scene):

        self.update_graph(scene)
        self.speed.graph.draw()

        return
