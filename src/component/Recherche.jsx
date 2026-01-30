import { useEffect, useRef, useState } from "react";
import { fromLonLat } from "ol/proj";
import VectorLayer from "ol/layer/Vector";
import VectorSource from "ol/source/Vector";
import Feature from "ol/Feature";
import Point from "ol/geom/Point";
import { Style, Circle as CircleStyle, Fill, Stroke } from "ol/style";

export default function Recherche({ map }) {
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(false);

  const layerRef = useRef(null);

  // crée/ajoute la couche marqueur une seule fois
  useEffect(() => {
    if (!map) return;

    if (!layerRef.current) {
      layerRef.current = new VectorLayer({
        source: new VectorSource(),
        style: new Style({
          image: new CircleStyle({
            radius: 7,
            fill: new Fill({ color: "#111" }),
            stroke: new Stroke({ color: "#fff", width: 2 }),
          }),
        }),
      });
      map.addLayer(layerRef.current);
    }

    return () => {
      // si tu veux la retirer quand le composant se démonte :
      // if (layerRef.current) map.removeLayer(layerRef.current);
    };
  }, [map]);

  const setMarkerAndZoom = (lon, lat, zoom = 13) => {
    if (!map || !layerRef.current) return;

    const source = layerRef.current.getSource();
    source.clear();

    const f = new Feature({
      geometry: new Point(fromLonLat([lon, lat])),
    });
    source.addFeature(f);

    map.getView().animate({
      center: fromLonLat([lon, lat]),
      zoom,
      duration: 600,
    });
  };

  // 🔍 recherche via Nominatim
  const search = async () => {
    if (!map) return;
    const query = q.trim();
    if (!query) return;

    setLoading(true);
    try {
      const res = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&limit=1&q=${encodeURIComponent(
          query
        )}`
      );
      const data = await res.json();

      if (!data?.length) {
        alert("Aucun résultat");
        return;
      }

      const lon = Number(data[0].lon);
      const lat = Number(data[0].lat);
      setMarkerAndZoom(lon, lat, 13);
    } catch (e) {
      console.error(e);
      alert("Erreur de recherche");
    } finally {
      setLoading(false);
    }
  };

  // 📍 localisation
  const locate = () => {
    if (!map) return;

    if (!navigator.geolocation) {
      alert("Géolocalisation non supportée");
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const { longitude, latitude } = pos.coords;
        setMarkerAndZoom(longitude, latitude, 15);
      },
      () => alert("Impossible d'obtenir la position"),
      { enableHighAccuracy: true, timeout: 10000 }
    );
  };

  return (
    <div
      className="bg-white border border-gray-300 rounded-md px-2 py-2 shadow-sm flex items-center gap-2"
      style={{ pointerEvents: "auto" }}
    >
      <input
        value={q}
        onChange={(e) => setQ(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && search()}
        placeholder="Rechercher une ville / adresse…"
        className="border border-gray-300 rounded px-2 py-1 text-sm w-64 outline-none"
      />

      <button
        onClick={search}
        disabled={loading}
        className="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-100"
      >
        {loading ? "..." : "OK"}
      </button>

      <button
        onClick={locate}
        className="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-100"
        title="Ma position"
      >
        📍
      </button>
    </div>
  );
}
