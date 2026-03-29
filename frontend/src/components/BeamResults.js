import React, { useState } from 'react';
import './BeamResults.css';

export default function BeamResults({ beams, seed }) {
  const [copied, setCopied] = useState(null);

  const copy = (text, i) => {
    navigator.clipboard.writeText(text);
    setCopied(i);
    setTimeout(() => setCopied(null), 1800);
  };

  return (
    <div className="card beam-card" style={{ animationDelay: '0.2s' }}>
      <p className="card-label">Beam Search</p>
      <h2 className="card-title">Top Candidate Sequences</h2>
      <p className="beam-intro">
        Beam search explores multiple paths simultaneously and returns the highest-scoring sequences.
      </p>

      <div className="beam-list">
        {beams.map((b, i) => {
          const words = b.sentence.split(' ');
          const seedLen = seed.split(' ').length;
          return (
            <div key={i} className={`beam-item ${i === 0 ? 'best' : ''}`}>
              <div className="beam-rank">
                <span className="rank-num">#{i + 1}</span>
                {i === 0 && <span className="best-tag">Best</span>}
              </div>
              <div className="beam-content">
                <div className="beam-sentence">
                  {words.map((w, j) => (
                    <span key={j} className={j >= seedLen ? 'b-predicted' : 'b-seed'}>
                      {w}{' '}
                    </span>
                  ))}
                </div>
                <div className="beam-footer">
                  <span className="beam-score">score: {b.score.toFixed(4)}</span>
                  <button className="beam-copy" onClick={() => copy(b.sentence, i)}>
                    {copied === i ? '✓' : '⎘'}
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
