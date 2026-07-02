"""
motion_profile.py

Modelo cinemático abstrato para cálculo de tempos previstos de movimento
entre centroides de células da mesa matricial.

Este módulo NÃO:
- controla hardware
- executa movimento
- depende de EventBus
- conhece estados do sistema

Este módulo APENAS:
- calcula tempos previstos a partir de geometria + parâmetros
- fornece decomposição temporal do movimento

Usado exclusivamente pelo TemporalConductor.
"""

from typing import Dict, Tuple
import math


class MotionProfile:
    """
    MotionProfile define como o tempo de deslocamento de um atuador
    é estimado a partir de parâmetros geométricos e cinemáticos.

    Ele é independente de hardware real e pode ser usado tanto
    em simulação quanto em operação real.
    """

    def __init__(
        self,
        horizontal_speed: float,
        vertical_speed: float,
        settling_time: float
    ):
        """
        Parâmetros cinemáticos do atuador.

        :param horizontal_speed: velocidade constante no plano XY (mm/s)
        :param vertical_speed: velocidade constante do pino (mm/s)
        :param settling_time: tempo de assentamento mecânico τ (s)
        """
        self.horizontal_speed = horizontal_speed
        self.vertical_speed = vertical_speed
        self.settling_time = settling_time

    def _horizontal_distance(
        self,
        start_xy: Tuple[float, float],
        end_xy: Tuple[float, float]
    ) -> float:
        """
        Distância euclidiana entre dois centroides no plano XY.
        """
        dx = end_xy[0] - start_xy[0]
        dy = end_xy[1] - start_xy[1]
        return math.sqrt(dx * dx + dy * dy)

    def compute_motion_times(
        self,
        start_xy: Tuple[float, float],
        end_xy: Tuple[float, float],
        target_height: float
    ) -> Dict[str, float]:
        """
        Calcula os tempos previstos para um movimento completo do atuador.

        O movimento é decomposto em:
        - deslocamento horizontal (XY)
        - subida vertical
        - tempo de assentamento (τ)
        - descida vertical

        :param start_xy: centroide inicial da célula (x, y) em mm
        :param end_xy: centroide final da célula (x, y) em mm
        :param target_height: altura do pino (mm)

        :return: dicionário com tempos parciais e tempo total
        """

        # Distância horizontal (mm)
        horizontal_distance = self._horizontal_distance(start_xy, end_xy)

        # Tempo horizontal (s)
        horizontal_time = horizontal_distance / self.horizontal_speed

        # Subida e descida vertical (s)
        lift_time = target_height / self.vertical_speed
        descent_time = target_height / self.vertical_speed

        total_time = (
            horizontal_time
            + lift_time
            + self.settling_time
            + descent_time
        )

        return {
            "horizontal_distance_mm": horizontal_distance,
            "horizontal_time_s": horizontal_time,
            "lift_time_s": lift_time,
            "settling_time_s": self.settling_time,
            "descent_time_s": descent_time,
            "total_time_s": total_time,
        }
