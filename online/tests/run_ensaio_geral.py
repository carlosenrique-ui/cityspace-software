"""
IPT-CITYSPACE
ENSAIO GERAL – TESTE INTEGRADO (ONLINE)

Integra:
- EventBus
- TemporalConductor
- ActuatorStatechart
- ActuatorDriverMock

Sem hardware real NOTEBOOK
"""

import time
import threading
import numpy as np
from pathlib import Path

# ===============================
# IMPORTS ONLINE
# ===============================

from online.core.event_bus import EventBus
from online.core.actuator_events import (
    MovePinEvent,
    PinReachedEvent,
    PhaseChangedEvent,
)

from online.states.actuator_statechart import ActuatorStatechart
from online.time.temporal_conductor import TemporalConductor

from online.hardware.actuator_driver_mock import ActuatorDriverMock
from online.hardware.actuator_driver_base import ActuatorCommand

# ===============================
# PATHS
# ===============================

ENGINE_ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ENGINE_ROOT / "data/csv/quadro_8x16.csv"

assert CSV_PATH.exists(), f"CSV não encontrado: {CSV_PATH}"

# ===============================
# LOAD GRID (METROS)
# ===============================

grid_raw = np.loadtxt(CSV_PATH, delimiter=",")
assert grid_raw.shape == (8, 16)

z_min = grid_raw.min()
grid_m = grid_raw - z_min

print("\nGRID CARREGADO")
print("Shape:", grid_m.shape)
print("Altura mínima (m):", z_min)
print("Altura máxima (m):", grid_m.max())

# ===============================
# EVENT BUS
# ===============================

bus = EventBus()

# ===============================
# DRIVER MOCK
# ===============================

driver = ActuatorDriverMock()
print("[DRIVER MOCK] Inicializado")

# ===============================
# SUBSCRIBERS
# ===============================

import time
from online.core.actuator_events import PinReachedEvent

def on_move(evt: MovePinEvent):
    """
    Tradução EVENTO → COMANDO DE HARDWARE
    """

    cmd = ActuatorCommand(
        pin_id=evt.pin_id,
        x=evt.x,
        y=evt.y,
        z_real_m=evt.z_real_m,
        z_pin_cm=evt.z_pin_cm,
        phase=evt.phase,
    )

    driver.move_pin(cmd)

    # resposta imediata do MOCK (simula hardware)
    bus.emit(
        PinReachedEvent(
            event_type="PIN_REACHED",
            timestamp=time.time(),
            pin_id=evt.pin_id,
            z_pin_cm=evt.z_pin_cm,
        )
    )


def on_reached(evt: PinReachedEvent):
    print(
        f"[OK ] pin={evt.pin_id:03d} "
        f"z_pin={evt.z_pin_cm:.1f} cm"
    )

def on_phase(evt: PhaseChangedEvent):
    print(f"\n=== FASE: {evt.phase} ===\n")

bus.subscribe(MovePinEvent, on_move)
bus.subscribe(PinReachedEvent, on_reached)
bus.subscribe(PhaseChangedEvent, on_phase)

# ===============================
# ACTUATOR STATECHART
# ===============================

actuator = ActuatorStatechart(
    event_bus=bus,
    move_speed_cm_s=2.0,
    settling_time_s=0.3,
)

# ===============================
# TEMPORAL CONDUCTOR
# ===============================

conductor = TemporalConductor(
    bus=bus,
    grid_rows=8,
    grid_cols=16,
    cell_size_cm=1.0,
    step_delay_s=0.05,
)

conductor.set_phases([
    {"name": "1940–1959", "color": "#1f77b4"},
    {"name": "1960–1979", "color": "#2ca02c"},
    {"name": "1980–1999", "color": "#ff7f0e"},
    {"name": "2000–2020", "color": "#d62728"},
])

# ===============================
# LOOP DO ATUADOR
# ===============================

def actuator_loop():
    while conductor.running:
        actuator.update()
        time.sleep(0.01)

threading.Thread(
    target=actuator_loop,
    daemon=True
).start()

# ===============================
# EXECUÇÃO
# ===============================

print("\nINICIANDO ENSAIO GERAL\n")
start = time.time()

conductor.run(grid_m)

elapsed = time.time() - start

print("\nENSAIO FINALIZADO")
print(f"Tempo total aproximado: {elapsed:.1f} s")
