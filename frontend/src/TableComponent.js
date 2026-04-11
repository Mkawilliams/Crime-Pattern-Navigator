import React from "react";
import "./App.css";

function TableComponent({ rows }) {
  if (!rows || rows.length === 0) {
    return <p style={{ color: "white" }}>No data available.</p>;
  }

  //Calculate total count for footer
  const totalCount = rows.reduce((sum, row) => sum + row.crime_count, 0);

  return (
    <div className="table-wrapper">
      <table className="table-data">
        <thead>
          <tr>
            <th>Year</th>
            <th>Division</th>     
            <th>Crime Type</th>   
            <th>Count</th>        
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
        <tfoot>
          <tr>
            <td colSpan="3" style={{ fontWeight: "bold", textAlign: "right" }}>
              Total
            </td>
            <td style={{ fontWeight: "bold" }}>{totalCount}</td>
          </tr>
        </tfoot>
      </table>
    </div>
  );
}

export default TableComponent;