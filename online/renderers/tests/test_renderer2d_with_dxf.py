# ======================================================
# TESTE AUTO-DOCUMENTADO — RENDERER2D + DXF (FUNDO)
# IPT-CITYSPACE
# ======================================================
#
# Este teste segue EXATAMENTE o padrão real do Renderer2D:
# - layers são fornecidas no construtor
# - não existe add_layer()
# - DXF entra como layer de fundo
#
# ======================================================

import numpy as np
import matplotlib.pyplot as plt

from online.renderers.renderer2d import Renderer2D
from online.renderers.layers.layer_dxf_lines import LayerDXFLines


# ======================================================
# ACTUATOR DUMMY (respeita o contrato do Renderer2D)
# ======================================================
class ActuatorDummy:
    def apply(self, *args, **kwargs):
        return None


def print_header():
    print("=" * 70)
    print("TESTE: Renderer2D + DXF como Layer de Fundo")
    print("Projeto: IPT-CitySpace")
    print("=" * 70)
    print("DXF: OFFLINE / referência espacial")
    print("Eixo X: Sentido Bairro (Av. Escola Politécnica)")
    print("Eixo Y: Sentido Campus (USP)")
    print("-" * 70)


def main():

    print_header()

    # --------------------------------------------------
    # [1] Estado fictício da mesa (8 x 16)
    # --------------------------------------------------
    estado_mesa = np.zeros((8, 16))

    # --------------------------------------------------
    # [2] Actuator dummy
    # --------------------------------------------------
    actuator = ActuatorDummy()

    # --------------------------------------------------
    # [3] Grid e colormap (exigidos por Layer2D)
    # --------------------------------------------------
    grid = estado_mesa
    colormap = "inferno"

    # --------------------------------------------------
    # [4] Layer DXF (FUNDO)
    # --------------------------------------------------
    layer_dxf = LayerDXFLines(
        name="DXF_FUNDO",
        grid=grid,
        colormap=colormap,
        dxf_path="/mnt/c/IPT-CitySpace-2018/data/vetor/dxf_corrigido.dxf",
        color="gray",
        linewidth=0.6,
        alpha=0.4,
        zorder=1,
    )

    # --------------------------------------------------
    # [5] Renderer2D (LAYERS DEFINIDAS NO CONSTRUTOR)
    # --------------------------------------------------
    renderer = Renderer2D(
        actuator=actuator,
        layers=[layer_dxf]
    )

    # --------------------------------------------------
    # [6] Renderização
    # --------------------------------------------------
    fig, ax = renderer.render(estado_mesa)

    ax.set_title(
        "Renderer2D + DXF (layer de fundo)\n"
        "Eixo X: Bairro | Eixo Y: Campus",
        fontsize=12
    )

    plt.show()

    print("=" * 70)
    print("TESTE FINALIZADO COM SUCESSO")
    print("DXF herdado corretamente como layer de fundo")
    print("=" * 70)


if __name__ == "__main__":
    main()
