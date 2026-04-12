from dataclasses import dataclass, field
from typing import Iterable, override

import numpy as np
import pyray as rl
from pyray import BLACK, RED
from raylib import KEY_A, KEY_D, KEY_S, KEY_W

from app.entities.base import BaseEntity, EntityTickBundle


class NaiveVehicle(BaseEntity):
    """
    A generic vehicle with customizable forces, handling, and wheel configuration
    """

    @dataclass
    class Wheel:
        position: tuple[float, float]
        acceleration_factor: float
        size: np.typing.NDArray[np.float64] = field(
            default_factory=lambda: np.array([10, 4], np.float64)
        )
        turns: bool = False

    size: np.typing.NDArray[np.float64]

    turn_amount: float = 0.0
    "within [-1, 1]"

    velocity: np.typing.NDArray[np.float64] = np.array([0.0, 0.0], np.float64)
    angular_velocity: float = 0.0
    damping: float = 0.1
    angular_damping: float = 0.1

    turn_speed = 2.0
    acceleration = 400
    turn_ratio = 0.015

    wheels: list[Wheel]

    body: rl.Rectangle

    def __init__(self, *, size: tuple[float, float], wheels: Iterable[Wheel]):
        super().__init__()
        self.size = np.array(size, np.float64)
        self.wheels = list(wheels)

        # rendering
        self.body = rl.Rectangle(
            -self.size[0] / 2, -self.size[1] / 2, self.size[0], self.size[1]
        )

    @override
    def tick(self, bundle: EntityTickBundle) -> None:

        forward = self._get_forward_vector()

        # add forward/backwards velocity
        if rl.is_key_down(KEY_W):
            self.velocity += forward * self.acceleration * bundle.dt
        if rl.is_key_down(KEY_S):
            self.velocity -= forward * self.acceleration * bundle.dt

        # project to only forward velocity
        forward_speed = np.dot(self.velocity, forward)
        self.velocity = forward_speed * forward

        if rl.is_key_down(KEY_A):
            self.turn_amount = max(-1, self.turn_amount - self.turn_speed * bundle.dt)
        elif rl.is_key_down(KEY_D):
            self.turn_amount = min(1, self.turn_amount + self.turn_speed * bundle.dt)
        else:
            self.turn_amount *= np.pow(0.01, bundle.dt)

        self.rotation += self.turn_amount * self.turn_ratio * forward_speed * bundle.dt

        # do damping
        self.velocity *= np.pow(self.damping, bundle.dt)
        self.angular_velocity *= np.pow(self.angular_damping, bundle.dt)

        # integrate position/vel
        self.position += self.velocity * bundle.dt

        self.rotation += self.angular_velocity * bundle.dt
        self.rotation %= np.pi * 2

    def _get_forward_vector(self):
        return np.array([np.cos(self.rotation), np.sin(self.rotation)], np.float64)

    @override
    def draw(self) -> None:
        with self.rl_transform_local():
            rl.rl_translatef(self.size[1] / 2, 0, 0)
            rl.draw_rectangle_rec(self.body, RED)

            for wheel in self.wheels:
                rl.rl_push_matrix()
                rl.rl_translatef(wheel.position[0], wheel.position[1], 0)
                if wheel.turns:
                    rl.rl_rotatef(np.rad2deg(self.turn_amount * 0.7), 0, 0, 1)

                rl.draw_rectangle(
                    int(-wheel.size[0] / 2),
                    int(-wheel.size[1] / 2),
                    int(wheel.size[0]),
                    int(wheel.size[1]),
                    BLACK,
                )
                rl.rl_pop_matrix()
