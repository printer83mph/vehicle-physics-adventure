from dataclasses import dataclass

import numpy as np
import pyray as rl
from numpy.typing import NDArray


class Graph:
    @dataclass
    class YSeries:
        name: str | None
        color: rl.Color
        thickness: float
        values: NDArray[np.float64]

    def __init__(
        self,
        *,
        position: tuple[int, int] = (0, 0),
        size: tuple[int, int] = (80, 80),
        line_spacing: tuple[float, float] = (5.0, 5.0),
        line_offset: tuple[float, float] = (0.0, 0.0),
        y_scale: float = 25.0,
        y_offset: float = 0.0,
        background_color: tuple[int, int, int, int] | None = None,
    ):
        self.position: tuple[int, int] = position
        self.size: tuple[int, int] = size
        self.line_spacing: tuple[float, float] = line_spacing
        self.line_offset: tuple[float, float] = line_offset
        self.y_scale = y_scale
        self.y_offset = y_offset
        self.background_color = background_color
        self.x_series: NDArray[np.float64] = np.array([], np.float64)
        self.y_series_list: list[Graph.YSeries] = []

    def draw(self):
        """
        Draws all y series in `y_series_list`, automatically scaling the
        x-axis based on data points in `x_series`.

        For the scissor mode to function properly, this must be called in
        pure screen space without any matrix transforms.
        """

        x_min, x_max = np.min(self.x_series), np.max(self.x_series)
        inv_rl_x_scale = 1.0 / (x_max - x_min)
        inv_rl_y_scale = 1.0 / self.y_scale
        x_pos, y_pos = self.position
        x_size, y_size = self.size

        rl.begin_scissor_mode(x_pos, y_pos, x_pos + x_size, y_pos + y_size)
        rl.rl_push_matrix()
        rl.rl_translatef(x_pos, y_pos, 0)

        if self.background_color is not None:
            rl.draw_rectangle(0, 0, x_size, y_size, self.background_color)

        # draw background lines
        # TODO

        # draw data series
        for i in range(len(self.x_series) - 1):
            x1_x2 = self.x_series[i : i + 2]

            # start and end in rl space
            rl_x1_x2 = (x1_x2 - x_min) * inv_rl_x_scale * x_size

            for y_series in self.y_series_list:
                try:
                    y1_y2 = y_series.values[i : i + 2]
                except IndexError:
                    # if index out of bounds, don't draw this segment
                    continue

                rl_y1_y2 = (1.0 - (y1_y2 - self.y_offset) * inv_rl_y_scale) * y_size

                # draw line from i to i+1
                rl.draw_line_ex(
                    (rl_x1_x2[0], rl_y1_y2[0]),
                    (rl_x1_x2[1], rl_y1_y2[1]),
                    y_series.thickness,
                    y_series.color,
                )

        rl.rl_pop_matrix()
        rl.end_scissor_mode()
