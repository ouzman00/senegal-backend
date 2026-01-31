import React, { useEffect, useMemo, useState } from "react";
import Draw from "ol/interaction/Draw";
import Modify from "ol/interaction/Modify";
import Snap from "ol/interaction/Snap";
import Select from "ol/interaction/Select";
import { click } from "ol/events/condition";
import GeoJSON from "ol/format/GeoJSON";

function normalizeBaseUrl(url) {
  if (!url) return "";
  return url.trim().replace(/\/+$/, "");
}

function getFeatureStableId(feature) {
  const id = feature?.getId?.();
  if (id !== undefined && id !== null && id !== "") return id;

  const pid = feature?.get?.("id");
  if (pid !== undefined && pid !== null && pid !== "") return pid;

  const props = feature?.getProperties?.() || {};
  if (props?.id !== undefined && props?.id !== null && props?.id !== "") return props.id;

  return null;
}

function removeFeatureByIdSafe(source, id) {
  if (!source || id == null) return;
  const f = source.getFeatureById?.(id);
  if (f) return source.removeFeature(f);

  const all = source.getFeatures?.() || [];
  const target = all.find((x) => String(getFeatureStableId(x)) === String(id));
  if (target) source.removeFeature(target);
}

export default function MapEditor({
  map,
  editableLayer,
  apiBaseUrl,
  drawType = "Point",
  defaultName = "Nouvel objet",
  flatPayload = false,
}) {
  const [mode, setMode] = useState("none");
  const [selectedId, setSelectedId] = useState(null);
  const geojson = useMemo(() => new GeoJSON(), []);
  const baseUrl = useMemo(() => normalizeBaseUrl(apiBaseUrl), [apiBaseUrl]);

  if (!baseUrl) {
    return (
      <div className="p-3 bg-red-100 border border-red-300 rounded">
        MapEditor désactivé (API non configurée)
      </div>
    );
  }

  useEffect(() => {
    if (!map || !editableLayer) return;

    const select = new Select({
      condition: click,
      layers: [editableLayer],
    });

    select.on("select", (e) => {
      const f = e.selected?.[0] || null;
      setSelectedId(f ? getFeatureStableId(f) : null);
    });

    if (mode === "draw") select.setActive(false);

    map.addInteraction(select);
    return () => map.removeInteraction(select);
  }, [map, editableLayer, mode]);

  useEffect(() => {
    if (!map || !editableLayer) return;
    const source = editableLayer.getSource();
    if (!source) return;

    let draw = null;
    let modify = null;
    const snap = new Snap({ source });

    if (mode === "draw") {
      draw = new Draw({ source, type: drawType });

      draw.on("drawend", async (evt) => {
        const feature = evt.feature;

        const geo = geojson.writeFeatureObject(feature, {
          dataProjection: "EPSG:4326",
          featureProjection: "EPSG:3857",
        });

        const props = {
          nom: feature.get("nom") ?? defaultName,
          adresse: feature.get("adresse") ?? null,
        };

        const payload = flatPayload
          ? { ...props, geometry: geo.geometry }
          : { type: "Feature", geometry: geo.geometry, properties: props };

        try {
          const res = await fetch(`${baseUrl}/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
          });

          if (!res.ok) throw new Error(`POST HTTP ${res.status}`);

          const created = await res.json();
          const createdId =
            created?.id ?? created?.properties?.id ?? created?.pk ?? created?.uuid ?? null;

          if (createdId != null) {
            feature.setId(createdId);
            feature.set("id", createdId);
          }

          const createdProps = created?.properties ?? created ?? {};
          feature.set("nom", createdProps.nom ?? props.nom ?? defaultName);
          feature.set("adresse", createdProps.adresse ?? props.adresse ?? null);
        } catch (err) {
          console.error("MapEditor POST:", err);
          source.removeFeature(feature);
          alert("Création impossible (API)");
        }
      });
    }

    if (mode === "modify") {
      modify = new Modify({ source });

      modify.on("modifyend", async (evt) => {
        for (const feature of evt.features.getArray()) {
          const id = getFeatureStableId(feature);
          if (!id) continue;

          const geo = geojson.writeFeatureObject(feature, {
            dataProjection: "EPSG:4326",
            featureProjection: "EPSG:3857",
          });

          const props = {
            nom: feature.get("nom") ?? defaultName,
            adresse: feature.get("adresse") ?? null,
          };

          const payload = flatPayload
            ? { ...props, geometry: geo.geometry }
            : { type: "Feature", geometry: geo.geometry, properties: props };

          try {
            const res = await fetch(`${baseUrl}/${id}/`, {
              method: "PATCH",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(payload),
            });

            if (!res.ok) throw new Error(`PATCH HTTP ${res.status}`);
          } catch (err) {
            console.error("MapEditor PATCH:", err);
            alert("Modification non enregistrée");
          }
        }
      });
    }

    if (draw) map.addInteraction(draw);
    if (modify) map.addInteraction(modify);
    map.addInteraction(snap);

    return () => {
      if (draw) map.removeInteraction(draw);
      if (modify) map.removeInteraction(modify);
      map.removeInteraction(snap);
    };
  }, [map, editableLayer, mode, baseUrl, geojson, drawType, defaultName, flatPayload]);

  const deleteSelected = async () => {
    if (!editableLayer || !selectedId) {
      alert("Sélectionne un objet");
      return;
    }

    const source = editableLayer.getSource();

    try {
      const res = await fetch(`${baseUrl}/${selectedId}/`, { method: "DELETE" });
      if (!res.ok && res.status !== 204) throw new Error(`DELETE HTTP ${res.status}`);

      removeFeatureByIdSafe(source, selectedId);
      setSelectedId(null);
    } catch (err) {
      console.error("MapEditor DELETE:", err);
      alert("Suppression impossible");
    }
  };

  return (
    <div className="p-3 bg-white border border-gray-300 rounded-lg shadow flex flex-col gap-2">
      <div className="font-semibold">
        Éditeur ({drawType === "Polygon" ? "Surface" : "Point"})
      </div>

      <div className="flex gap-2 flex-wrap">
        <button
          className={`px-3 py-1 rounded ${
            mode === "draw" ? "bg-gray-800 text-white" : "bg-gray-200"
          }`}
          onClick={() => setMode(mode === "draw" ? "none" : "draw")}
        >
          Draw {drawType}
        </button>

        <button
          className={`px-3 py-1 rounded ${
            mode === "modify" ? "bg-gray-800 text-white" : "bg-gray-200"
          }`}
          onClick={() => setMode(mode === "modify" ? "none" : "modify")}
        >
          Modify
        </button>

        <button className="px-3 py-1 rounded bg-red-200" onClick={deleteSelected}>
          Delete
        </button>
      </div>

      <div className="text-xs text-gray-600">
        Sélection : {selectedId ? `ID ${selectedId}` : "aucune"}
      </div>
    </div>
  );
}
