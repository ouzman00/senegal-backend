import { useEffect, useState } from "react";
import { toLonLat } from "ol/proj";

/**
 * Convertit degrés décimaux → DMS
 */
function toDMS(deg, isLon = true) {
  const absolute = Math.abs(deg);
  const degrees = Math.floor(absolute);
  const minutesNotTruncated = (absolute - degrees) * 60;
  const minutes = Math.floor(minutesNotTruncated);
  const seconds = Math.floor((minutesNotTruncated - minutes) * 60);

  const direction = isLon
    ? deg >= 0 ? "E" : "O"
    : deg >= 0 ? "N" : "S";

  return `${degrees}°${minutes}′${seconds}″ ${direction}`;
}

export default function Coordonnees({ map }) {
  const [coords, setCoords] = useState(null);

  useEffect(() => {
    if (!map) return;

    const handler = (evt) => {
      const [lon, lat] = toLonLat(evt.coordinate);
      setCoords({
        lon: toDMS(lon, true),
        lat: toDMS(lat, false),
      });
    };

    map.on("pointermove", handler);

    return () => {
      map.un("pointermove", handler);
    };
  }, [map]);

  if (!coords) return null;

  return (
  <div
    className="absolute bottom-4 left-1/2 -translate-x-1/2
               bg-white/90 backdrop-blur px-3 py-1
               rounded-lg shadow text-xs font-mono
               border border-gray-300 z-40"
    style={{ pointerEvents: "none" }}
  >
    <div>Lon : {coords.lon}</div>
    <div>Lat : {coords.lat}</div>
  </div>
);
}
