import React from "react";
import { MapContainer, TileLayer, GeoJSON, useMapEvents } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import Legend from "./Legend";

//Map click handler MUST be outside
function MapClickHandler({ onDivisionClick }) {
  useMapEvents({
    click: () => {
      console.log("Map clicked");
      onDivisionClick(null);
    }
  });
  return null;
}

//Map Function
function MapComponent({ geojson, mapTheme, crimeData, onDivisionClick }) {

  const getColor = (count, maxCount) => {
    const ratio = maxCount > 0 ? count / maxCount : 0;
    const hue = 60 - (60 * ratio);
    return `hsl(${hue}, 100%, 50%)`;
  };

  //Style
  const styleDivision = (feature) => {
    const divisionName = feature.properties.Name;
    const crimeCount = crimeData[divisionName] || 0;
    const maxCount = Math.max(...Object.values(crimeData));

    return {
      fillColor: getColor(crimeCount, maxCount),
      weight: 1,
      opacity: 1,
      color: "white",
      dashArray: "3",
      fillOpacity: 0.7
    };
  };

  //Division Clicks
  const onEachDivision = (feature, layer) => {
    const divisionName = feature.properties.Name;
    const crimeCount = crimeData[divisionName] || 0;

    layer.bindTooltip(`${divisionName}<br/>Crimes: ${crimeCount}`, { sticky: true });

    layer.on({
      click: (e) => {
        L.DomEvent.stopPropagation(e);
        onDivisionClick(divisionName);
      }
    });
  };

  return (
    <MapContainer
      center={[25.0343, -77.3963]}
      zoom={11}
      style={{ height: "100%", width: "100%" }}
      scrollWheelZoom={true}
      zoomControl={false}
    >
      {/* Map Click Hanler*/}
      <MapClickHandler onDivisionClick={onDivisionClick} />

      <TileLayer
        url={
          mapTheme === "dark"
            ? "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            : "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        }
      />

      {geojson && (
        <GeoJSON
          key={JSON.stringify(crimeData)}
          data={geojson}
          style={styleDivision}
          onEachFeature={onEachDivision}
        />
      )}

      <Legend crimeData={crimeData} />
    </MapContainer>
  );
}

export default MapComponent;