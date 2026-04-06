import React,  { useEffect, useState } from "react";
import "./App.css";
import MapComponent from "./MapComponent";
import TableComponent from "./TableComponent";
import Filters from "./Filters";

function App() {
  const [years, setYears] = useState([]);
  const [divisions, setDivisions] = useState([]);
  const [offences, setOffences] = useState([]);
  const [mapData, setMapData] = useState(null);
  const [tableData, setTableData] = useState([]);
  const [selectedYears, setSelectedYears] = useState([]);
  const [selectedDivisions, setSelectedDivisions] = useState([]);
  const [selectedOffences, setSelectedOffences] = useState([]);
  const [mapTheme, setMapTheme] = useState("light");

  // Load filter options
useEffect(() => {
  fetch("http://localhost:8000/filters")
    .then(res => res.json())
    .then(data => {
      setYears(data.years || []);
      setDivisions(data.divisions || []);
      setOffences(data.offences || []);
      // set sensible defaults
      setSelectedYears(data.years || []);
      setSelectedDivisions(data.divisions || []);
      setSelectedOffences(data.offences || []);
    });
}, []);

// Load map + table when filters change
useEffect(() => {
  if (selectedYears.length && selectedDivisions.length && selectedOffences.length) {
    const yearParams = selectedYears.map(y => `years=${y}`).join("&");
    const divisionParams = selectedDivisions.map(d => `divisions=${encodeURIComponent(d)}`).join("&");
    const offenceParams = selectedOffences.map(o => `offences=${encodeURIComponent(o)}`).join("&");

    fetch(`http://localhost:8000/map-data?${yearParams}&${divisionParams}&${offenceParams}`)
      .then(res => res.json())
      .then(data => setMapData(data));

    fetch(`http://localhost:8000/table-data?${yearParams}&${divisionParams}&${offenceParams}`)
      .then(res => res.json())
      .then(data => setTableData(data));
  }
}, [selectedYears, selectedDivisions, selectedOffences]);

//Derive crimeData from tableData here, BEFORE return
const crimeData = Array.isArray(tableData)
  ? tableData.reduce((acc, row) => {
      const divisionName = row.division_name?.trim();
      acc[divisionName] = (acc[divisionName] || 0) + row.crime_count;
      return acc;
    }, {})
  : {};


  return (
    <div className="app-container">
      {/* Disclaimer banner */}
      <div className="disclaimer">
        Disclaimer: This map is for research and educational purposes only. It is not an official government product. Data is sourced from public RBPF reports.
      </div>

      {/* Title overlay */}
      <div className="title-overlay">
        Bahamas Crime Intelligence Map
      </div>

      {/* Filters overlay */}
      <Filters
        years={years}
        divisions={divisions}
        offences={offences}
        selectedYears={selectedYears}
        setSelectedYears={setSelectedYears}
        selectedDivisions={selectedDivisions}
        setSelectedDivisions={setSelectedDivisions}
        selectedOffences={selectedOffences}
        setSelectedOffences={setSelectedOffences}
        mapTheme={mapTheme}
        setMapTheme={setMapTheme}
      />

      {/* Map wrapper */}
      <div className="map-wrapper">
        <MapComponent geojson={mapData} mapTheme={mapTheme} crimeData={crimeData} />
      </div>

      {/* Summary table overlay */}
      <div className="table-wrapper">
        <div className="summary-table">
          <TableComponent rows={tableData} />
        </div>
        <div>
          ©️ 2026 Matthew Williams. All rights reserved.
        </div>
      </div>
    </div>
  );
}

export default App;