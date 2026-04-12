from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Generator

import numpy as np
import pyray as rl


@dataclass
class EntityTickBundle:
    dt: float
    elapsed_time: float
    entities: list[BaseEntity]


class BaseEntity:
    """
    Extensible base class for objects in a scene.
    Can define per-tick logic, drawing, and can report when self-deletion should occur.
    """

    position: np.typing.NDArray[np.float64]
    "`[x, y]` - World position"
    rotation: float
    "Rotation, in radians"

    def __init__(
        self,
        *,
        pos: tuple[float, float] = (0, 0),
        rotation: float = 0,
    ):
        self.position = np.array(pos, float)
        self.rotation = rotation

    def tick(self, bundle: EntityTickBundle) -> None:
        pass

    def should_delete(self) -> bool:
        return False

    def draw(self) -> None:
        pass

    @contextmanager
    def rl_transform_local(self) -> Generator[None]:
        """Temporarily push local transform matrices to the stack, including translation and rotation."""

        rl.rl_push_matrix()
        rl.rl_translatef(self.position[0], self.position[1], 0)
        rl.rl_rotatef(np.rad2deg(self.rotation), 0, 0, 1)
        try:
            yield None
        finally:
            rl.rl_pop_matrix()
