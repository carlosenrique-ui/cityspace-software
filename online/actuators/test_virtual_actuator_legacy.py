from online.actuators.virtual_actuator import VirtualActuator
from online.renderers.renderer2d import Renderer2D
from online.time.construction_timeline import ConstructionTimeline
from online.time.temporal_conductor import TemporalConductor
from online.contracts.temporal_event import TemporalEvent, TemporalEventType
from online.core.event_bus import EventBus


print("\n### TESTE — MÓDULO 2 (VIRTUAL ACTUATOR) ###\n")

bus = EventBus()

timeline = ConstructionTimeline()
timeline.add_event(1, "create", "Building_A")
timeline.add_event(2, "create", "Building_B")
timeline.add_event(3, "update", "Building_B")
timeline.add_event(4, "remove", "Building_A")

actuator = VirtualActuator()
renderer = Renderer2D(actuator)

conductor = TemporalConductor(
    timeline=timeline,
    renderer=renderer,
    start_t=0,
    end_t=5,
    fps=1.0
)

bus.subscribe(TemporalEventType.STEP_FORWARD, conductor.handle_event)
bus.subscribe(TemporalEventType.STEP_BACKWARD, conductor.handle_event)
bus.subscribe(TemporalEventType.SEEK, conductor.handle_event)

bus.emit(TemporalEvent(event_type=TemporalEventType.STEP_FORWARD))
bus.emit(TemporalEvent(event_type=TemporalEventType.STEP_FORWARD))
bus.emit(TemporalEvent(event_type=TemporalEventType.STEP_BACKWARD))
bus.emit(TemporalEvent(event_type=TemporalEventType.SEEK, t=4))

print("\nSNAPSHOT FINAL:", actuator.snapshot())
print("\n### FIM DO TESTE ###\n")
