"""
IPT-CITYSPACE
Physical Motion Profile

Modelo físico canônico para:

- Mesa virtual
- Mesa real futura

Objetivo:
manter equivalência temporal entre simulação e hardware.
"""

import math

# ============================================================
# CURVA FÍSICA — S-CURVE
# ============================================================

def ease_in_out(t: float) -> float:
    """
    Curva típica de atuador real:

        aceleração → cruzeiro → desaceleração

    Entrada:
        t ∈ [0,1]

    Retorna:
        progresso suavizado.
    """
    return 0.5 - 0.5 * math.cos(math.pi * t)


# ============================================================
# GERADOR DE MOVIMENTO
# ============================================================

def generate_motion_steps(
    target_height: float,
    duration_s: float,
    frame_duration_s: float = 0.1,
    time_scale: float = 1.0,
    return_metadata: bool = False,
):
    """
    Gera sequência de alturas absolutas simulando movimento físico.

    Parameters
    ----------
    target_height : float
        Altura final do pino (metros)

    duration_s : float
        Tempo físico total da subida (segundos)

    frame_duration_s : float
        Duração visual de cada frame

    time_scale : float
        Escala temporal global (debug / simulação)

    return_metadata : bool
        Futuro uso para sincronização dos 3 relógios.

    Returns
    -------
    list[float]
        Lista de alturas absolutas por frame.
    """

    # --------------------------------------------------------
    # Guardrails físicos
    # --------------------------------------------------------
    target_height = max(0.0, float(target_height))
    duration_s = max(0.0, float(duration_s))
    frame_duration_s = max(1e-6, float(frame_duration_s))

    duration_s *= time_scale

    n_frames = max(1, math.ceil(duration_s / frame_duration_s))

    values = []

    for i in range(n_frames):
        t = (i + 1) / n_frames
        p = ease_in_out(t)
        values.append(target_height * p)

    if return_metadata:
        return {
            "values": values,
            "n_frames": n_frames,
            "duration_s": duration_s,
        }

    return values
