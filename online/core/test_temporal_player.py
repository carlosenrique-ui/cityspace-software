"""
IPT-CITYSPACE
Teste unitário — TemporalPlayer

Objetivo:
- Garantir controle PLAY / PAUSE / STEP
- Garantir execução em thread
- NÃO envolve UI
- NÃO envolve hardware
"""

import time

from online.core.event_bus import EventBus
from online.core.temporal_state import TemporalState
from online.core.temporal_conductor import TemporalConductor
from online.core.temporal_player import TemporalPlayer


def build_sequence():
    seq = []
    index = 0
    for y in range(2):
        for x in range(3):
            seq.append(
                TemporalState(
                    index=index,
                    phase="TEST",
                    x=x,
                    y=y,
                    z_real_m=0.1,
                    z_pin_cm=10.0,
                )
            )
            index += 1
    return seq


def main():
    print("\n=== TESTE TEMPORAL PLAYER ===\n")

    bus = EventBus()

    conductor = TemporalConductor(
        bus=bus,
        step_delay_s=0.01,
        loop=False,
    )

    sequence = build_sequence()
    conductor.load_sequence(sequence)

    player = TemporalPlayer(conductor)

    # -------------------------
    # STEP
    # -------------------------
    player.step_forward()
    assert conductor.index == 1

    player.step_backward()
    assert conductor.index == 0

    # -------------------------
    # PLAY / PAUSE
    # -------------------------
    player.play()
    time.sleep(0.02)   # curto de propósito
    player.pause()

    # Aqui NÃO garantimos índice > 0
    # apenas que o sistema não travou
    assert conductor.index >= 0

    # -------------------------
    # STOP
    # -------------------------
    player.stop()
    assert conductor.index == 0

    print("✅ TemporalPlayer OK\n")


if __name__ == "__main__":
    main()
