from dataclasses import dataclass
from typing import Iterable, override

import numpy as np
import pyray as rl
from pyray import RED

from app.entities.base import BaseEntity, EntityTickBundle


class NaiveVehicle(BaseEntity):
    """
    A generic vehicle with customizable forces, handling, and wheel configuration
    """

    @dataclass
    class Wheel:
        position: tuple[float, float]
        acceleration_factor: float

    size: np.typing.NDArray[np.float64]
    velocity: np.typing.NDArray[np.float64] = np.array([0, 0])
    angular_velocity: float = 0

    wheels: list[Wheel]

    def __init__(self, *, size: tuple[float, float], wheels: Iterable[Wheel]):
        super().__init__()
        self.size = np.array(size)
        self.wheels = list(wheels)

        # rendering
        self.body = rl.Rectangle(
            -self.size[0] / 2, -self.size[1] / 2, self.size[0], self.size[1]
        )

    @override
    def tick(self, bundle: EntityTickBundle) -> None:
        for wheel in self.wheels:
            pass

        self.rotation %= 360

    body: rl.Rectangle

    @override
    def draw(self) -> None:
        with self.rl_transform_local():
            rl.draw_rectangle_rec(self.body, RED)
