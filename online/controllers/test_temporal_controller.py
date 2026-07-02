from online.core.event_bus import EventBus
from online.core.temporal_state import TemporalState
from online.core.temporal_conductor import TemporalConductor
from online.core.temporal_player import TemporalPlayer

from online.actuators.visual_actuator import VisualActuator
from online.actuators.virtual_actuator import VirtualActuator
from online.renderers.renderer2d import Renderer2D
from online.controllers.temporal_controller import TemporalController


def build_sequence():
    seq = []
    index = 0
    for y in range(2):
        for x in range(3):
            seq.append(
                TemporalState(
                    index=index,
                    phase="SCAN",
                    x=x,
                    y=y,
                    z_real_m=0.1 * (index + 1),
                    z_pin_cm=10 * (index + 1),
                )
            )
            index += 1
    return seq


def main():
    bus = EventBus()

    visual_actuator = VisualActuator(bus)
    virtual_actuator = VirtualActuator()
    renderer = Renderer2D(virtual_actuator)

    controller = TemporalController(
        visual_actuator=visual_actuator,
        renderer=renderer,
    )

    conductor = TemporalConductor(
        bus=bus,
        step_delay_s=0.1,
        loop=False,
    )

    conductor.load_sequence(build_sequence())
    player = TemporalPlayer(conductor)

    # -------------------------
    # Simula execução temporal
    # -------------------------
    player.step_forward()
    controller.tick(t=1)

    player.step_forward()
    controller.tick(t=2)

    player.step_forward()
    controller.tick(t=3)

    print("✔ TemporalController funcionando")


if __name__ == "__main__":
    main()
