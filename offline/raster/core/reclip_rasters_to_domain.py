import rasterio
from rasterio.mask import mask
import fiona
from shapely.geometry import shape
from pathlib import Path

# ==========================================================
# IPT-CitySpace – RECLIP CIENTÍFICO DEFINITIVO
# Recorte usando domínio 1:2 validado
# ==========================================================

# Estamos dentro de: offline/raster/core/
# Precisamos subir 3 níveis até ipt-cityspace-engine
BASE = Path(__file__).resolve().parents[3]

# RASTERS ROTACIONADOS VALIDADOS
DTM_ROT = BASE / "offline/data/processed/dtm/IPT_2018_DTM_ROT.tif"
DSM_ROT = BASE / "offline/data/processed/dsm/IPT_2018_DSM_ROT.tif"

# DOMÍNIO VALIDADO
DOMAIN_PATH = BASE / "offline/products/scientific/domain_rect_1x2.gpkg"
DOMAIN_LAYER = "domain_rect_1x2"

# SAÍDAS
DTM_OUT = BASE / "offline/data/processed/dtm/IPT_2018_DTM_DOMAIN.tif"
DSM_OUT = BASE / "offline/data/processed/dsm/IPT_2018_DSM_DOMAIN.tif"


def clip_raster(input_path, output_path, domain_geom):

    print(f"\n[CLIP] {input_path.name}")

    with rasterio.open(input_path) as src:

        out_image, out_transform = mask(
            src,
            [domain_geom],
            crop=True
        )

        out_meta = src.meta.copy()
        out_meta.update({
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })

        with rasterio.open(output_path, "w", **out_meta) as dst:
            dst.write(out_image)

    print(f"[OK] Gerado: {output_path.name}")


def main():

    print("\n=================================================")
    print("IPT-CitySpace – RECLIP DEFINITIVO")
    print("=================================================\n")

    print("[1/4] Verificando arquivos...")

    for p in [DTM_ROT, DSM_ROT, DOMAIN_PATH]:
        print("→", p)
        if not p.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {p}")

    print("\n[2/4] Lendo domínio validado...")

    with fiona.open(DOMAIN_PATH, layer=DOMAIN_LAYER) as src:
        feature = next(iter(src))
        domain_geom = shape(feature["geometry"])

    print("Domínio carregado com sucesso.")

    print("\n[3/4] Executando recorte científico...")

    clip_raster(DTM_ROT, DTM_OUT, domain_geom)
    clip_raster(DSM_ROT, DSM_OUT, domain_geom)

    print("\n[4/4] Processo concluído.")
    print("✔ Rasters científicos recortados com sucesso.\n")


if __name__ == "__main__":
    main()