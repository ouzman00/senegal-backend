import { useEffect, useState } from "react";
import "./App.css";
import Carte from "./component/Carte";

const API_BASE_URL =
  (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

function App() {
  const [hopitauxData, setHopitauxData] = useState(null);
  const [ecolesData, setEcolesData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const hopitauxUrl = `${API_BASE_URL}/api/hopitaux/`;

    // --- HOPITAUX (obligatoire) ---
    fetch(hopitauxUrl)
      .then((res) => {
        if (!res.ok) throw new Error(`Hopitaux HTTP ${res.status}`);
        return res.json();
      })
      .then(setHopitauxData)
      .catch((err) => {
        console.error("Erreur hopitaux :", err);
        setError(err.message);
      });
  }, []);

  if (error) return <div>Erreur API: {error}</div>;
  if (!hopitauxData) return <div>Chargement des données...</div>;

  return <Carte hopitauxData={hopitauxData} ecolesData={ecolesData} />;
}

export default App;
