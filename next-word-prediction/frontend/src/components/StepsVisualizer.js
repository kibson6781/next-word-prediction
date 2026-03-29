import React, { useState } from 'react';
import './StepsVisualizer.css';

export default function StepsVisualizer({ steps }) {
  const [expanded, setExpanded] = useState(0);

  return (
    <div className="card steps-card" style={{ animationDelay: '0.2s' }}>
      <p className="card-label">Step-by-Step</p>
      <h2 className="card-title">Prediction Breakdown</h2>
      <p className="steps-intro">
        Each step shows the top candidate words and their probabilities. Hover to explore.
      </p>

      <div className="steps-list">
        {steps.map((step, i) => (
          <StepRow
            key={i}
            step={step}
            index={i}
            isOpen={expanded === i}
            onToggle={() => setExpanded(expanded === i ? -1 : i)}
          />
        ))}
      </div>
    </div>
  );
}

function StepRow({ step, index, isOpen, onToggle }) {
  const maxProb = Math.max(...step.candidates.map(c => c.probability));

  return (
    <div className={`step-row ${isOpen ? 'open' : ''}`}>
      <button className="step-summary" onClick={onToggle}>
        <span className="step-num">#{index + 1}</span>
        <span className="step-chosen">{step.chosen}</span>
        <span className="step-input-preview">…{step.input.slice(-30)}</span>
        <span className="step-chevron">{isOpen ? '▲' : '▼'}</span>
      </button>

      {isOpen && (
        <div className="step-detail">
          <p className="step-context">
            <span className="ctx-label">Context:</span>
            <span className="ctx-text">"{step.input}"</span>
          </p>
          <div className="candidates">
            {step.candidates.map((c, j) => (
              <CandidateBar
                key={j}
                candidate={c}
                isChosen={c.word === step.chosen}
                maxProb={maxProb}
                rank={j + 1}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function CandidateBar({ candidate, isChosen, maxProb, rank }) {
  const pct = (candidate.probability / maxProb) * 100;
  return (
    <div className={`cand-row ${isChosen ? 'chosen' : ''}`}>
      <span className="cand-rank">#{rank}</span>
      <span className="cand-word">{candidate.word}</span>
      <div className="cand-bar-wrap">
        <div
          className="cand-bar"
          style={{ width: `${pct}%`, animationDelay: `${rank * 0.05}s` }}
        />
      </div>
      <span className="cand-prob">{candidate.probability.toFixed(1)}%</span>
      {isChosen && <span className="chosen-tag">✓ chosen</span>}
    </div>
  );
}
