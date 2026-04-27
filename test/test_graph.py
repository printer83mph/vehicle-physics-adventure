import time

import numpy as np
import pyray as rl
from raylib.colors import RAYWHITE

from app.ui.graph import Graph


def main():

    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 400

    rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "awesome vehicle simulator")
    rl.set_target_fps(rl.get_monitor_refresh_rate(rl.get_current_monitor()))

    graph = Graph(
        position=(50, 50),  # position of top left corner
        size=(300, 300),
        y_scale=3.0,  # span of y values
        y_offset=-1.5,  # minimum y value shown
        line_spacing=(1.0, 1.0),  # space between each background line
        line_offset=(0.0, 0.0),  # base offset for background lines
    )

    # init y series
    y_series_sin = Graph.YSeries(
        color=rl.RED,
        thickness=2,
        values=np.zeros(1, np.float64),
    )
    y_series_cos = Graph.YSeries(
        color=rl.GREEN,
        thickness=2,
        values=np.zeros(1, np.float64),
    )
    graph.add_series(y_series_sin)
    graph.add_series(y_series_cos)

    def update_graph():
        time_offset = time.time()
        graph.x_series = np.linspace(
            time_offset, time_offset + 6.0, 100, dtype=np.float64
        )
        y_series_sin.values = np.sin(graph.x_series * np.pi * 0.5)
        y_series_cos.values = np.cos(graph.x_series * np.pi * 0.5)

    while not rl.window_should_close():
        update_graph()

        rl.begin_drawing()
        rl.clear_background(RAYWHITE)

        # test draw graph
        graph.draw()

        rl.end_drawing()


if __name__ == "__main__":
    main()
