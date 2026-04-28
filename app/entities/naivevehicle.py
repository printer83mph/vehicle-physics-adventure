from dataclasses import dataclass, field
from typing import Iterable, override

import numpy as np
import pyray as rl
from pyray import BLACK, BLUE, GREEN, RED
from raylib import KEY_A, KEY_D, KEY_S, KEY_SPACE, KEY_W

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

    def __init__(self, *, size: tuple[float, float], wheels: Iterable[Wheel]):
        super().__init__()

        self.size: np.typing.NDArray[np.float64] = np.array(size, np.float64)
        self.wheels: list[NaiveVehicle.Wheel] = list(wheels)

        self.turn_amount: float = 0.0
        "how far left or right the car is steering, within [-1, 1]"

        # physics tracking
        self.velocity: np.typing.NDArray[np.float64] = np.array([0.0, 0.0], np.float64)
        self.angular_velocity: float = 0.0
        self.sliding: bool = False

        # parameters
        self.damping: float = 0.9
        self.brake_damping: float = 0.25
        self.angular_damping: float = 0.6
        self.turn_speed = 2.0
        self.acceleration = 150
        self.turn_ratio = 0.012

        # rendering
        self.body = rl.Rectangle(
            -self.size[0] / 2, -self.size[1] / 2, self.size[0], self.size[1]
        )

        self._steer_line_start_pos = rl.Vector2()
        self._steer_line_end_pos = rl.Vector2()

    @override
    def tick(self, bundle: EntityTickBundle) -> None:

        forward = self._get_forward_vector()
        steering_forward = self._get_steering_forward_vector()

        handbraking = rl.is_key_down(KEY_SPACE)
        side_speed = np.linalg.norm(np.cross(self.velocity, steering_forward))

        if self.sliding and abs(side_speed) < 45.0:
            self.sliding = False
        elif not self.sliding and abs(side_speed) > 85.0:
            self.sliding = True

        if handbraking:
            self.sliding = True

        # add forward/backwards velocity
        if rl.is_key_down(KEY_W):
            self.velocity += forward * self.acceleration * bundle.dt
        if rl.is_key_down(KEY_S):
            self.velocity -= forward * self.acceleration * bundle.dt

        forward_speed = np.dot(self.velocity, forward)
        if not self.sliding:
            # static friction: project to only forward velocity
            self.velocity = forward_speed * forward

        if rl.is_key_down(KEY_A):
            self.turn_amount = max(
                -1,
                self.turn_amount - self.turn_speed * bundle.dt,
            )
        elif rl.is_key_down(KEY_D):
            self.turn_amount = min(
                1,
                self.turn_amount + self.turn_speed * bundle.dt,
            )
        else:
            self.turn_amount *= np.pow(0.01, bundle.dt)

        # rotate car based on "turn amount"
        turn_factor = 0.7 if self.sliding else 1.0
        self.angular_velocity = (
            self.turn_amount * self.turn_ratio * forward_speed * turn_factor
        )
        self.rotation += self.angular_velocity * bundle.dt

        # do damping
        damping = self.brake_damping if self.sliding else self.damping
        self.velocity *= np.pow(damping, bundle.dt)
        self.angular_velocity *= np.pow(self.angular_damping, bundle.dt)

        # integrate position/vel
        self.position += self.velocity * bundle.dt

        self.rotation += self.angular_velocity * bundle.dt
        self.rotation %= np.pi * 2

    def _get_forward_vector(self):
        return np.array([np.cos(self.rotation), np.sin(self.rotation)], np.float64)

    def _get_steering_forward_vector(self):
        rotation = self.rotation + self.turn_amount * np.pi / 8
        return np.array([np.cos(rotation), np.sin(rotation)], np.float64)

    @override
    def draw(self) -> None:
        with self.rl_transform_local():
            rl.draw_rectangle_rec(self.body, BLUE if self.sliding else RED)

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

        steering_vector = self._get_steering_forward_vector() * 40

        self._steer_line_start_pos.x = self.position[0]
        self._steer_line_start_pos.y = self.position[1]
        self._steer_line_end_pos.x = self.position[0] + steering_vector[0]
        self._steer_line_end_pos.y = self.position[1] + steering_vector[1]
        rl.draw_line_ex(
            self._steer_line_start_pos,
            self._steer_line_end_pos,
            2.0,
            GREEN,
        )
