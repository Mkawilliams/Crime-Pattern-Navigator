import React from "react";
import { Select, MenuItem, Checkbox, ListItemText } from "@mui/material";

// This component is used in Filters.js to render the dropdowns for years, divisions, and offences. 
// It provides a consistent UI and handles the logic for selecting/deselecting all options.

// A reusable component for checkbox dropdowns with "Select All" and "Deselect All" options
function CheckboxDropdown({ label, items, selectedItems, setSelectedItems }) {
  const handleChange = (event) => {
    const value = event.target.value;

    if (value.includes("ALL")) {
      setSelectedItems(items); // select all
    } else if (value.includes("NONE")) {
      setSelectedItems([]); // deselect all
    } else {
      setSelectedItems(value);
    }
  };
  
  // Ensure the dropdown label is always visible, even when no items are selected
  return (
    <Select
      multiple
      displayEmpty
      value={selectedItems}
      onChange={handleChange}
      renderValue={() => label}
      style={{ width: "100%", marginBottom: "8px" }}
    >
      <MenuItem value="ALL">
        <Checkbox checked={selectedItems.length === items.length} />
        <ListItemText primary="Select All" />
      </MenuItem>
      <MenuItem value="NONE">
        <Checkbox checked={selectedItems.length === 0} />
        <ListItemText primary="Deselect All" />
      </MenuItem>

      {items.map((item) => (
        <MenuItem key={item} value={item}>
          <Checkbox checked={selectedItems.indexOf(item) > -1} />
          <ListItemText primary={item} />
        </MenuItem>
      ))}
    </Select>
  );
}

export default CheckboxDropdown;