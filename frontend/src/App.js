import React, { useState, useEffect, useRef, useCallback } from "react";
import "./App.css";

// Your Render backend URL (set in .env.production)
const API = process.env.REACT_APP_API_URL || "";

function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

export default function App() {
  const [text, setText] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeIdx, setActiveIdx] = useState(-1);
  const [showDrop, setShowDrop] = useState(false);
  const inputRef = useRef(null);

  const fetchSuggestions = useCallback(
    debounce(async (val) => {
      if (!val.trim() || !API) {
        setSuggestions([]);
        setShowDrop(false);
        return;
      }
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
      } catch {
        setSuggestions([]);
      } finally {
        setLoading(false);
      }
    }, 300),
    []
  );

  useEffect(() => {
    fetchSuggestions(text);
  }, [text]);

  const appendWord = (word) => {
    const trimmed = text.trimEnd();
    setText(trimmed ? trimmed + " " + word + " " : word + " ");
    setSuggestions([]);
    setShowDrop(false);
    setActiveIdx(-1);
    inputRef.current?.focus();
  };

  const handleKey = (e) => {
    if (!showDrop || !suggestions.length) return;
    if (e.key === "ArrowDown") { e.preventDefault(); setActiveIdx(i => Math.min(i + 1, suggestions.length - 1)); }
    if (e.key === "ArrowUp")   { e.preventDefault(); setActiveIdx(i => Math.max(i - 1, -1)); }
    if (e.key === "Enter" && activeIdx >= 0) { e.preventDefault(); appendWord(suggestions[activeIdx].word); }
    if (e.key === "Escape") { setShowDrop(false); setActiveIdx(-1); }
    if (e.key === "Tab" && suggestions.length) { e.preventDefault(); appendWord(suggestions[activeIdx >= 0 ? activeIdx : 0].word); }
  };

  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;

  return (
    <div className="app">
      <header className="header">
        <h1 className="title">Next Word Predictor</h1>
        <p className="subtitle">Powered by n-gram statistical model · Python backend</p>
      </header>

      <main className="main">
        <div className="search-wrapper">
          <div className={`search-box ${showDrop && suggestions.length ? "open" : ""}`}>
            <div className="input-row">
              <span className="prompt">›</span>
              <textarea
                ref={inputRef}
                className="search-input"
                value={text}
                onChange={e => setText(e.target.value)}
                onKeyDown={handleKey}
                onFocus={() => suggestions.length && setShowDrop(true)}
                placeholder="Start typing a sentence…"
                rows={3}
                spellCheck={false}
              />
              {loading && <span className="spinner" />}
              {text && (
                <button className="clear-btn" onClick={() => {
                  setText(""); setSuggestions([]); setShowDrop(false); inputRef.current?.focus();
                }}>✕</button>
              )}
            </div>

            {showDrop && suggestions.length > 0 && (
              <ul className="dropdown">
                {suggestions.map((s, i) => (
                  <li
                    key={s.word}
                    className={`suggestion ${i === activeIdx ? "active" : ""}`}
                    onMouseDown={() => appendWord(s.word)}
                    onMouseEnter={() => setActiveIdx(i)}
                  >
                    <span className="word">{s.word}</span>
                    <span className="bar-wrap">
                      <span className="bar" style={{ width: `${Math.round(s.score * 100)}%` }} />
                    </span>
                    <span className="score">{Math.round(s.score * 100)}%</span>
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="hints">
            <span>↑↓ navigate</span>
            <span>·</span>
            <span>Tab to insert</span>
            <span>·</span>
            <span>Esc to close</span>
          </div>
        </div>

        <div className="stats">
          <div className="stat"><span className="val">{wordCount}</span><span className="label">words</span></div>
          <div className="stat"><span className="val">{text.length}</span><span className="label">chars</span></div>
          <div className="stat"><span className="val">{suggestions.length}</span><span className="label">predictions</span></div>
        </div>
      </main>
    </div>
  );
}
