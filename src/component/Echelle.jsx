import { useEffect, useMemo, useRef, useState } from "react";
import ScaleLine from "ol/control/ScaleLine";

/**
 * Calcule une échelle approximative 1:XXXXX
 * Hypothèse : écran 96 dpi (standard web). C’est une approximation.
 */
function getScaleDenominator(view, projection, dpi = 96) {
  const resolution = view.getResolution();
  if (!resolution) return null;

  // m/pixel * pixel/inch * inch/m = ratio
  const inchesPerMeter = 39.37;
  const metersPerPixel = resolution; // EPSG:3857 -> en mètres
  const scale = metersPerPixel * dpi * inchesPerMeter;

  return Math.round(scale);
}

function formatScale(scale) {
  if (!scale) return "—";
  return `1:${scale.toLocaleString("fr-FR")}`;
}

export default function Echelle({ map }) {
  const scaleRef = useRef(null);
  const [scaleDenom, setScaleDenom] = useState(null);

  // Liste d’échelles proposées
  const options = useMemo(
    () => [100, 500, 1000, 10000, 500000, 1000000, 2500000, 50000000],
    []
  );

  // Control ScaleLine (barre graphique)
  useEffect(() => {
    if (!map || !scaleRef.current) return;

    const control = new ScaleLine({
      units: "metric",
      bar: true,
      steps: 4,
      text: true,
      minWidth: 120,
      target: scaleRef.current, // on l'injecte dans notre div
    });

    map.addControl(control);

    return () => {
      map.removeControl(control);
    };
  }, [map]);

  // Met à jour le 1:xxxxx quand on bouge/zoom
  useEffect(() => {
    if (!map) return;

    const view = map.getView();
    const update = () => {
      const denom = getScaleDenominator(view, view.getProjection());
      setScaleDenom(denom);
    };

    update();
    view.on("change:resolution", update);

    return () => {
      view.un("change:resolution", update);
    };
  }, [map]);

  // Choisir une échelle -> ajuste zoom (approx)
  const onSelectScale = (e) => {
    if (!map) return;
    const targetScale = Number(e.target.value);
    if (!targetScale) return;

    const view = map.getView();
    const currentScale = getScaleDenominator(view, view.getProjection());
    if (!currentScale) return;

    // ratio entre échelle actuelle et échelle désirée
    // si targetScale est plus grand => zoom out
    const ratio = targetScale / currentScale;

    // resolution varie linéairement, zoom varie en log2
    // newZoom = zoom - log2(ratio)
    const currentZoom = view.getZoom();
    if (currentZoom == null) return;

    const delta = Math.log2(ratio);
    const newZoom = currentZoom - delta;

    view.animate({ zoom: newZoom, duration: 300 });
  };

  return (
  <div
    className="bg-white/90 backdrop-blur px-3 py-2 rounded-lg shadow border border-gray-300 text-xs"
    style={{ pointerEvents: "auto" }}
  >
    <div className="flex items-center justify-between gap-3">
      <div className="font-mono">{formatScale(scaleDenom)}</div>

      <select
        className="border rounded px-2 py-1 bg-white"
        onChange={onSelectScale}
        defaultValue=""
      >
        <option value="" disabled>
          Choisir…
        </option>
        {options.map((s) => (
          <option key={s} value={s}>
            1:{s.toLocaleString("fr-FR")}
          </option>
        ))}
      </select>
    </div>

    {/* Barre graphique OL */}
    
  </div>
);

}
