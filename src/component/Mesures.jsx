import { useEffect, useMemo, useRef, useState } from "react";
import VectorLayer from "ol/layer/Vector";
import VectorSource from "ol/source/Vector";
import Draw from "ol/interaction/Draw";
import Snap from "ol/interaction/Snap";
import { Style, Stroke, Fill, Circle as CircleStyle } from "ol/style";
import { getLength, getArea } from "ol/sphere";
import { unByKey } from "ol/Observable";

function formatLengthMeters(lengthMeters) {
  if (!Number.isFinite(lengthMeters)) return "0 m";
  if (lengthMeters >= 1000) return `${(lengthMeters / 1000).toFixed(2)} km`;
  return `${lengthMeters.toFixed(2)} m`;
}

function formatAreaMeters2(areaMeters2) {
  if (!Number.isFinite(areaMeters2)) return "0 m²";
  if (areaMeters2 >= 1_000_000) return `${(areaMeters2 / 1_000_000).toFixed(2)} km²`;
  return `${areaMeters2.toFixed(2)} m²`;
}

export default function Mesures({ map }) {
  const [mode, setMode] = useState("none"); // none | distance | surface
  const [result, setResult] = useState(null);

  const drawRef = useRef(null);
  const snapRef = useRef(null);
  const listenerRef = useRef(null);

  const measureLayer = useMemo(() => {
    return new VectorLayer({
      source: new VectorSource(),
      style: new Style({
        stroke: new Stroke({ color: "#111827", width: 3 }),
        fill: new Fill({ color: "rgba(17,24,39,0.10)" }),
        image: new CircleStyle({
          radius: 5,
          fill: new Fill({ color: "#111827" }),
          stroke: new Stroke({ color: "#fff", width: 1 }),
        }),
      }),
    });
  }, []);

  // Ajouter la couche une seule fois
  useEffect(() => {
    if (!map) return;
    map.addLayer(measureLayer);
    return () => {
      map.removeLayer(measureLayer);
    };
  }, [map, measureLayer]);

  // Gérer interactions Draw/Snap selon mode
  useEffect(() => {
    if (!map) return;

    // cleanup ancienne interaction
    if (drawRef.current) map.removeInteraction(drawRef.current);
    if (snapRef.current) map.removeInteraction(snapRef.current);
    if (listenerRef.current) {
      unByKey(listenerRef.current);
      listenerRef.current = null;
    }

    drawRef.current = null;
    snapRef.current = null;

    if (mode === "none") return;

    const source = measureLayer.getSource();
    if (!source) return;

    const type = mode === "distance" ? "LineString" : "Polygon";

    const draw = new Draw({ source, type });
    const snap = new Snap({ source });

    drawRef.current = draw;
    snapRef.current = snap;

    map.addInteraction(draw);
    map.addInteraction(snap);

    draw.on("drawstart", (evt) => {
      setResult(null);

      const geom = evt.feature.getGeometry();
      listenerRef.current = geom.on("change", (e) => {
        const g = e.target;

        if (mode === "distance") {
          const len = getLength(g); // en mètres (approx sphère)
          setResult({ type: "distance", value: formatLengthMeters(len) });
        } else {
          const area = getArea(g); // en m²
          setResult({ type: "surface", value: formatAreaMeters2(area) });
        }
      });
    });

    draw.on("drawend", () => {
      if (listenerRef.current) {
        unByKey(listenerRef.current);
        listenerRef.current = null;
      }
    });

    return () => {
      if (drawRef.current) map.removeInteraction(drawRef.current);
      if (snapRef.current) map.removeInteraction(snapRef.current);
      if (listenerRef.current) {
        unByKey(listenerRef.current);
        listenerRef.current = null;
      }
      drawRef.current = null;
      snapRef.current = null;
    };
  }, [map, mode, measureLayer]);

  const clear = () => {
    measureLayer.getSource()?.clear();
    setResult(null);
  };

  return (
    <div className="absolute bottom-4 right-4 z-50 flex flex-col gap-2">
      {/* Panel boutons */}
      <div className="bg-white/90 backdrop-blur border border-gray-300 shadow rounded-xl p-2 flex gap-2 flex-wrap">
        <button
          className={`px-3 py-1 rounded-lg text-sm ${
            mode === "distance" ? "bg-gray-900 text-white" : "bg-gray-200"
          }`}
          onClick={() => setMode((m) => (m === "distance" ? "none" : "distance"))}
        >
          Distance
        </button>

        <button
          className={`px-3 py-1 rounded-lg text-sm ${
            mode === "surface" ? "bg-gray-900 text-white" : "bg-gray-200"
          }`}
          onClick={() => setMode((m) => (m === "surface" ? "none" : "surface"))}
        >
          Surface
        </button>

        <button className="px-3 py-1 rounded-lg text-sm bg-red-200" onClick={clear}>
          Effacer
        </button>

        <button className="px-3 py-1 rounded-lg text-sm bg-gray-100" onClick={() => setMode("none")}>
          Arrêter
        </button>
      </div>

      {/* Résultat */}
      <div
        className="bg-white/90 backdrop-blur border border-gray-300 shadow rounded-xl px-3 py-2 text-xs font-mono"
        style={{ pointerEvents: "none" }}
      >
        {mode === "none" ? (
          <div>Mesure : inactif</div>
        ) : result ? (
          <div>
            {result.type === "distance" ? "Distance" : "Surface"} : <b>{result.value}</b>
          </div>
        ) : (
          <div>Tracez sur la carte…</div>
        )}
      </div>
    </div>
  );
}
