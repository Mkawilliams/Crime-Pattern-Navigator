import React from "react";
import "./App.css";

function Legend({ crimeData }) {
  return (
    <div className="legend">
      <h4>Crime Percentage</h4>
      <div className="gradient-bar"></div>
      <div className="legend-labels">
        <span>0%</span>
        <span>100%</span>
      </div>
    </div>
  );
}

export default Legend;