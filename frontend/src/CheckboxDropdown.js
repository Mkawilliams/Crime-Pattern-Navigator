import React from "react";
import { Select, MenuItem, Checkbox, ListItemText } from "@mui/material";

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