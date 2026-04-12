from typing import override

import numpy as np
import pyray as rl
from pyray import RED

from app.entities.base import BaseEntity, EntityTickBundle


class Vehicle(BaseEntity):
    """
    A generic vehicle with customizable forces, handling, and wheel configuration
    """

    @override
    def tick(self, bundle: EntityTickBundle) -> None:
        self.position[0] = np.sin(bundle.elapsed_time * np.pi) * 80
        self.rotation += bundle.dt * np.pi * 2

        self.rotation %= 360

    body: rl.Rectangle = rl.Rectangle(-20, -40, 40, 80)

    @override
    def draw(self) -> None:
        with self.rl_transform_local():
            rl.draw_rectangle_rec(self.body, RED)
