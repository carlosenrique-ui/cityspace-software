"""
IPT-CITYSPACE
Teste de integração:
TemporalConductor + EventBus + StateManager

Objetivo:
- Validar emissão real de eventos (MovePinEvent)
- Garantir que EventBus e StateManager recebem eventos
- NÃO validar statechart (isso é o PASSO 2)
"""

from pathlib import Path
from typing import List

from offline.loading.offline_product import OfflineProduct

from online.core.temporal_conductor import TemporalConductor
from online.core.temporal_state import TemporalState
from online.core.event_bus import EventBus
from online.core.state_manager import StateManager
from online.core.state import State
from online.core.actuator_events import MovePinEvent


# ==================================================
# BUILDER: grid -> List[TemporalState]
# ==================================================
def build_sequence_from_grid(grid) -> List[TemporalState]:
    sequence = []
    index = 0

    rows, cols = grid.shape

    for y in range(rows):
        x_range = range(cols) if y % 2 == 0 else reversed(range(cols))

        for x in x_range:
            z_cm = int(grid[y, x])

            state = TemporalState(
                index=index,
                x=x,
                y=y,
                z_pin_cm=z_cm,
                z_real_m=z_cm / 100.0,
                phase="scan",
            )

            sequence.append(state)
            index += 1

    return sequence


def main():
    print("\n=== TESTE TEMPORAL CONDUCTOR + EVENTBUS + STATEMANAGER ===\n")

    snapshot_path = Path(
        "offline/products/snapshots/1cm_rotated"
    )

    # --------------------------
    # OFFLINE → grid
    # --------------------------
    product = OfflineProduct(snapshot_path)
    grid = product.grid

    print(f"Grid carregado: shape={grid.shape}")

    # --------------------------
    # grid → sequência temporal
    # --------------------------
    sequence = build_sequence_from_grid(grid)
    print(f"Sequência criada: {len(sequence)} estados")

    # --------------------------
    # EventBus + StateManager
    # --------------------------
    bus = EventBus()
    state_manager = StateManager(event_bus=bus)

    # --------------------------
    # 🔑 Estado dummy (SEM statechart)
    # --------------------------
    class DummyState(State):
        def on_event(self, event_type, payload):
            # Não transiciona, apenas aceita
            return self

    dummy_state = DummyState()
    dummy_state.name = "DUMMY"

    state_manager.current_state = dummy_state
    state_manager.initialized = True

    print("✔ StateManager inicializado com DummyState")

    # --------------------------
    # 🔑 Conexão EventBus → StateManager
    # --------------------------
    def state_manager_handler(event: MovePinEvent):
        state_manager.handle_event(event.event_type, event)

    bus.subscribe("MOVE_PIN", state_manager_handler)

    print("✔ StateManager inscrito no EventBus para MOVE_PIN")

    # --------------------------
    # TemporalConductor
    # --------------------------
    conductor = TemporalConductor(
        bus=bus,
        step_delay_s=0.0,
        loop=False,
    )

    conductor.load_sequence(sequence)

    # --------------------------
    # Execução passo a passo
    # --------------------------
    for _ in range(len(sequence)):
        conductor.step_forward()

    # --------------------------
    # Validação mínima
    # --------------------------
    print("\nStateManager.current_state:")
    print(state_manager.current_state)

    print("\n✅ TESTE TEMPORAL + EVENTBUS + STATEMANAGER PASSOU\n")


if __name__ == "__main__":
    main()
