import time

import numpy as np
import pyray as rl
from raylib.colors import LIGHTGRAY, RAYWHITE

from app.ui.graph import Graph


def main():

    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 400

    rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "awesome vehicle simulator")
    rl.set_target_fps(rl.get_monitor_refresh_rate(rl.get_current_monitor()))

    graph = Graph(
        position=(50, 50),
        size=(300, 300),
        y_scale=3.0,
        y_offset=-1.5,
        background_color=LIGHTGRAY,
    )

    # init y series
    y_series_sin = Graph.YSeries(
        name="default",
        color=rl.RED,
        thickness=2,
        values=np.zeros(1, np.float64),
    )
    graph.y_series_list.append(y_series_sin)

    def update_graph():
        time_offset = time.time()
        graph.x_series = np.linspace(
            time_offset, time_offset + 12.0, 50, dtype=np.float64
        )
        y_series_sin.values = np.sin(graph.x_series)

    while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(RAYWHITE)

        update_graph()

        # test draw graph
        graph.draw()

        rl.end_drawing()


if __name__ == "__main__":
    main()
