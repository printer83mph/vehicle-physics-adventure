from app.entities.base import BaseEntity, EntityTickBundle
from app.entities.vehicle import Vehicle


class Scene:
    entities: list[BaseEntity] = []
    elapsed_time: float = 0

    def __init__(self):
        self.entities.append(Vehicle(0, 0))

    def tick(self, dt: float):
        # Bundle of scene/tick info to send to all entities
        bundle = EntityTickBundle(
            dt=dt,
            elapsed_time=self.elapsed_time,
            entities=self.entities,
        )

        # run entity ticks
        for entity in self.entities:
            entity.tick(bundle)

        # remove entities that request self-deletion
        self.entities = [
            entity for entity in self.entities if not entity.should_delete()
        ]

        self.elapsed_time += dt

    def draw(self):
        for entity in self.entities:
            entity.draw()
