"""
IPT-CITYSPACE
TemporalPlayer

Responsável por:
- Executar TemporalConductor em thread
- Expor comandos PLAY / PAUSE / STOP / STEP
- Fornecer heartbeat simples para UI
"""

import threading
from typing import Optional

from online.core.temporal_conductor import TemporalConductor


class TemporalPlayer:
    """
    Wrapper assíncrono (thread) para TemporalConductor.
    """

    def __init__(self, conductor: TemporalConductor):
        self.conductor = conductor
        self._thread: Optional[threading.Thread] = None
        self._tick: int = 0  # 👈 heartbeat simples

    # ----------------------------------
    # CONTROLES
    # ----------------------------------

    def play(self):
        if self._thread and self._thread.is_alive():
            return

        self._thread = threading.Thread(
            target=self._run_play,
            daemon=True,
        )
        self._thread.start()

    def _run_play(self):
        self.conductor.play()
        self._tick += 1

    def pause(self):
        self.conductor.pause()
        self._tick += 1

    def stop(self):
        self.conductor.stop()
        self._tick += 1

    def step_forward(self):
        self.conductor.step_forward()
        self._tick += 1

    def step_backward(self):
        self.conductor.step_backward()
        self._tick += 1

    # ----------------------------------
    # HEARTBEAT (para Dash)
    # ----------------------------------

    def get_tick(self) -> int:
        return self._tick
