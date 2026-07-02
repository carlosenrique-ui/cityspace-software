# online/core/test_temporal_conductor.py

import numpy as np

from online.core.temporal_sequence import TemporalSequenceBuilder
from online.core.temporal_conductor import TemporalConductor
from online.core.event_bus import EventBus


def main():
    print("Sequence gerada: 512 estados")

    # ----------------------------
    # Grid de teste
    # ----------------------------
    grid_rows = 8
    grid_cols = 16
    grid_m = np.zeros((grid_rows, grid_cols))

    grid_m[3, 4] = 0.10
    grid_m[7, 15] = 0.20

    phases = [
        {"name": "1940–1959"},
        {"name": "1960–1979"},
        {"name": "1980–1999"},
        {"name": "2000–2020"},
    ]

    builder = TemporalSequenceBuilder(
        grid_rows=grid_rows,
        grid_cols=grid_cols
    )

    sequence = builder.build(grid_m, phases)

    # ----------------------------
    # Infraestrutura
    # ----------------------------
    bus = EventBus()

    # 🔧 ATENÇÃO: grid_cols NÃO EXISTE MAIS NO CONSTRUCTOR
    conductor = TemporalConductor(
        bus=bus,
        step_delay_s=0.0,
        loop=False,
    )

    conductor.load_sequence(sequence)

    # ----------------------------
    # Testes básicos
    # ----------------------------
    assert len(sequence) == 512

    conductor.step_forward()
    conductor.step_forward()
    conductor.step_backward()

    conductor.play()
    conductor.reverse()

    print("✔ TemporalConductor OK")


if __name__ == "__main__":
    main()
