from online.contracts.construction_frame import ConstructionFrame
from online.renderers.renderer2d import Renderer2D
from online.actuators.virtual_actuator import VirtualActuator


def main():
    actuator = VirtualActuator()
    renderer = Renderer2D(actuator)

    # -------------------------------------------------
    # Simula um snapshot convertido em frame
    # -------------------------------------------------
    frame = ConstructionFrame(
        t=0,
        created=[
            ("pin", 0, 0, 5.0),
            ("pin", 0, 1, 8.0),
            ("pin", 1, 1, 12.0),
        ],
        updated=[
            ("pin", 1, 0, 3.0),
        ],
        removed=[]
    )

    renderer.render(frame)

    print("✔ Renderer2D + ConstructionFrame funcionando")


if __name__ == "__main__":
    main()
