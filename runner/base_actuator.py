from abc import ABC, abstractmethod


class BaseActuator(ABC):
    """
    Interface canônica para qualquer tipo de mesa:
    - virtual (frames, GIF, UI)
    - real (motores, pinos, hardware)
    """

    @abstractmethod
    def move_to_cell(self, row: int, col: int):
        """Move o foco/atuador para a célula (row, col)."""
        pass

    @abstractmethod
    def set_pin_height(self, row: int, col: int, height_cm: float):
        """Define a altura do pino em cm."""
        pass

    @abstractmethod
    def wait(self, seconds: float):
        """Aguarda tempo físico ou simulado."""
        pass

    @abstractmethod
    def reset(self):
        """Reseta o estado da mesa."""
        pass
