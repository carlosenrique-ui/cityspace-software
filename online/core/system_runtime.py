# online/core/system_runtime.py

"""
OnlineRuntime — Orquestrador mínimo do ONLINE.

Responsabilidades:
- Instanciar EventBus
- Instanciar StateManager
- Registrar estados ONLINE
- Definir estado inicial
- Iniciar o sistema ONLINE

Não contém:
- lógica temporal
- controle físico
- regras de negócio
"""

from online.core.event_bus import EventBus
from online.core.state_manager import StateManager

from online.states.online_root import OnlineRootState
from online.states.initialization import InitializationState
from online.states.presentation import PresentationState
from online.states.analysis import AnalysisState


class OnlineRuntime:
    """
    Orquestrador mínimo do sistema ONLINE.
    """

    def __init__(self):
        self.bus = EventBus()
        self.state_manager = StateManager(event_bus=self.bus)
        self._register_states()

    def _register_states(self):
        """
        Registro explícito dos estados ONLINE.
        """
        self.state_manager.register_state("ONLINE_ROOT", OnlineRootState())
        self.state_manager.register_state("INITIALIZATION", InitializationState())
        self.state_manager.register_state("PRESENTATION", PresentationState())
        self.state_manager.register_state("ANALYSIS", AnalysisState())

    def start(self):
        """
        Inicia o sistema ONLINE no estado raiz.
        """
        print("\n[OnlineRuntime] Starting ONLINE system\n")
        self.state_manager.set_initial_state("ONLINE_ROOT")
