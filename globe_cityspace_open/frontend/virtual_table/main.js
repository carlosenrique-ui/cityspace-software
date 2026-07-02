const ROWS = 8;
const COLS = 16;

const table = document.getElementById("table");
const info = document.getElementById("info");

function parseMatrix(text) {
  return text
    .trim()
    .split(/\r?\n/)
    .map(row => row.split(";").map(Number));
}

function grayToColor(g) {
  return `rgb(${g}, ${g}, ${g})`;
}

function cellId(row, col) {
  const pinId = col * ROWS + row + 1;
  return `P${String(pinId).padStart(3, "0")}`;
}

async function loadData() {
  const pinText = await fetch("/projects/ipt_north_5000/grid_pino_cm.csv").then(r => r.text());
  const grayText = await fetch("/projects/ipt_north_5000/grid_uint8.csv").then(r => r.text());
  const manifest = await fetch("/projects/ipt_north_5000/manifest_ipt_north_5000.json").then(r => r.json());

  const pin = parseMatrix(pinText);
  const gray = parseMatrix(grayText);

  table.innerHTML = "";

  let minPin = Infinity;
  let maxPin = -Infinity;

  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const z = pin[r][c];
      const g = gray[r][c];

      minPin = Math.min(minPin, z);
      maxPin = Math.max(maxPin, z);

      const cell = document.createElement("div");
      cell.className = "cell";
      cell.title = `${cellId(r, c)} | ${z.toFixed(2)} cm | gray ${g}`;

      const pinDiv = document.createElement("div");
      pinDiv.className = "pin";
      pinDiv.style.height = `${Math.max(2, z * 9)}px`;
      pinDiv.style.background = grayToColor(g);

      const label = document.createElement("div");
      label.className = "label";
      label.innerHTML = `${cellId(r, c)}<br>${z.toFixed(1)}cm`;

      cell.appendChild(pinDiv);
      cell.appendChild(label);
      table.appendChild(cell);
    }
  }

  info.innerHTML =
    `<b>${manifest.project_name}</b><br>` +
    `Escala: 1:${manifest.spatial_policy.scale}<br>` +
    `Grid: ${ROWS} x ${COLS}<br>` +
    `Pin min/max: ${minPin.toFixed(2)}–${maxPin.toFixed(2)} cm<br>` +
    `Rotação: ${manifest.spatial_policy.rotation_deg}°<br>` +
    `Norte para cima: ${manifest.spatial_policy.north_up}<br>` +
    `Fonte: IPT DTM/DSM/DXF`;
}

document.getElementById("viewTop").onclick = () => {
  table.classList.remove("oblique");
  table.classList.add("top");
};

document.getElementById("viewOblique").onclick = () => {
  table.classList.remove("top");
  table.classList.add("oblique");
};

loadData().catch(err => {
  console.error(err);
  info.innerHTML = "Erro ao carregar dados IPT North 1:5000.";
});
