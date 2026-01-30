import React, { useEffect, useMemo, useRef, useState } from "react";
import "ol/ol.css";
import { Map, View } from "ol";
import TileLayer from "ol/layer/Tile";
import VectorLayer from "ol/layer/Vector";
import OSM from "ol/source/OSM";
import VectorSource from "ol/source/Vector";
import GeoJSON from "ol/format/GeoJSON";
import { fromLonLat } from "ol/proj";
import { Style, Stroke, Fill, Circle as CircleStyle } from "ol/style";

import Coordonnees from "./Coordonnees";
import MapEditor from "./MapEditor";
import RegionChart from "./RegionChart";
import Population from "./Population";
import Mesures from "./Mesures";
import Echelle from "./Echelle";
import Recherche from "./Recherche";

/* =======================
   API BASE (DEV + PROD)
   - En prod (Vercel): VITE_API_BASE_URL doit être défini
   - En dev: fallback sur http://127.0.0.1:8000
======================= */
const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  (import.meta.env.DEV ? "http://127.0.0.1:8000" : "")
).replace(/\/$/, "");

/* =======================
   IMPORTANT (Vite)
   Mets tes fichiers GeoJSON dans:
   public/donnees_shp/regions.geojson
   public/donnees_shp/communes.geojson

   ⚠️ Recommandé: renommer sans accents:
   - Régions.geojson -> regions.geojson
   - Communes.geojson -> communes.geojson
======================= */

export default function Carte({ hopitauxData, ecolesData }) {
  const mapRef = useRef(null);
  const [map, setMap] = useState(null);

  const [layers, setLayers] = useState({
    Regions: null,
    Communes: null,
    hopitaux: null,
    ecoles: null,
    highlight: null,
    overlay: null,
  });

  const [visibleLayers, setVisibleLayers] = useState({
    Regions: true,
    Communes: false,
    hopitaux: true,
    ecoles: false,
  });

  // Pour éviter de “capturer” un vieux état dans l’init de la map
  const visibleLayersRef = useRef(visibleLayers);
  useEffect(() => {
    visibleLayersRef.current = visibleLayers;
  }, [visibleLayers]);

  const [selectedFeature, setSelectedFeature] = useState(null);

  /* =======================
     CONFIG DES COUCHES
  ======================= */
  const layerConfigs = useMemo(
    () => [
      {
        id: "Regions",
        // ✅ chemin Vercel-friendly (fichier dans /public)
        url: "/donnees_shp/Régions.geojson",
        color: "#1E0F1C",
        width: 3,
        fill: "rgba(255,0,0,0)",
        name: "Régions",
      },
      {
        id: "Communes",
        url: "/donnees_shp/communes.geojson",
        color: "#A7001E",
        width: 1,
        fill: "rgba(255,0,0,0)",
        name: "Communes",
      },
      {
        id: "hopitaux",
        color: "#00FF00",
        type: "point",
        name: "Hôpitaux",
      },
      {
        id: "ecoles",
        color: "#1D4ED8",
        type: "polygon",
        name: "Écoles",
      },
    ],
    []
  );

  /* =======================
     INIT MAP (une seule fois)
  ======================= */
  useEffect(() => {
    if (!mapRef.current) return;

    // (Optionnel) aide debug: vérifier la variable en prod
    // eslint-disable-next-line no-console
    console.log("API BASE URL =", import.meta.env.VITE_API_BASE_URL);

    const baseLayer = new TileLayer({ source: new OSM() });

    const mapInstance = new Map({
      target: mapRef.current,
      layers: [baseLayer],
      view: new View({
        center: fromLonLat([-14.5, 14.5]),
        zoom: 8,
      }),
    });

    const highlightLayer = new VectorLayer({
      source: new VectorSource(),
      style: new Style({
        image: new CircleStyle({
          radius: 10,
          stroke: new Stroke({ color: "#FFD700", width: 3 }),
          fill: new Fill({ color: "rgba(255,215,0,0.3)" }),
        }),
        stroke: new Stroke({ color: "#FFD700", width: 3 }),
        fill: new Fill({ color: "rgba(255,215,0,0.15)" }),
      }),
    });

    const overlayLayer = new VectorLayer({
      source: new VectorSource(),
      visible: false,
    });

    mapInstance.addLayer(highlightLayer);
    mapInstance.addLayer(overlayLayer);

    const createdLayers = {};

    // Charge uniquement les couches GeoJSON statiques (Regions/Communes)
    layerConfigs
      .filter((c) => c.url)
      .forEach((config) => {
        const source = new VectorSource({
          url: config.url, // ✅ servie par Vercel si le fichier est dans /public
          format: new GeoJSON(),
        });

        source.on("addfeature", (e) => {
          e.feature.set("layerName", config.name);
        });

        const layer = new VectorLayer({
          source,
          visible: !!visibleLayersRef.current[config.id],
          style: new Style({
            stroke: new Stroke({
              color: config.color,
              width: config.width ?? 2,
            }),
            fill: config.fill ? new Fill({ color: config.fill }) : undefined,
          }),
        });

        createdLayers[config.id] = layer;
        mapInstance.addLayer(layer);
      });

    mapInstance.on("singleclick", (evt) => {
      let found = null;

      mapInstance.forEachFeatureAtPixel(evt.pixel, (feature) => {
        found = feature;
        return true;
      });

      if (found) {
        const props = found.getProperties();
        setSelectedFeature({ ...props, layerName: props.layerName || "Couche" });

        highlightLayer.getSource().clear();
        highlightLayer.getSource().addFeature(found.clone());
        overlayLayer.setVisible(true);
      } else {
        setSelectedFeature(null);
        highlightLayer.getSource().clear();
        overlayLayer.setVisible(false);
      }
    });

    setLayers({
      ...createdLayers,
      highlight: highlightLayer,
      overlay: overlayLayer,
    });

    setMap(mapInstance);

    return () => {
      mapInstance.setTarget(undefined);
    };
  }, [layerConfigs]);

  /* =======================
     VISIBILITÉ (toggle)
  ======================= */
  useEffect(() => {
    Object.entries(visibleLayers).forEach(([k, v]) => {
      layers[k]?.setVisible(!!v);
    });
  }, [visibleLayers, layers]);

  /* =======================
     HÔPITAUX (GeoJSON DRF)
  ======================= */
  useEffect(() => {
    if (!map || !Array.isArray(hopitauxData?.features)) return;

    if (layers.hopitaux) map.removeLayer(layers.hopitaux);

    const features = new GeoJSON().readFeatures(hopitauxData, {
      dataProjection: "EPSG:4326",
      featureProjection: "EPSG:3857",
    });

    features.forEach((f) => f.set("layerName", "Hôpitaux"));

    const source = new VectorSource({ features });

    const layer = new VectorLayer({
      source,
      visible: !!visibleLayers.hopitaux,
      style: new Style({
        image: new CircleStyle({
          radius: 6,
          fill: new Fill({ color: "#00FF00" }),
          stroke: new Stroke({ color: "#000", width: 1 }),
        }),
      }),
    });

    map.addLayer(layer);
    setLayers((p) => ({ ...p, hopitaux: layer }));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [map, hopitauxData]);

  /* =======================
     ÉCOLES (GeoJSON)
  ======================= */
  useEffect(() => {
    if (!map || !Array.isArray(ecolesData?.features)) return;

    if (layers.ecoles) map.removeLayer(layers.ecoles);

    const features = new GeoJSON().readFeatures(ecolesData, {
      dataProjection: "EPSG:4326",
      featureProjection: "EPSG:3857",
    });

    features.forEach((f) => f.set("layerName", "Écoles"));

    const source = new VectorSource({ features });

    const layer = new VectorLayer({
      source,
      visible: !!visibleLayers.ecoles,
      style: new Style({
        stroke: new Stroke({ color: "#1D4ED8", width: 2 }),
        fill: new Fill({ color: "rgba(29,78,216,0.15)" }),
      }),
    });

    map.addLayer(layer);
    setLayers((p) => ({ ...p, ecoles: layer }));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [map, ecolesData]);

  /* =======================
     UI
  ======================= */
  return (
    <div className="max-w-[1800px] mx-auto mt-10 px-4">
      <div className="border-2 rounded-xl p-6 shadow bg-white flex gap-4">
        <div className="w-60">
          <h3 className="font-semibold mb-2">Légende</h3>

          {layerConfigs.map((l) => (
            <label key={l.id} className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={!!visibleLayers[l.id]}
                onChange={() =>
                  setVisibleLayers((p) => ({ ...p, [l.id]: !p[l.id] }))
                }
              />
              <span>{l.name}</span>
            </label>
          ))}

          {/* Petit indicateur utile en prod */}
          <div className="mt-3 text-xs text-gray-500 break-words">
            API: {API_BASE_URL || "(non défini en prod)"}
          </div>
        </div>

        <div className="flex-1 relative">
          <div ref={mapRef} className="w-full h-[800px] border rounded" />
          <Recherche map={map} />
          <Coordonnees map={map} />
          <Mesures map={map} />
          <Echelle map={map} />
        </div>

        <div className="w-80 space-y-4">
          <Population selectedFeature={selectedFeature} />

          {map && layers.hopitaux && (
            <MapEditor
              map={map}
              editableLayer={layers.hopitaux}
              // ✅ endpoint complet, stable
              apiBaseUrl={`${API_BASE_URL}/api/hopitaux/`}
            />
          )}

          <RegionChart selectedRegion={selectedFeature?.nom || null} />
        </div>
      </div>
    </div>
  );
}
