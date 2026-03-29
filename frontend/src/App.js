import React, { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Header';
import PredictionPanel from './components/PredictionPanel';
import ResultPanel from './components/ResultPanel';
import StepsVisualizer from './components/StepsVisualizer';
import BeamResults from './components/BeamResults';
import Footer from './components/Footer';

const API = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export default function App() {
  const [formData, setFormData] = useState({
    seedText: '',
    nWords: 5,
    temperature: 1.0,
    topK: 5,
    mode: 'sample',
  });
  const [result, setResult]     = useState(null);
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState(null);
  const [health, setHealth]     = useState(null);

  useEffect(() => {
    fetch(`${API}/health`)
      .then(r => r.json())
      .then(setHealth)
      .catch(() => setHealth(null));
  }, []);

  const predict = async () => {
    if (!formData.seedText.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch(`${API}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          seed_text:   formData.seedText,
          n_words:     formData.nWords,
          temperature: formData.temperature,
          top_k:       formData.topK,
          mode:        formData.mode,
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      setResult(await res.json());
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="noise-overlay" />
      <div className="grid-bg" />
      <Header health={health} />
      <main className="main">
        <PredictionPanel
          formData={formData}
          setFormData={setFormData}
          onPredict={predict}
          loading={loading}
        />
        {error && (
          <div className="error-banner">
            <span className="err-icon">⚠</span> {error}
          </div>
        )}
        {result && (
          <>
            <ResultPanel result={result} />
            {result.mode === 'sampling' && result.steps?.length > 0 && (
              <StepsVisualizer steps={result.steps} />
            )}
            {result.mode === 'beam_search' && result.beam_results?.length > 0 && (
              <BeamResults beams={result.beam_results} seed={result.seed} />
            )}
          </>
        )}
      </main>
      <Footer />
    </div>
  );
}
