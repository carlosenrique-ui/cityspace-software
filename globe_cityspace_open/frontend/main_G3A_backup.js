const TABLE_COLS = 16;
const TABLE_ROWS = 8;
const CELL_CM = 2;

const osm = new Cesium.UrlTemplateImageryProvider({
  url: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
  maximumLevel: 19,
  credit: "© OpenStreetMap contributors"
});

const viewer = new Cesium.Viewer("cesiumContainer", {
  animation: false,
  timeline: false,
  geocoder: false,
  homeButton: true,
  sceneModePicker: true,
  baseLayerPicker: false,
  navigationHelpButton: false,
  infoBox: false,
  selectionIndicator: false,
  imageryProvider: osm,
  terrainProvider: new Cesium.EllipsoidTerrainProvider()
});

viewer.imageryLayers.removeAll();
viewer.imageryLayers.addImageryProvider(osm);

const locations = {
  sjc: { name: "São José dos Campos", lat: -23.1890, lon: -45.8870, height: 18000 },
  sao_paulo: { name: "São Paulo", lat: -23.5505, lon: -46.6333, height: 25000 },
  ipt: { name: "IPT / Cidade Universitária", lat: -23.5614, lon: -46.7350, height: 6000 },
  santos: { name: "Santos", lat: -23.9608, lon: -46.3336, height: 18000 },
  sorocaba: { name: "Sorocaba", lat: -23.5015, lon: -47.4526, height: 18000 }
};

let currentPoint = {
  name: locations.sjc.name,
  lat: locations.sjc.lat,
  lon: locations.sjc.lon
};

let markerEntity = null;
let areaEntity = null;

function setMarker(name, lat, lon) {
  if (markerEntity) viewer.entities.remove(markerEntity);

  markerEntity = viewer.entities.add({
    name: name,
    position: Cesium.Cartesian3.fromDegrees(lon, lat, 0),
    point: {
      pixelSize: 14,
      color: Cesium.Color.YELLOW,
      outlineColor: Cesium.Color.BLACK,
      outlineWidth: 2
    },
    label: {
      text: name,
      font: "16px sans-serif",
      fillColor: Cesium.Color.WHITE,
      outlineColor: Cesium.Color.BLACK,
      outlineWidth: 3,
      style: Cesium.LabelStyle.FILL_AND_OUTLINE,
      verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
      pixelOffset: new Cesium.Cartesian2(0, -18)
    }
  });
}

function flyTo(lat, lon, height, name) {
  currentPoint = { name, lat, lon };

  setMarker(name, lat, lon);

  document.getElementById("latInput").value = lat.toFixed(6);
  document.getElementById("lonInput").value = lon.toFixed(6);

  viewer.camera.flyTo({
    destination: Cesium.Cartesian3.fromDegrees(lon, lat, height),
    orientation: {
      heading: Cesium.Math.toRadians(0),
      pitch: Cesium.Math.toRadians(-50),
      roll: 0
    },
    duration: 2.0
  });
}

function metersToDegrees(lat, widthM, heightM) {
  const metersPerDegreeLat = 111320;
  const metersPerDegreeLon = 111320 * Math.cos(Cesium.Math.toRadians(lat));

  return {
    dLat: (heightM / 2) / metersPerDegreeLat,
    dLon: (widthM / 2) / metersPerDegreeLon
  };
}

function computeRealDimensions(scale) {
  const tableWidthCm = TABLE_COLS * CELL_CM;
  const tableHeightCm = TABLE_ROWS * CELL_CM;

  const widthM = (tableWidthCm / 100) * scale;
  const heightM = (tableHeightCm / 100) * scale;

  return {
    tableWidthCm,
    tableHeightCm,
    widthM,
    heightM
  };
}

function createScaledArea() {
  const scale = parseInt(document.getElementById("scaleSelect").value, 10);
  const dims = computeRealDimensions(scale);
  const delta = metersToDegrees(currentPoint.lat, dims.widthM, dims.heightM);

  const west = currentPoint.lon - delta.dLon;
  const east = currentPoint.lon + delta.dLon;
  const south = currentPoint.lat - delta.dLat;
  const north = currentPoint.lat + delta.dLat;

  if (areaEntity) viewer.entities.remove(areaEntity);

  areaEntity = viewer.entities.add({
    name: `Área CitySpace 1:${scale}`,
    rectangle: {
      coordinates: Cesium.Rectangle.fromDegrees(west, south, east, north),
      material: Cesium.Color.YELLOW.withAlpha(0.18),
      outline: true,
      outlineColor: Cesium.Color.YELLOW,
      outlineWidth: 3
    }
  });

  viewer.camera.flyTo({
    destination: Cesium.Rectangle.fromDegrees(west, south, east, north),
    duration: 1.5
  });

  document.getElementById("areaInfo").innerHTML = `
    Centro: ${currentPoint.lat.toFixed(6)}, ${currentPoint.lon.toFixed(6)}<br>
    Escala: 1:${scale}<br>
    Mesa física: ${dims.tableWidthCm} cm x ${dims.tableHeightCm} cm<br>
    Grid: ${TABLE_COLS} x ${TABLE_ROWS} = ${TABLE_COLS * TABLE_ROWS} pinos<br>
    Área real: ${dims.widthM.toFixed(1)} m x ${dims.heightM.toFixed(1)} m<br>
    Célula real: ${(dims.widthM / TABLE_COLS).toFixed(1)} m x ${(dims.heightM / TABLE_ROWS).toFixed(1)} m
  `;
}

document.getElementById("flyCity").addEventListener("click", () => {
  const key = document.getElementById("citySelect").value;
  const loc = locations[key];
  flyTo(loc.lat, loc.lon, loc.height, loc.name);
});

document.getElementById("flyLatLon").addEventListener("click", () => {
  const lat = parseFloat(document.getElementById("latInput").value);
  const lon = parseFloat(document.getElementById("lonInput").value);

  if (Number.isNaN(lat) || Number.isNaN(lon)) {
    alert("Informe latitude e longitude válidas.");
    return;
  }

  flyTo(lat, lon, 10000, `Lat/Lon: ${lat.toFixed(6)}, ${lon.toFixed(6)}`);
});

document.getElementById("createArea").addEventListener("click", createScaledArea);

flyTo(locations.sjc.lat, locations.sjc.lon, locations.sjc.height, locations.sjc.name);
