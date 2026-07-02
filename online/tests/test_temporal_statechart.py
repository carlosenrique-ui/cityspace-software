"""
IPT-CITYSPACE
Teste de integração:
Temporal Statechart (StateManager + Estados Formais)

Objetivo:
- Formalizar estados do sistema temporal
- Validar transições determinísticas
- Garantir governança do fluxo (INIT → SCAN → END)
- NÃO envolve UI
- NÃO envolve hardware
"""

from pathlib import Path

from offline.loading.offline_product import OfflineProduct

from online.core.temporal_conductor import TemporalConductor
from online.core.temporal_state import TemporalState
from online.core.event_bus import EventBus
from online.core.state_manager import StateManager
from online.core.state import State
from online.core.actuator_events import MovePinEvent


# ==================================================
# ESTADOS FORMAIS
# ==================================================
class InitState(State):
    name = "INIT"

    def on_event(self, event_type, payload):
        if event_type == "MOVE_PIN":
            return ScanningState()
        return self


class ScanningState(State):
    name = "SCANNING"

    def on_event(self, event_type, payload):
        if event_type == "END_OF_SEQUENCE":
            return EndState()
        return self


class EndState(State):
    name = "END"

    def on_event(self, event_type, payload):
        # Estado terminal
        return self


# ==================================================
# BUILDER: grid -> sequência temporal
# ==================================================
def build_sequence_from_grid(grid):
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
    print("\n=== TESTE TEMPORAL STATECHART ===\n")

    snapshot_path = Path(
        "offline/products/snapshots/1cm_rotated"
    )

    # --------------------------
    # OFFLINE → grid
    # --------------------------
    product = OfflineProduct(snapshot_path)
    grid = product.grid
    sequence = build_sequence_from_grid(grid)

    print(f"Grid carregado: {grid.shape}")
    print(f"Sequência temporal: {len(sequence)} estados")

    # --------------------------
    # EventBus + StateManager
    # --------------------------
    bus = EventBus()
    state_manager = StateManager(event_bus=bus)

    # Estado inicial
    state_manager.current_state = InitState()
    state_manager.initialized = True

    print(f"Estado inicial: {state_manager.current_state.name}")

    # --------------------------
    # Conectar EventBus → StateManager
    # --------------------------
    def state_manager_handler(event):
        state_manager.handle_event(event.event_type, event)

    bus.subscribe("MOVE_PIN", state_manager_handler)
    bus.subscribe("END_OF_SEQUENCE", state_manager_handler)

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
    # Execução temporal
    # --------------------------
    for _ in range(len(sequence)):
        conductor.step_forward()

    # Evento explícito de fim
    bus.emit(
        MovePinEvent(
            event_type="END_OF_SEQUENCE",
            timestamp=None,
            pin_id=None,
            x=None,
            y=None,
            z_real_m=None,
            z_pin_cm=None,
            phase="end",
        )
    )

    # --------------------------
    # Validações
    # --------------------------
    print(f"\nEstado final: {state_manager.current_state.name}")

    assert state_manager.current_state.name == "END", \
        "Statechart não terminou em END"

    print("\n✅ TESTE TEMPORAL STATECHART PASSOU\n")


if __name__ == "__main__":
    main()
