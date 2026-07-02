from online.contracts.temporal_event import TemporalEvent, TemporalEventType


class TemporalSequence:
    """
    StateChart temporal mínimo:
    emite eventos temporais no EventBus
    """

    def __init__(self, bus):
        self.bus = bus

    def run_single_cell(self):
        self.bus.emit(TemporalEvent(event_type=TemporalEventType.STEP_FORWARD))
        self.bus.emit(TemporalEvent(event_type=TemporalEventType.STEP_FORWARD))
        self.bus.emit(TemporalEvent(event_type=TemporalEventType.STEP_BACKWARD))
        self.bus.emit(TemporalEvent(event_type=TemporalEventType.SEEK, t=4))
