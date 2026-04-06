import React from "react";
import CheckboxDropdown from "./CheckboxDropdown";

function Filters({
  years, divisions, offences,
  selectedYears, setSelectedYears,
  selectedDivisions, setSelectedDivisions,
  selectedOffences, setSelectedOffences,
  mapTheme, setMapTheme
}) {
  return (
    /* Filters panel */
   <div className="filters">

    {/* Year filter */}
      <CheckboxDropdown
        label="Years"
        items={years}
        selectedItems={selectedYears}
        setSelectedItems={setSelectedYears}
      />

    {/* Division filter */}
      <CheckboxDropdown
        label="Divisions"
        items={divisions}
        selectedItems={selectedDivisions}
        setSelectedItems={setSelectedDivisions}
      />

    {/* Offence filter */}
      <CheckboxDropdown
        label="Offences"
        items={offences}
        selectedItems={selectedOffences}
        setSelectedItems={setSelectedOffences}
      />
    

      {/* Map theme toggle button */}
      <label className="switch">
        <input
          type="checkbox"
          checked={mapTheme === "dark"}
          onChange={() => setMapTheme(mapTheme === "light" ? "dark" : "light")}
        />
        <span className="slider round"></span>
      </label>
      <span style={{ marginLeft: "8px", color: "white" }}>
        {mapTheme === "dark" ? "Dark Mode" : "Light Mode"}
      </span>
    </div>
  );
}

export default Filters;