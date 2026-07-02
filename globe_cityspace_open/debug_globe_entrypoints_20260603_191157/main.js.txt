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
  navigationHelpButton: true,
  infoBox: false,
  selectionIndicator: false,
  imageryProvider: osm,
  terrainProvider: new Cesium.EllipsoidTerrainProvider()
});

viewer.imageryLayers.removeAll();
viewer.imageryLayers.addImageryProvider(osm);

viewer.scene.screenSpaceCameraController.enableRotate = true;
viewer.scene.screenSpaceCameraController.enableTranslate = true;
viewer.scene.screenSpaceCameraController.enableZoom = true;
viewer.scene.screenSpaceCameraController.enableTilt = true;
viewer.scene.screenSpaceCameraController.enableLook = true;

const cities = {
  sjc: {
    name: "São José dos Campos",
    centerLat: -23.1890,
    centerLon: -45.8870,
    west: -46.02,
    south: -23.32,
    east: -45.75,
    north: -23.05,
    cameraHeight: 22000
  },
  sao_paulo: {
    name: "São Paulo",
    centerLat: -23.5505,
    centerLon: -46.6333,
    west: -46.83,
    south: -23.72,
    east: -46.45,
    north: -23.42,
    cameraHeight: 38000
  },
  ipt: {
    name: "IPT - Campus Principal",
    centerLat: -23.5567944,
    centerLon: -46.7373288,
    west: -46.7470,
    south: -23.5645,
    east: -46.7280,
    north: -23.5500,
    cameraHeight: 2500
  },
  santos: {
    name: "Santos",
    centerLat: -23.9608,
    centerLon: -46.3336,
    west: -46.40,
    south: -24.02,
    east: -46.25,
    north: -23.90,
    cameraHeight: 15000
  },
  sorocaba: {
    name: "Sorocaba",
    centerLat: -23.5015,
    centerLon: -47.4526,
    west: -47.58,
    south: -23.58,
    east: -47.33,
    north: -23.42,
    cameraHeight: 20000
  }
};

let activeCityKey = "sjc";

let currentPoint = {
  name: cities.sjc.name,
  lat: cities.sjc.centerLat,
  lon: cities.sjc.centerLon
};

let markerEntity = null;
let areaEntity = null;
let gridEntities = [];
let currentGrid = null;
let pickPointMode = false;

function getActiveCity() {
  return cities[activeCityKey];
}

function clearGrid() {
  gridEntities.forEach(e => viewer.entities.remove(e));
  gridEntities = [];
}

function setMarker(name, lat, lon) {
  if (markerEntity) {
    viewer.entities.remove(markerEntity);
  }

  markerEntity = viewer.entities.add({
    position: Cesium.Cartesian3.fromDegrees(lon, lat),
    point: {
      pixelSize: 14,
      color: Cesium.Color.YELLOW,
      outlineColor: Cesium.Color.BLACK,
      outlineWidth: 2,
      disableDepthTestDistance: Number.POSITIVE_INFINITY
    },
    label: {
      text: name,
      font: "16px sans-serif",
      fillColor: Cesium.Color.WHITE,
      outlineColor: Cesium.Color.BLACK,
      outlineWidth: 3,
      style: Cesium.LabelStyle.FILL_AND_OUTLINE,
      verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
      pixelOffset: new Cesium.Cartesian2(0, -18),
      disableDepthTestDistance: Number.POSITIVE_INFINITY
    }
  });
}

function setReferencePoint(name, lat, lon) {
  currentPoint = { name, lat, lon };
  setMarker(name, lat, lon);

  document.getElementById("coordInfo").innerHTML = `
    ${name}<br>
    Lat: ${lat.toFixed(7)}<br>
    Lon: ${lon.toFixed(7)}
  `;
}

function openCity() {
  activeCityKey = document.getElementById("citySelect").value;
  const city = getActiveCity();

  setReferencePoint(
    `${city.name} - Centroide`,
    city.centerLat,
    city.centerLon
  );

  const rectangle = Cesium.Rectangle.fromDegrees(
    city.west,
    city.south,
    city.east,
    city.north
  );

  viewer.camera.flyTo({
    destination: rectangle,
    duration: 2.0
  });

  document.getElementById("areaInfo").innerHTML =
    "Cidade aberta. Navegue como no Google Earth, escolha um ponto e gere a área.";
}

function viewTop() {
  const city = getActiveCity();

  viewer.camera.flyTo({
    destination: Cesium.Cartesian3.fromDegrees(
      currentPoint.lon,
      currentPoint.lat,
      city.cameraHeight
    ),
    orientation: {
      heading: 0,
      pitch: Cesium.Math.toRadians(-90),
      roll: 0
    },
    duration: 1.5
  });
}

function viewOblique() {
  const city = getActiveCity();

  viewer.camera.flyTo({
    destination: Cesium.Cartesian3.fromDegrees(
      currentPoint.lon,
      currentPoint.lat,
      city.cameraHeight
    ),
    orientation: {
      heading: Cesium.Math.toRadians(25),
      pitch: Cesium.Math.toRadians(-55),
      roll: 0
    },
    duration: 1.5
  });
}

function viewNorth() {
  const position = viewer.camera.positionCartographic;

  viewer.camera.flyTo({
    destination: viewer.camera.position,
    orientation: {
      heading: 0,
      pitch: viewer.camera.pitch,
      roll: 0
    },
    duration: 1.0
  });
}

function metersToDegrees(lat, widthM, heightM) {
  const metersPerDegreeLat = 111320;
  const metersPerDegreeLon =
    111320 * Math.cos(Cesium.Math.toRadians(lat));

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

function drawGrid(west, south, east, north) {
  clearGrid();

  const dLon = (east - west) / TABLE_COLS;
  const dLat = (north - south) / TABLE_ROWS;

  for (let c = 0; c <= TABLE_COLS; c++) {
    const lon = west + c * dLon;

    gridEntities.push(
      viewer.entities.add({
        polyline: {
          positions: Cesium.Cartesian3.fromDegreesArray([
            lon, south,
            lon, north
          ]),
          width: 1,
          material: Cesium.Color.RED
        }
      })
    );
  }

  for (let r = 0; r <= TABLE_ROWS; r++) {
    const lat = south + r * dLat;

    gridEntities.push(
      viewer.entities.add({
        polyline: {
          positions: Cesium.Cartesian3.fromDegreesArray([
            west, lat,
            east, lat
          ]),
          width: 1,
          material: Cesium.Color.RED
        }
      })
    );
  }

  for (let r = 0; r < TABLE_ROWS; r++) {
    for (let c = 0; c < TABLE_COLS; c++) {
      const cellNumber = r * TABLE_COLS + c + 1;
      const cellId = "P" + String(cellNumber).padStart(3, "0");

      const centerLon = west + (c + 0.5) * dLon;
      const centerLat = north - (r + 0.5) * dLat;

      gridEntities.push(
        viewer.entities.add({
          position: Cesium.Cartesian3.fromDegrees(centerLon, centerLat, 0),
          label: {
            text: cellId,
            font: "11px sans-serif",
            fillColor: Cesium.Color.WHITE,
            outlineColor: Cesium.Color.BLACK,
            outlineWidth: 3,
            style: Cesium.LabelStyle.FILL_AND_OUTLINE,
            horizontalOrigin: Cesium.HorizontalOrigin.CENTER,
            verticalOrigin: Cesium.VerticalOrigin.CENTER,
            disableDepthTestDistance: Number.POSITIVE_INFINITY
          }
        })
      );
    }
  }
}

function createScaledArea() {
  const scale = parseInt(
    document.getElementById("scaleSelect").value,
    10
  );

  const dims = computeRealDimensions(scale);

  const delta = metersToDegrees(
    currentPoint.lat,
    dims.widthM,
    dims.heightM
  );

  const west = currentPoint.lon - delta.dLon;
  const east = currentPoint.lon + delta.dLon;
  const south = currentPoint.lat - delta.dLat;
  const north = currentPoint.lat + delta.dLat;

  if (areaEntity) {
    viewer.entities.remove(areaEntity);
  }

  areaEntity = viewer.entities.add({
    rectangle: {
      coordinates: Cesium.Rectangle.fromDegrees(west, south, east, north),
      material: Cesium.Color.YELLOW.withAlpha(0.15),
      outline: true,
      outlineColor: Cesium.Color.YELLOW
    }
  });

  currentGrid = {
    west,
    south,
    east,
    north,
    scale,
    widthM: dims.widthM,
    heightM: dims.heightM,
    centerLat: currentPoint.lat,
    centerLon: currentPoint.lon
  };

  drawGrid(west, south, east, north);


  viewer.camera.flyTo({
    destination: Cesium.Rectangle.fromDegrees(west, south, east, north),
    duration: 1.5
  });

  document.getElementById("areaInfo").innerHTML = `
    Centro: ${currentPoint.lat.toFixed(7)}, ${currentPoint.lon.toFixed(7)}<br>
    Escala: 1:${scale}<br>
    Mesa: ${dims.tableWidthCm} cm x ${dims.tableHeightCm} cm<br>
    Grid: ${TABLE_COLS} x ${TABLE_ROWS} = ${TABLE_COLS * TABLE_ROWS} pinos<br>
    Área real: ${dims.widthM.toFixed(1)} m x ${dims.heightM.toFixed(1)} m<br>
    Célula: ${(dims.widthM / TABLE_COLS).toFixed(1)} m x ${(dims.heightM / TABLE_ROWS).toFixed(1)} m
  `;
}

function exportGridJSON() {
  if (!currentGrid) {
    alert("Crie uma área antes de exportar.");
    return;
  }

  const dLon = (currentGrid.east - currentGrid.west) / TABLE_COLS;
  const dLat = (currentGrid.north - currentGrid.south) / TABLE_ROWS;

  const cells = [];

  for (let r = 0; r < TABLE_ROWS; r++) {
    for (let c = 0; c < TABLE_COLS; c++) {
      const cellNumber = r * TABLE_COLS + c + 1;
      const cellId = "P" + String(cellNumber).padStart(3, "0");

      const centerLon = currentGrid.west + (c + 0.5) * dLon;
      const centerLat = currentGrid.north - (r + 0.5) * dLat;

      cells.push({
        cell_id: cellId,
        row: r + 1,
        col: c + 1,
        centroid_lat: centerLat,
        centroid_lon: centerLon
      });
    }
  }

  const payload = {
    application: "Globe-CitySpace",
    contract_type: "spatial_grid",
    grid_rows: TABLE_ROWS,
    grid_cols: TABLE_COLS,
    cell_count: TABLE_ROWS * TABLE_COLS,
    scale: currentGrid.scale,
    width_m: currentGrid.widthM,
    height_m: currentGrid.heightM,
    center_lat: currentGrid.centerLat,
    center_lon: currentGrid.centerLon,
    bbox: {
      west: currentGrid.west,
      south: currentGrid.south,
      east: currentGrid.east,
      north: currentGrid.north
    },
    cells: cells
  };

  const blob = new Blob(
    [JSON.stringify(payload, null, 2)],
    { type: "application/json" }
  );

  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "globe_cityspace_grid_16x8.json";
  a.click();
  URL.revokeObjectURL(url);
}

const clickHandler = new Cesium.ScreenSpaceEventHandler(
  viewer.scene.canvas
);

clickHandler.setInputAction(
  function(click) {
    if (!pickPointMode) {
      return;
    }

    const cartesian = viewer.camera.pickEllipsoid(
      click.position,
      viewer.scene.globe.ellipsoid
    );

    if (!cartesian) {
      alert("Não foi possível capturar o ponto clicado.");
      return;
    }

    const cartographic =
      Cesium.Cartographic.fromCartesian(cartesian);

    const lon =
      Cesium.Math.toDegrees(cartographic.longitude);

    const lat =
      Cesium.Math.toDegrees(cartographic.latitude);

    pickPointMode = false;

    document.getElementById("enablePickPoint").innerText =
      "Escolher ponto";

    setReferencePoint(
      "Ponto de Referência",
      lat,
      lon
    );
  },
  Cesium.ScreenSpaceEventType.LEFT_CLICK
);

document.getElementById("openCity").addEventListener("click", openCity);
document.getElementById("viewTop").addEventListener("click", viewTop);
document.getElementById("viewOblique").addEventListener("click", viewOblique);
document.getElementById("viewNorth").addEventListener("click", viewNorth);
document.getElementById("createArea").addEventListener("click", createScaledArea);

document.getElementById("exportGrid").addEventListener("click", exportGridJSON);


function sanitizeProjectName(name) {
  return String(name)
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-zA-Z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "")
    .toLowerCase();
}

function generateSpatialProjectJSON() {
  if (!currentGrid) {
    alert("Crie uma Área CitySpace antes de gerar o Spatial Project.");
    return;
  }

  const city = getActiveCity();
  const scale = currentGrid.scale;
  const cellSizeCm = CELL_CM;

  const projectName = city.name + " - " + currentPoint.name + " - 1:" + scale;

  const payload = {
    contract_type: "spatial_project",
    contract_version: "G5.4",
    application: "Globe-CitySpace",
    created_at_local: new Date().toISOString(),

    project_name: projectName,

    source: {
      city_key: activeCityKey,
      city_name: city.name,
      reference_point_name: currentPoint.name
    },

    center: {
      lat: currentGrid.centerLat,
      lon: currentGrid.centerLon
    },

    scale: scale,

    grid: {
      rows: TABLE_ROWS,
      cols: TABLE_COLS,
      cell_count: TABLE_ROWS * TABLE_COLS,
      cell_size_cm: cellSizeCm,
      table_width_cm: TABLE_COLS * cellSizeCm,
      table_height_cm: TABLE_ROWS * cellSizeCm
    },

    bbox: {
      west: currentGrid.west,
      south: currentGrid.south,
      east: currentGrid.east,
      north: currentGrid.north
    },

    spatial_layout: {
      layout_file: "contracts/spatial_layout_16x8.json",
      numbering_mode: "ipt_column_zigzag",
      p001: "upper_left",
      p008: "lower_left",
      p121: "lower_right",
      p128: "upper_right"
    },

    integration_policy: {
      globe_cityspace_role: "producer_of_spatial_contract",
      ipt_cityspace_role: "physical_runtime_consumer",
      direct_import_from_legacy_online_offline: false
    },

    next_pipeline: {
      target: "IPT-CitySpace Runtime",
      expected_consumers: [
        "Height Provider",
        "Physical Table",
        "Projection Mapping",
        "Actuator Plan",
        "Mesa Virtual",
        "Mesa Real"
      ]
    }
  };

  const blob = new Blob(
    [JSON.stringify(payload, null, 2)],
    { type: "application/json" }
  );

  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");

  a.href = url;
  a.download = sanitizeProjectName(projectName) + "_spatial_project_G54.json";
  a.click();

  URL.revokeObjectURL(url);

  document.getElementById("areaInfo").innerHTML +=
    "<br><br>Spatial Project G5.4 gerado.<br>Arquivo JSON exportado para download.";
}

document
  .getElementById("exportSpatialProject")
  .addEventListener("click", generateSpatialProjectJSON);

document.getElementById("enablePickPoint").addEventListener("click", () => {
  pickPointMode = !pickPointMode;

  document.getElementById("enablePickPoint").innerText =
    pickPointMode ? "Clique no mapa..." : "Escolher ponto";

  document.getElementById("coordInfo").innerHTML =
    pickPointMode
      ? "Modo ativo: clique no mapa para definir o ponto de referência."
      : "Seleção cancelada.";
});

openCity();

const mouseMoveHandler = new Cesium.ScreenSpaceEventHandler(
  viewer.scene.canvas
);

mouseMoveHandler.setInputAction(
  function(movement) {
    const cartesian = viewer.camera.pickEllipsoid(
      movement.endPosition,
      viewer.scene.globe.ellipsoid
    );

    if (!cartesian) {
      document.getElementById("cursorInfo").innerHTML =
        "Lat/Lon: --";
      return;
    }

    const cartographic =
      Cesium.Cartographic.fromCartesian(cartesian);

    const lon =
      Cesium.Math.toDegrees(cartographic.longitude);

    const lat =
      Cesium.Math.toDegrees(cartographic.latitude);

    document.getElementById("cursorInfo").innerHTML =
      `Lat: ${lat.toFixed(7)}<br>Lon: ${lon.toFixed(7)}`;
  },
  Cesium.ScreenSpaceEventType.MOUSE_MOVE
);

function clearAreaAndGrid() {
  if (areaEntity) {
    viewer.entities.remove(areaEntity);
    areaEntity = null;
  }

  clearGrid();
  currentGrid = null;

  document.getElementById("areaInfo").innerHTML =
    "Área e Grid limpos. Escolha um ponto e gere uma nova Área CitySpace.";
}

document
.getElementById("clearArea")
.addEventListener(
  "click",
  clearAreaAndGrid
);
