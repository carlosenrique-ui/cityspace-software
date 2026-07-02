from online.contracts.construction_frame import ConstructionFrame
from online.renderers.renderer2d import Renderer2D


class ActuatorMock:
    def execute(self, cmd):
        print(f"{cmd.type.value.upper()} -> {cmd.payload}")


def test_renderer2d_frame():
    actuator = ActuatorMock()
    renderer = Renderer2D(actuator)

    frame = ConstructionFrame(
        t=1,
        created=["Building_A"],
        removed=["Building_B"],
        updated=["Building_C"]
    )

    renderer.render(frame)


if __name__ == "__main__":
    test_renderer2d_frame()
