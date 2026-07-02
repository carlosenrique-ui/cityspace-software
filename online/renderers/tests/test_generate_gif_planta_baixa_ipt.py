# ======================================================
# TESTE VISUAL — GIF TEMPORAL CANÔNICO
# Planta Baixa IPT
# ======================================================
#
# OBJETIVO:
# - Testar visualização humana e para projeção
# - Ajustar contraste, alpha, colormap e ritmo
# - Usar dados reais (metros)
# - Manter compatibilidade com mesa virtual e mesa real
#
# ESTE ARQUIVO É PARA TESTE / AJUSTE VISUAL
# O MOTOR NÃO DEVE SER ALTERADO AQUI
#
# ======================================================

from online.renderers.generate_gif_planta_baixa_ipt import generate_gif


def main():

    print("=" * 70)
    print("TESTE — GIF TEMPORAL | Planta Baixa IPT")
    print("=" * 70)

    # --------------------------------------------------
    # PARÂMETROS VISUAIS (AJUSTE APENAS AQUI)
    # --------------------------------------------------

    # Tempo / ritmo
    N_FRAMES = 40          # mais frames = transição mais suave
    GIF_FPS = 5            # mais lento para projeção

    # Altura (metros reais)
    MAX_HEIGHT_M = 30.0

    # Planta Baixa (DXF)
    DXF_ALPHA = 0.25       # transparência da planta (0.15–0.35)

    # --------------------------------------------------
    # EXECUÇÃO DO TESTE
    # --------------------------------------------------
    gif_path = generate_gif(
        n_frames=N_FRAMES,
        max_height_m=MAX_HEIGHT_M,
        gif_fps=GIF_FPS,
        dxf_alpha=DXF_ALPHA
    )

    print("=" * 70)
    print("GIF GERADO COM SUCESSO")
    print("Arquivo:", gif_path)
    print("=" * 70)


if __name__ == "__main__":
    main()
