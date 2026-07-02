import numpy as np


def normalize_ndsm(ndsm):
    """
    Estado OFF-LINE: Normalize (2–98 percentis)
    Normaliza nDSM (metros) para uint8 (0–255).
    """

    print("[Normalize] Normalizando nDSM (2–98%)")

    valid = ndsm[ndsm > 0]

    if valid.size == 0:
        print("[Normalize] Nenhum valor positivo encontrado")
        return np.zeros_like(ndsm, dtype=np.uint8)

    p2, p98 = np.percentile(valid, [2, 98])
    print(f"[Normalize] Percentis: p2={p2:.2f} m | p98={p98:.2f} m")

    norm = (ndsm - p2) / (p98 - p2)
    norm = np.clip(norm, 0, 1)
    gray = (norm * 255).astype(np.uint8)

    gray[ndsm == 0] = 0

    print("[Normalize] Normalização concluída\n")
    return gray


# =====================================================
# NOVA FUNÇÃO — NORMALIZAÇÃO VERTICAL DO TERRENO
# =====================================================

def normalize_vertical_reference(dtm, dsm=None, nodata=None):
    """
    Define a cota zero local baseada na menor cota do DTM.

    Isso garante consistência entre:
    - DTM
    - DSM
    - nDSM
    - curvas de nível
    - produtos derivados

    Regra científica do IPT-CitySpace:
    ZERO LOCAL = min(DTM)
    """

    print("")
    print("================================")
    print("VERTICAL NORMALIZATION")
    print("================================")

    if nodata is not None:
        dtm = np.where(dtm == nodata, np.nan, dtm)

    zero_local = np.nanmin(dtm)

    print("Local terrain zero:", zero_local)

    dtm_local = dtm - zero_local

    print("DTM min (new):", np.nanmin(dtm_local))
    print("DTM max (new):", np.nanmax(dtm_local))

    if dsm is not None:
        dsm_local = dsm - zero_local
        return dtm_local, dsm_local, zero_local

    return dtm_local, None, zero_local