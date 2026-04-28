import pyray
from pyray import RAYWHITE

from app.scene import Scene


class Viewer:
    scene: Scene
    camera: pyray.Camera2D = pyray.Camera2D()

    def __init__(self, scene: Scene):
        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600

        pyray.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "awesome vehicle simulator")
        pyray.set_target_fps(
            pyray.get_monitor_refresh_rate(pyray.get_current_monitor())
        )

        self.scene = scene
        self.camera.target = pyray.Vector2(20, 20)
        self.camera.offset = pyray.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.camera.rotation = 0.0
        self.camera.zoom = 1.0

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

        pyray.end_drawing()

    def run(self):
        while not pyray.window_should_close():
            self._tick()
            self._draw()
