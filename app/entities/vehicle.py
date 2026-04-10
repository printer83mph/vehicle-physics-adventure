from typing import override

import numpy as np
import pyray
from pyray import RED

from app.entities.base import BaseEntity, EntityTickBundle


class Vehicle(BaseEntity):
    """
    A generic vehicle with customizable forces, handling, and wheel configuration
    """

    @override
    def tick(self, bundle: EntityTickBundle) -> None:
        self.position[0] = np.sin(bundle.elapsed_time * np.pi) * 80

    @override
    def draw(self) -> None:
        pyray.draw_rectangle(self.position[0] - 20, self.position[1] - 20, 40, 40, RED)
