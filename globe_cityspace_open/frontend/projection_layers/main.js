const ROWS = 8;
const COLS = 16;
const BASE = "../../projects/ipt_north_5000/";

let matrices = {};
let manifest = null;

const table = document.getElementById("table");
const info = document.getElementById("info");
const cellMode = document.getElementById("cellMode");
const layerMode = document.getElementById("layerMode");
const bmpLink = document.getElementById("bmpLink");

function parseMatrix(text) {
  return text.trim().split(/\r?\n/).map(r => r.split(";").map(Number));
}

function pinId(row, col) {
  return col * ROWS + row + 1;
}

function cellId(row, col) {
  return `P${String(pinId(row, col)).padStart(3, "0")}`;
}

function viridis(t) {
  const stops = [
    [68, 1, 84],
    [49, 104, 142],
    [53, 183, 121],
    [253, 231, 37]
  ];
  t = Math.max(0, Math.min(1, t));
  const i = Math.min(stops.length - 2, Math.floor(t * (stops.length - 1)));
  const f = t * (stops.length - 1) - i;
  const a = stops[i], b = stops[i + 1];
  return `rgb(${Math.round(a[0] + (b[0]-a[0])*f)},${Math.round(a[1] + (b[1]-a[1])*f)},${Math.round(a[2] + (b[2]-a[2])*f)})`;
}

function range(mat) {
  const vals = mat.flat().filter(Number.isFinite);
  return [Math.min(...vals), Math.max(...vals)];
}

function render() {
  const mode = layerMode.value;
  const cellCm = cellMode.value;

  const mat =
    mode === "pin" ? matrices.pin :
    mode === "gray" ? matrices.gray :
    mode === "total" ? matrices.total :
    mode === "building" ? matrices.building :
    matrices.terrain;

  const pin = matrices.pin;
  const gray = matrices.gray;
  const [mn, mx] = range(mat);
  const denom = mx - mn || 1;

  table.innerHTML = "";
  const baseLayer = document.createElement("div");
  baseLayer.id = "baseLayer";
  table.appendChild(baseLayer);

  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const value = mat[r][c];
      const z = pin[r][c];
      const g = gray[r][c];
      const t = (value - mn) / denom;

      const cell = document.createElement("div");
      cell.className = "cell";
      cell.style.background = mode === "gray" ? `rgb(${g},${g},${g})` : viridis(t);

      const pinDiv = document.createElement("div");
      pinDiv.className = "pin";
      pinDiv.style.height = `${Math.max(2, z * 11)}px`;
      pinDiv.style.background = viridis(z / 10.0);

      const label = document.createElement("div");
      label.className = "label";
      label.innerHTML = `${cellId(r,c)}<br>${z.toFixed(1)}cm`;

      cell.title =
        `${cellId(r,c)} | pin=${z.toFixed(3)} cm | gray=${g} | ` +
        `terrain=${matrices.terrain[r][c]} | building=${matrices.building[r][c]} | total=${matrices.total[r][c]}`;

      cell.appendChild(pinDiv);
      cell.appendChild(label);
      table.appendChild(cell);
    }
  }

  bmpLink.href = `${BASE}ipt_north_5000_${cellCm}cm.bmp`;

  info.innerHTML =
    `<b>${manifest.project_name}</b><br>` +
    `Modo físico: ${cellCm}cm x ${cellCm}cm<br>` +
    `Camada: ${layerMode.options[layerMode.selectedIndex].text}<br>` +
    `Min/Max camada: ${mn.toFixed(3)} – ${mx.toFixed(3)}<br>` +
    `Pin height: 0–10 cm<br>` +
    `Gray: 0–255<br>` +
    `Escala: 1:${manifest.spatial_policy.scale}<br>` +
    `Rotação: ${manifest.spatial_policy.rotation_deg}°<br>` +
    `Norte para cima: ${manifest.spatial_policy.north_up}<br>` +
    `Fonte: IPT DTM/DSM/DXF`;
}

async function load() {
  manifest = await fetch(BASE + "manifest_ipt_north_5000.json").then(r => r.json());
  matrices.pin = parseMatrix(await fetch(BASE + "grid_pino_cm.csv").then(r => r.text()));
  matrices.gray = parseMatrix(await fetch(BASE + "grid_uint8.csv").then(r => r.text()));
  matrices.total = parseMatrix(await fetch(BASE + "grid_z_total_m.csv").then(r => r.text()));
  matrices.terrain = parseMatrix(await fetch(BASE + "grid_terrain_m.csv").then(r => r.text()));
  matrices.building = parseMatrix(await fetch(BASE + "grid_building_m.csv").then(r => r.text()));
  render();
}

document.getElementById("btnTop").onclick = () => {
  table.classList.remove("oblique");
  table.classList.add("top");
};

document.getElementById("btnOblique").onclick = () => {
  table.classList.remove("top");
  table.classList.add("oblique");
};

cellMode.onchange = render;
layerMode.onchange = render;

load().catch(err => {
  console.error(err);
  info.innerHTML = "Erro ao carregar IPT Projection Layers.";
});
