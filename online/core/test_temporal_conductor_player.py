"""
TemporalConductor
-----------------
Scheduler / Player temporal síncrono.

Responsável por:
- Navegar uma sequência temporal discreta (timeline)
- Executar PLAY / PAUSE / STEP / REVERSE
- Emitir eventos MovePinEvent
- NÃO conhece hardware
- NÃO conhece tempo mecânico real
"""

import time
from enum import Enum, auto
from typing import List, Optional

from online.core.temporal_state import TemporalState
from online.core.actuator_events import MovePinEvent


class PlayerMode(Enum):
    STOPPED = auto()
    PLAY = auto()
    REVERSE = auto()
    PAUSED = auto()


class TemporalConductor:
    def __init__(
        self,
        bus,
        grid_cols: int,
        step_delay_s: float = 0.05,
    ):
        self.bus = bus
        self.grid_cols = grid_cols
        self.step_delay_s = step_delay_s

        self.sequence: List[TemporalState] = []
        self.current_index: int = 0

        self.running: bool = False
        self.mode: PlayerMode = PlayerMode.STOPPED

    # ======================================================
    # LOAD
    # ======================================================

    def load_sequence(self, sequence: List[TemporalState]):
        assert sequence, "Sequência temporal vazia"
        self.sequence = sequence
        self.current_index = 0
        self.mode = PlayerMode.STOPPED
        self.running = False

    # ======================================================
    # INTERNAL
    # ======================================================

    def _emit_current_state(self):
        state = self.sequence[self.current_index]

        pin_id = state.y * self.grid_cols + state.x

        evt = MovePinEvent(
            event_type="MOVE_PIN",
            timestamp=None,
            pin_id=pin_id,
            x=state.x,
            y=state.y,
            z_real_m=state.z_real_m,
            z_pin_cm=state.z_pin_cm,
            phase=state.phase,
        )

        self.bus.emit(evt)

    # ======================================================
    # STEP
    # ======================================================

    def step_forward(self):
        if self.current_index < len(self.sequence) - 1:
            self.current_index += 1
            self._emit_current_state()

    def step_backward(self):
        if self.current_index > 0:
            self.current_index -= 1
            self._emit_current_state()

    # ======================================================
    # PLAY / CONTROL
    # ======================================================

    def play(self):
        if not self.sequence:
            return

        self.mode = PlayerMode.PLAY
        self.running = True

        while self.running and self.current_index < len(self.sequence) - 1:
            self.step_forward()
            time.sleep(self.step_delay_s)

        self.running = False
        self.mode = PlayerMode.STOPPED

    def reverse(self):
        if not self.sequence:
            return

        self.mode = PlayerMode.REVERSE
        self.running = True

        while self.running and self.current_index > 0:
            self.step_backward()
            time.sleep(self.step_delay_s)

        self.running = False
        self.mode = PlayerMode.STOPPED

    def pause(self):
        self.running = False
        self.mode = PlayerMode.PAUSED

    def stop(self):
        self.running = False
        self.current_index = 0
        self.mode = PlayerMode.STOPPED

    # ======================================================
    # SEEK / QUERY  (⚠️ ESSENCIAL PARA UI)
    # ======================================================

    def set_index(self, index: int):
        """Alias explícito para controle via UI (slider)."""
        if 0 <= index < len(self.sequence):
            self.current_index = index
            self._emit_current_state()

    def get_index(self) -> int:
        return self.current_index

    def get_current_state(self) -> Optional[TemporalState]:
        if not self.sequence:
            return None
        return self.sequence[self.current_index]
