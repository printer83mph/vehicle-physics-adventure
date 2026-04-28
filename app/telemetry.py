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
    # For now, we'll just separate stuff into data like this
    velocity: TelemetryData

    car: NaiveVehicle

    MAX_SERIES_LENGTH = 100

    def __init__(self, car, SCREEN_WIDTH, SCREEN_HEIGHT):
        GRAPH_WIDTH = 200
        GRAPH_HEIGHT = 200

        self.car = car

        velocity_graph: Graph = Graph(
            position=(
                SCREEN_WIDTH - GRAPH_WIDTH,
                0,
            ),  # position of top left corner
            size=(200, 200),
            y_min=-2.0,  # min y value shown
            y_max=2.0,  # max y value shown
            line_spacing=(1.0, 1.0),  # space between each background line
            line_offset=(0.0, 0.0),  # base offset for background lines
        )

        # init y series
        velocity_series = Graph.YSeries(
            color=rl.RED,
            thickness=2,
            values=np.zeros(self.MAX_SERIES_LENGTH, np.float64),
        )

        velocity_graph.x_series = np.zeros(self.MAX_SERIES_LENGTH, np.float64)

        velocity_graph.add_series(velocity_series)
        self.velocity = TelemetryData(graph=velocity_graph, series=velocity_series)

    def update_graph(self, scene: Scene):
        current_time = time.time()

        car_velocity = self.car.velocity
        car_speed = np.linalg.norm(car_velocity[0], car_velocity[1])

        self.velocity.graph.x_series[:-1] = self.velocity.graph.x_series[1:]
        self.velocity.graph.x_series[-1] = current_time

        self.velocity.series.values[:-1] = self.velocity.series.values[1:]
        self.velocity.series.values[-1] = car_speed

        return True

    def draw(self, scene):

        self.update_graph(scene)
        self.velocity.graph.draw()

        return
