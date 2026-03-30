@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:       #0b0c0f;
  --surface:  #13151a;
  --border:   #222530;
  --border-hi:#3a3f52;
  --accent:   #5b6ef5;
  --accent2:  #a78bfa;
  --text:     #e2e4f0;
  --muted:    #5c6079;
  --green:    #4ade80;
  --radius:   12px;
}

body {
  background: var(--bg);
  color: var(--text);
  font-family: 'DM Sans', sans-serif;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}

/* ── Background grid ── */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(91,110,245,.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(91,110,245,.04) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
  z-index: 0;
}

.app { position: relative; z-index: 1; max-width: 720px; margin: 0 auto; padding: 60px 24px 80px; }

/* ── Header ── */
.header { text-align: center; margin-bottom: 52px; }

.logo {
  display: inline-flex; align-items: center; gap: 4px;
  font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 500;
  letter-spacing: .15em; text-transform: uppercase;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 6px; padding: 5px 12px; margin-bottom: 20px;
}
.logo-bracket { color: var(--accent); }
.logo-text    { color: var(--muted); }

.title {
  font-family: 'JetBrains Mono', monospace;
  font-size: clamp(26px, 5vw, 40px);
  font-weight: 700;
  letter-spacing: -.02em;
  background: linear-gradient(135deg, #fff 40%, var(--accent2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 13px; color: var(--muted);
  font-family: 'JetBrains Mono', monospace; letter-spacing: .05em;
}

/* ── Search box ── */
.search-wrapper { position: relative; }

.search-box {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  transition: border-color .2s, box-shadow .2s;
  overflow: hidden;
}
.search-box:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(91,110,245,.12), 0 8px 32px rgba(0,0,0,.4);
}
.search-box.open { border-radius: var(--radius) var(--radius) 0 0; border-bottom-color: var(--border); }

.input-row { display: flex; align-items: flex-start; gap: 10px; padding: 16px 18px; }

.prompt-symbol {
  font-family: 'JetBrains Mono', monospace;
  font-size: 22px; color: var(--accent);
  margin-top: 2px; user-select: none; flex-shrink: 0;
}

.search-input {
  flex: 1;
  background: transparent; border: none; outline: none; resize: none;
  font-family: 'JetBrains Mono', monospace;
  font-size: 15px; font-weight: 400;
  color: var(--text); line-height: 1.65;
  caret-color: var(--accent);
}
.search-input::placeholder { color: var(--muted); }

.spinner {
  width: 16px; height: 16px; flex-shrink: 0; margin-top: 6px;
  border: 2px solid var(--border-hi); border-top-color: var(--accent);
  border-radius: 50%; animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.clear-btn {
  background: none; border: none; color: var(--muted); cursor: pointer;
  font-size: 13px; padding: 4px 6px; border-radius: 4px; flex-shrink: 0; margin-top: 2px;
  transition: color .15s, background .15s;
}
.clear-btn:hover { color: var(--text); background: var(--border); }

/* ── Dropdown ── */
.dropdown {
  list-style: none;
  border-top: 1px solid var(--border);
  max-height: 320px; overflow-y: auto;
  background: var(--surface);
  border-radius: 0 0 var(--radius) var(--radius);
  box-shadow: 0 16px 40px rgba(0,0,0,.5);
}
.dropdown::-webkit-scrollbar { width: 4px; }
.dropdown::-webkit-scrollbar-track { background: transparent; }
.dropdown::-webkit-scrollbar-thumb { background: var(--border-hi); border-radius: 2px; }

.suggestion {
  display: flex; align-items: center; gap: 12px;
  padding: 11px 18px; cursor: pointer;
  transition: background .12s;
  border-bottom: 1px solid var(--border);
}
.suggestion:last-child { border-bottom: none; }
.suggestion:hover, .suggestion.active { background: rgba(91,110,245,.08); }
.suggestion.active .suggestion-word { color: var(--accent2); }

.suggestion-word {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px; font-weight: 500;
  width: 140px; flex-shrink: 0;
  transition: color .12s;
}

.suggestion-bar-wrap {
  flex: 1; height: 3px; background: var(--border);
  border-radius: 2px; overflow: hidden;
}
.suggestion-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  border-radius: 2px;
  transition: width .3s ease;
}

.suggestion-score {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; color: var(--muted); width: 36px; text-align: right;
}

/* ── Keyboard hints ── */
.hints {
  display: flex; gap: 16px; justify-content: center; margin-top: 12px;
}
.hints span {
  font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--muted);
}
.hints span + span::before { content: '·'; margin-right: 16px; }

/* ── Stats ── */
.stats {
  display: flex; justify-content: center; gap: 40px; margin-top: 48px;
}
.stat { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.stat-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 28px; font-weight: 700;
  background: linear-gradient(135deg, var(--text), var(--accent2));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.stat-label { font-size: 11px; color: var(--muted); letter-spacing: .08em; text-transform: uppercase; }

/* API status badges */
.api-warn {
  margin-top: 12px; font-size: 12px; color: #f59e0b;
  background: rgba(245,158,11,.08); border: 1px solid rgba(245,158,11,.2);
  border-radius: 6px; padding: 6px 14px; display: inline-block;
  font-family: 'JetBrains Mono', monospace;
}
.api-ok {
  margin-top: 12px; font-size: 12px; color: #4ade80;
  font-family: 'JetBrains Mono', monospace; letter-spacing: .05em;
}
