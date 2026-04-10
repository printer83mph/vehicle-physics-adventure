from app.scene import Scene
from app.viewer import Viewer


def main():
    scene = Scene()
    viewer = Viewer(scene)

    viewer.run()


if __name__ == "__main__":
    main()
