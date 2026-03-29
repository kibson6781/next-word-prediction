import React from 'react';
import './Header.css';

export default function Header({ health }) {
  return (
    <header className="header">
      <div className="header-inner">
        <div className="logo-group">
          <div className="logo-icon">
            <svg viewBox="0 0 36 36" fill="none">
              <rect width="36" height="36" rx="10" fill="url(#g1)" />
              <path d="M8 26 L14 10 L18 20 L22 14 L28 26" stroke="#fff" strokeWidth="2.2"
                    strokeLinecap="round" strokeLinejoin="round"/>
              <defs>
                <linearGradient id="g1" x1="0" y1="0" x2="36" y2="36">
                  <stop stopColor="#7c6dff"/>
                  <stop offset="1" stopColor="#ff6db4"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <div>
            <h1 className="logo-text">NextWord<span className="logo-accent">AI</span></h1>
            <p className="logo-sub">Bidirectional LSTM · Next-Word Prediction</p>
          </div>
        </div>
        <div className="header-status">
          {health ? (
            <div className="status-badge online">
              <span className="status-dot" />
              <span>Model Online</span>
              <span className="status-vocab">vocab {health.vocab_size?.toLocaleString()}</span>
            </div>
          ) : (
            <div className="status-badge offline">
              <span className="status-dot" />
              <span>Connecting…</span>
            </div>
          )}
        </div>
      </div>
      <div className="header-bar" />
    </header>
  );
}
