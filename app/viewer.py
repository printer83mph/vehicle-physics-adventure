import pyray
from pyray import RAYWHITE

from app.entities.naivevehicle import NaiveVehicle
from app.scene import Scene
from app.telemetry import Telemetry


class Viewer:
    def __init__(self):
        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600

        pyray.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "awesome vehicle simulator")
        pyray.set_target_fps(
            pyray.get_monitor_refresh_rate(pyray.get_current_monitor())
        )

        car = NaiveVehicle(
            size=(40, 20),
            wheels=[
                NaiveVehicle.Wheel(
                    position=(15, 10), acceleration_factor=0.0, turns=True
                ),
                NaiveVehicle.Wheel(
                    position=(15, -10), acceleration_factor=0.0, turns=True
                ),
                NaiveVehicle.Wheel(position=(-15, 10), acceleration_factor=1.0),
                NaiveVehicle.Wheel(position=(-15, -10), acceleration_factor=1.0),
            ],
        )

        self.scene: Scene = Scene()
        self.scene.entities.append(car)
        self.camera: pyray.Camera2D = pyray.Camera2D()
        self.camera.target = pyray.Vector2(20, 20)
        self.camera.offset = pyray.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.camera.rotation = 0.0
        self.camera.zoom = 1.0

        self.telemetry = Telemetry(
            car=car,
            SCREEN_WIDTH=SCREEN_WIDTH,
            SCREEN_HEIGHT=SCREEN_HEIGHT,
        )

    def _tick(self):
        dt = pyray.get_frame_time()
        dt = min(dt, 0.066667)  # prevent large timesteps
        self.scene.tick(dt)

    def _draw(self):
        pyray.begin_drawing()
        pyray.clear_background(RAYWHITE)

        pyray.begin_mode_2d(self.camera)
        self.scene.draw()
        pyray.end_mode_2d()

        self.telemetry.draw(self.scene)

        pyray.end_drawing()

    def run(self):
        while not pyray.window_should_close():
            self._tick()
            self._draw()
