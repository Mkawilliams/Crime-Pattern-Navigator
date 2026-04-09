import { useEffect } from "react";
import { useMap } from "react-leaflet";
import L from "leaflet";

function Legend() {
  const map = useMap();

  useEffect(() => {
    const legend = L.control({ position: "bottomleft" });

    legend.onAdd = () => {
      const div = L.DomUtil.create("div", "info legend");
      const grades = [0, 10, 20, 50, 100, 200];
      const colors = {
                        0: "#FFEDA0", 
                        10: "#FEB24C", 
                        20: "#FD8D3C", 
                        50: "#FC4E2A", 
                        100: "#E31A1C", 
                        200: "#BD0026", 
                        300: "#800026"
                    };

      div.style.backgroundColor = "white";
      div.style.padding = "10px";
      div.style.lineHeight = "18px";
      div.style.color = "#555";

      div.innerHTML = "<h4>Crime Count</h4>";

      for (let i = 0; i < grades.length; i++) {
        div.innerHTML +=
          '<i style="background:' + colors[i] + '; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7;"></i> ' +
          grades[i] + (grades[i + 1] ? "&ndash;" + grades[i + 1] + "<br>" : "+");
      }
      return div;
    };

    legend.addTo(map);
    return () => legend.remove(); // Cleanup on unmount
  }, [map]);

  return null;
}
export default Legend;