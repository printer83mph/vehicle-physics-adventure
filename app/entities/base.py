from __future__ import annotations

from dataclasses import dataclass

import numpy as np


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

    def __init__(self, x: float, y: float):
        self.position = np.array([x, y])

    def tick(self, bundle: EntityTickBundle) -> None:
        pass

    def should_delete(self) -> bool:
        return False

    def draw(self) -> None:
        pass
