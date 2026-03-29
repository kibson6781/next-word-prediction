import React, { useState } from 'react';
import './ResultPanel.css';

export default function ResultPanel({ result }) {
  const [copied, setCopied] = useState(false);

  const copy = () => {
    navigator.clipboard.writeText(result.full_sentence);
    setCopied(true);
    setTimeout(() => setCopied(false), 1800);
  };

  const words = result.full_sentence.split(' ');
  const seedLen = result.seed.split(' ').length;

  return (
    <div className="card result-card" style={{ animationDelay: '0.1s' }}>
      <div className="result-header">
        <div>
          <p className="card-label">Output</p>
          <h2 className="card-title">Predicted Sentence</h2>
        </div>
        <div className="result-meta">
          <span className="glow-pill">
            <span className="dot" />
            {result.mode === 'beam_search' ? 'Beam Search' : 'Sampling'}
          </span>
          <button className="copy-btn" onClick={copy}>
            {copied ? '✓ Copied' : '⎘ Copy'}
          </button>
        </div>
      </div>

      <div className="sentence-display">
        {words.map((w, i) => (
          <span
            key={i}
            className={`word ${i >= seedLen ? 'predicted' : 'seed'}`}
            style={i >= seedLen ? { animationDelay: `${(i - seedLen) * 0.08}s` } : {}}
          >
            {w}{i < words.length - 1 ? ' ' : ''}
          </span>
        ))}
      </div>

      <div className="result-stats">
        <Stat label="Seed words" val={seedLen} />
        <Stat label="Predicted" val={result.predicted_words?.length ?? '—'} color="accent" />
        <Stat label="Total words" val={words.length} />
        <Stat label="Characters" val={result.full_sentence.length} />
      </div>
    </div>
  );
}

function Stat({ label, val, color }) {
  return (
    <div className="stat">
      <span className={`stat-val ${color ? `stat-${color}` : ''}`}>{val}</span>
      <span className="stat-label">{label}</span>
    </div>
  );
}
