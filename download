import React, { useState, useEffect, useRef, useCallback } from "react";
import "./App.css";

const API = process.env.REACT_APP_API_URL || "";

function debounce(fn, delay) {
  let timer;
  return (...args) => { clearTimeout(timer); timer = setTimeout(() => fn(...args), delay); };
}

export default function App() {
  const [text, setText] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeIdx, setActiveIdx] = useState(-1);
  const [showDrop, setShowDrop] = useState(false);
  const [apiOk, setApiOk] = useState(null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (!API) { setApiOk(false); return; }
    fetch(`${API}/health`).then(r => r.ok ? setApiOk(true) : setApiOk(false)).catch(() => setApiOk(false));
  }, []);

  const fetchSuggestions = useCallback(debounce(async (val) => {
    if (!val.trim() || !API) { setSuggestions([]); setShowDrop(false); return; }
    setLoading(true);
    try {
      const res = await fetch(`${API}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: val, top_k: 6 }),
      });
      const data = await res.json();
      setSuggestions(data.suggestions || []);
      setShowDrop(true);
      setActiveIdx(-1);
    } catch { setSuggestions([]); } finally { setLoading(false); }
  }, 250), []);

  useEffect(() => { fetchSuggestions(text); }, [text]);

  const appendWord = (word) => {
    const trimmed = text.trimEnd();
    setText(trimmed ? trimmed + " " + word + " " : word + " ");
    setSuggestions([]); setShowDrop(false); setActiveIdx(-1);
    inputRef.current?.focus();
  };

  const handleKey = (e) => {
    if (!showDrop || !suggestions.length) return;
    if (e.key === "ArrowDown") { e.preventDefault(); setActiveIdx(i => Math.min(i+1, suggestions.length-1)); }
    if (e.key === "ArrowUp")   { e.preventDefault(); setActiveIdx(i => Math.max(i-1, -1)); }
    if (e.key === "Enter" && activeIdx >= 0) { e.preventDefault(); appendWord(suggestions[activeIdx].word); }
    if (e.key === "Escape") { setShowDrop(false); setActiveIdx(-1); }
    if (e.key === "Tab" && suggestions.length) { e.preventDefault(); appendWord(suggestions[activeIdx >= 0 ? activeIdx : 0].word); }
  };

  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;

  return (
    <div className="app">
      <header className="header">
        <div className="logo"><span className="logo-bracket">[</span><span className="logo-text">NWP</span><span className="logo-bracket">]</span></div>
        <h1 className="title">Next Word Predictor</h1>
        <p className="subtitle">n-gram statistical language model</p>
        {apiOk === false && <div className="api-warn">⚠ Backend not connected — set REACT_APP_API_URL in .env.production</div>}
        {apiOk === true  && <div className="api-ok">● API connected</div>}
      </header>
      <main className="main">
        <div className="search-wrapper">
          <div className={`search-box ${showDrop && suggestions.length ? "open" : ""}`}>
            <div className="input-row">
              <span className="prompt-symbol">›</span>
              <textarea ref={inputRef} className="search-input" value={text}
                onChange={e => setText(e.target.value)} onKeyDown={handleKey}
                onFocus={() => suggestions.length && setShowDrop(true)}
                placeholder="Start typing a sentence…" rows={3} spellCheck={false} />
              {loading && <span className="spinner" />}
              {text && <button className="clear-btn" onClick={() => { setText(""); setSuggestions([]); setShowDrop(false); inputRef.current?.focus(); }}>✕</button>}
            </div>
            {showDrop && suggestions.length > 0 && (
              <ul className="dropdown" role="listbox">
                {suggestions.map((s, i) => (
                  <li key={s.word} className={`suggestion ${i === activeIdx ? "active" : ""}`}
                    onMouseDown={() => appendWord(s.word)} onMouseEnter={() => setActiveIdx(i)}
                    role="option" aria-selected={i === activeIdx}>
                    <span className="suggestion-word">{s.word}</span>
                    <span className="suggestion-bar-wrap"><span className="suggestion-bar" style={{ width: `${Math.round(s.score * 100)}%` }} /></span>
                    <span className="suggestion-score">{Math.round(s.score * 100)}%</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
          <div className="hints"><span>↑↓ navigate</span><span>Tab / Enter to insert</span><span>Esc to close</span></div>
        </div>
        <section className="stats">
          <div className="stat"><span className="stat-val">{wordCount}</span><span className="stat-label">words</span></div>
          <div className="stat"><span className="stat-val">{text.length}</span><span className="stat-label">chars</span></div>
          <div className="stat"><span className="stat-val">{suggestions.length}</span><span className="stat-label">predictions</span></div>
        </section>
      </main>
    </div>
  );
}
