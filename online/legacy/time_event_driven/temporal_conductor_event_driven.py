# online/time/temporal_conductor.py

import time
from typing import Optional
from online.contracts.temporal_event import TemporalEvent, TemporalEventType


class TemporalConductor:
    """
    Player Temporal orientado a eventos.
    Compatível com EventBus real do projeto.
    """

    def __init__(
        self,
        timeline,
        renderer,
        start_t: int = 0,
        end_t: Optional[int] = None,
        fps: float = 1.0
    ):
        self.timeline = timeline
        self.renderer = renderer

        self.start_t = start_t
        self.end_t = end_t
        self.t = start_t

        self.fps = fps
        self._playing = False

    # -------------------------
    # Entrada via EventBus
    # -------------------------

    def handle_event(self, event):
        if not isinstance(event, TemporalEvent):
            return

        if event.event_type == TemporalEventType.PLAY:
            self.play()

        elif event.event_type == TemporalEventType.PAUSE:
            self.pause()

        elif event.event_type == TemporalEventType.STEP_FORWARD:
            self.step_forward()

        elif event.event_type == TemporalEventType.STEP_BACKWARD:
            self.step_backward()

        elif event.event_type == TemporalEventType.SEEK and event.t is not None:
            self.seek(event.t)

    # -------------------------
    # Execução
    # -------------------------

    def play(self):
        self._playing = True
        while self._playing:
            self.step_forward()
            time.sleep(1.0 / self.fps)

    def pause(self):
        self._playing = False

    # -------------------------
    # Tempo
    # -------------------------

    def seek(self, t: int):
        self.t = t
        self._render_current()

    def step_forward(self):
        if self.end_t is not None and self.t >= self.end_t:
            self.pause()
            return

        self.t += 1
        self._render_current()

    def step_backward(self):
        if self.t <= self.start_t:
            return

        self.t -= 1
        self._render_current()

    # -------------------------
    # Interno
    # -------------------------

    def _render_current(self):
        frame = self.timeline.get_frame(self.t)
        self.renderer.render(frame)
