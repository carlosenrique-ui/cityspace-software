"""
IPT-CITYSPACE
Console Player — UI Temporal Observadora

Objetivo:
- Observar a execução temporal do sistema
- Exibir estado, posição e Z
- NÃO controlar o sistema
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
# STATECHART (já validado)
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
        return self


# ==================================================
# BUILDER
# ==================================================
def build_sequence_from_grid(grid):
    sequence = []
    index = 0

    rows, cols = grid.shape

    for y in range(rows):
        x_range = range(cols) if y % 2 == 0 else reversed(range(cols))
        for x in x_range:
            z_cm = int(grid[y, x])

            sequence.append(
                TemporalState(
                    index=index,
                    x=x,
                    y=y,
                    z_pin_cm=z_cm,
                    z_real_m=z_cm / 100.0,
                    phase="scan",
                )
            )
            index += 1

    return sequence


# ==================================================
# CONSOLE OBSERVER
# ==================================================
class ConsoleObserver:
    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager

    def on_move_pin(self, event: MovePinEvent):
        state_name = (
            self.state_manager.current_state.name
            if self.state_manager.current_state
            else "NONE"
        )

        print(
            f"State={state_name:9s} | "
            f"(x={event.x}, y={event.y}) | "
            f"Z={event.z_pin_cm:3d} cm"
        )


# ==================================================
# MAIN
# ==================================================
def main():
    print("\n=== IPT-CITYSPACE | CONSOLE PLAYER ===\n")

    snapshot_path = Path(
        "offline/products/snapshots/1cm_rotated"
    )

    # --------------------------
    # OFFLINE
    # --------------------------
    product = OfflineProduct(snapshot_path)
    grid = product.grid
    sequence = build_sequence_from_grid(grid)

    print(f"Grid: {grid.shape}")
    print(f"Steps: {len(sequence)}")

    # --------------------------
    # EventBus + StateManager
    # --------------------------
    bus = EventBus()
    state_manager = StateManager(event_bus=bus)

    state_manager.current_state = InitState()
    state_manager.initialized = True

    # EventBus → StateManager
    def state_manager_handler(event):
        state_manager.handle_event(event.event_type, event)

    bus.subscribe("MOVE_PIN", state_manager_handler)
    bus.subscribe("END_OF_SEQUENCE", state_manager_handler)

    # --------------------------
    # Console Observer
    # --------------------------
    observer = ConsoleObserver(state_manager)
    bus.subscribe("MOVE_PIN", observer.on_move_pin)

    # --------------------------
    # TemporalConductor
    # --------------------------
    conductor = TemporalConductor(
        bus=bus,
        step_delay_s=0.05,
        loop=False,
    )

    conductor.load_sequence(sequence)

    # --------------------------
    # EXECUÇÃO
    # --------------------------
    for _ in range(len(sequence)):
        conductor.step_forward()

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

    print("\n=== FIM DA EXECUÇÃO ===\n")


if __name__ == "__main__":
    main()
