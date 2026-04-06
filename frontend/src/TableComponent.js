import React from "react";
import "./TableComponent.css";

function TableComponent({ rows }) {
  if (!rows || rows.length === 0) {
    return <p style={{ color: "white" }}>No data available.</p>;
  }

  return (
    <div className="table-wrapper">
      <table className="table-data">
        <thead>
          <tr>
            <th>Year</th>
            <th>Division</th>     {/* renamed from division_name */}
            <th>Crime Type</th>   {/* renamed from Offence */}
            <th>Count</th>        {/* renamed from crime_count */}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr key={idx}>
              <td>{row.Year}</td>
              <td>{row.division_name}</td>
              <td>{row.Offence}</td>
              <td>{row.crime_count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TableComponent;