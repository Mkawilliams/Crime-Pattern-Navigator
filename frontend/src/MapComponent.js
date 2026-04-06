import React from "react";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";

function MapComponent({ geojson, mapTheme, crimeData }) {
  // Click handler for each division
  const onEachDivision = (feature, layer) => {
    layer.on({
      click: () => {
        alert(`Clicked division: ${feature.properties.Name}`);
      }
    });
  };

  // Style divisions based on crime count
  const styleDivision = (feature) => {
    const divisionName = feature.properties.Name  // adjust based on your GeoJSON
    const crimeCount = crimeData[divisionName] || 0;

    return {
      fillColor: getColor(crimeCount),
      weight: 1,
      opacity: 1,
      color: "#333",
      fillOpacity: 0.7
    };
  };

  const getColor = (count) => {
    return count > 200 ? "#800026" :
           count > 100 ? "#BD0026" :
           count > 50  ? "#E31A1C" :
           count > 20  ? "#FC4E2A" :
           count > 10  ? "#FD8D3C" :
           count > 0   ? "#FEB24C" :
                         "#FFEDA0";
  };

  return (
    <MapContainer
      center={[25.0343, -77.3963]} // Nassau coords
      zoom={11}
      style={{ height: "100%", width: "100%" }}
      scrollWheelZoom={true}
      zoomControl={false}
    >
      <TileLayer
        url={
          mapTheme === "dark"
            ? "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            : "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        }
      />
      {geojson && (
        <GeoJSON
          data={geojson}
          style={styleDivision}
          onEachFeature={onEachDivision}
        />
      )}
    </MapContainer>
  );
}

export default MapComponent;
