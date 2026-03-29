import React, { useState } from 'react';
import './PredictionPanel.css';

const PRESETS = [
  'The future of artificial intelligence',
  'Machine learning is a',
  'Deep neural networks can',
  'The ocean covers more than',
  'Climate change is one of',
];

export default function PredictionPanel({ formData, setFormData, onPredict, loading }) {
  const [charCount, setCharCount] = useState(0);

  const update = (key, val) => setFormData(p => ({ ...p, [key]: val }));

  const handleTextChange = e => {
    update('seedText', e.target.value);
    setCharCount(e.target.value.length);
  };

  const handleKeyDown = e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') onPredict();
  };

  return (
    <div className="card panel">
      <div className="panel-header">
        <div>
          <p className="card-label">Input</p>
          <h2 className="card-title">Seed Text & Parameters</h2>
        </div>
        <span className="kbd-hint">⌘↵ to run</span>
      </div>

      {/* Seed Text */}
      <div className="field">
        <label className="field-label">Seed Text</label>
        <div className="textarea-wrap">
          <textarea
            className="seed-input"
            placeholder="Start typing… e.g. 'The future of'"
            value={formData.seedText}
            onChange={handleTextChange}
            onKeyDown={handleKeyDown}
            rows={3}
          />
          <span className="char-count">{charCount}</span>
        </div>
        {/* Presets */}
        <div className="presets">
          {PRESETS.map(p => (
            <button
              key={p}
              className="preset-chip"
              onClick={() => { update('seedText', p); setCharCount(p.length); }}
            >
              {p}
            </button>
          ))}
        </div>
      </div>

      {/* Controls grid */}
      <div className="controls-grid">
        {/* Number of words */}
        <div className="control-group">
          <label className="field-label">
            Predicted Words
            <span className="val-badge">{formData.nWords}</span>
          </label>
          <input
            type="range" min={1} max={50} step={1}
            value={formData.nWords}
            onChange={e => update('nWords', +e.target.value)}
            className="slider accent-slider"
          />
          <div className="slider-ticks">
            {[1,10,20,30,40,50].map(n => (
              <span key={n} onClick={() => update('nWords', n)}>{n}</span>
            ))}
          </div>
        </div>

        {/* Temperature */}
        <div className="control-group">
          <label className="field-label">
            Temperature
            <span className="val-badge">{formData.temperature.toFixed(1)}</span>
          </label>
          <input
            type="range" min={0.1} max={2.0} step={0.1}
            value={formData.temperature}
            onChange={e => update('temperature', +e.target.value)}
            className="slider pink-slider"
            disabled={formData.mode === 'beam'}
          />
          <div className="temp-desc">
            {formData.temperature < 0.5 ? '🧊 Conservative' :
             formData.temperature < 1.2 ? '⚖ Balanced' : '🔥 Creative'}
          </div>
        </div>

        {/* Top-K */}
        <div className="control-group">
          <label className="field-label">
            Top-K Candidates
            <span className="val-badge">{formData.topK}</span>
          </label>
          <input
            type="range" min={1} max={20} step={1}
            value={formData.topK}
            onChange={e => update('topK', +e.target.value)}
            className="slider teal-slider"
            disabled={formData.mode === 'beam'}
          />
          <p className="field-hint">Words shown as alternatives per step</p>
        </div>

        {/* Mode */}
        <div className="control-group">
          <label className="field-label">Decoding Mode</label>
          <div className="mode-toggle">
            {[
              { id: 'sample', icon: '🎲', label: 'Sampling' },
              { id: 'beam',   icon: '🔭', label: 'Beam Search' },
            ].map(m => (
              <button
                key={m.id}
                className={`mode-btn ${formData.mode === m.id ? 'active' : ''}`}
                onClick={() => update('mode', m.id)}
              >
                <span>{m.icon}</span>
                <span>{m.label}</span>
              </button>
            ))}
          </div>
          <p className="field-hint">
            {formData.mode === 'beam'
              ? 'Beam search: deterministic, returns top-3 sentences'
              : 'Sampling: stochastic, uses temperature & top-K'}
          </p>
        </div>
      </div>

      {/* Run button */}
      <button
        className={`run-btn ${loading ? 'loading' : ''}`}
        onClick={onPredict}
        disabled={loading || !formData.seedText.trim()}
      >
        {loading ? (
          <>
            <span className="spinner" />
            Predicting…
          </>
        ) : (
          <>
            <span className="run-icon">⚡</span>
            Predict Next Words
          </>
        )}
      </button>
    </div>
  );
}
