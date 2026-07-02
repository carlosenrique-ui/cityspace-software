# ======================================================
# LAYER 2D — DXF COMO LINHAS DE FUNDO
# IPT-CITYSPACE
# ======================================================
#
# Esta layer respeita o contrato completo de Layer2D.
# Ela NÃO usa o grid para renderização raster, mas
# precisa recebê-lo para integração correta ao renderer.
#
# ======================================================

import geopandas as gpd
from pathlib import Path

from online.renderers.layer2d import Layer2D


class LayerDXFLines(Layer2D):

    def __init__(
        self,
        name,
        grid,
        colormap,
        dxf_path,
        layer_name="entities",
        color="gray",
        linewidth=0.6,
        alpha=0.4,
        zorder=1,
    ):
        # --------------------------------------------------
        # Inicialização formal da Layer2D
        # --------------------------------------------------
        super().__init__(
            name=name,
            grid=grid,
            colormap=colormap,
            zorder=zorder,
        )

        # --------------------------------------------------
        # Configuração DXF
        # --------------------------------------------------
        self.dxf_path = Path(dxf_path)
        self.layer_name = layer_name

        self.color = color
        self.linewidth = linewidth
        self.alpha = alpha

        self.gdf = None
        self._load_dxf()

    # --------------------------------------------------
    # Carregar DXF (executado uma única vez)
    # --------------------------------------------------
    def _load_dxf(self):

        if not self.dxf_path.exists():
            raise FileNotFoundError(
                f"DXF não encontrado: {self.dxf_path}"
            )

        gdf = gpd.read_file(self.dxf_path, layer=self.layer_name)

        # Manter somente LineStrings
        gdf = gdf[gdf.geom_type == "LineString"]

        if gdf.empty:
            raise ValueError(
                "DXF carregado, mas não contém LineStrings."
            )

        self.gdf = gdf

    # --------------------------------------------------
    # Draw: sobrescreve comportamento raster
    # --------------------------------------------------
    def draw(self, ax, **kwargs):

        if self.gdf is None:
            return

        self.gdf.plot(
            ax=ax,
            color=self.color,
            linewidth=self.linewidth,
            alpha=self.alpha,
            zorder=self.zorder,
        )
