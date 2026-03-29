import React, { useState, useEffect } from 'react';
import './App.css';

const API = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// ── Sub-components ──────────────────────────────────────────────────────────

function Header({ health }) {
  return (
    <header className="header">
      <div className="header-inner">
        <div className="logo-group">
          <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
            <rect width="36" height="36" rx="10" fill="url(#g1)"/>
            <path d="M8 26L14 10L18 20L22 14L28 26" stroke="#fff" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"/>
            <defs><linearGradient id="g1" x1="0" y1="0" x2="36" y2="36"><stop stopColor="#7c6dff"/><stop offset="1" stopColor="#ff6db4"/></linearGradient></defs>
          </svg>
          <div>
            <h1 className="logo-text">NextWord<span className="logo-accent">AI</span></h1>
            <p className="logo-sub">Bidirectional LSTM · Next-Word Prediction</p>
          </div>
        </div>
        {health ? (
          <div className="badge online"><span className="dot"/><span>Model Online</span><span className="vocab">vocab {health.vocab_size}</span></div>
        ) : (
          <div className="badge offline"><span className="dot"/><span>Connecting…</span></div>
        )}
      </div>
      <div className="header-bar"/>
    </header>
  );
}

const PRESETS = [
  'The future of artificial intelligence',
  'Machine learning is a',
  'Deep neural networks can',
  'The ocean covers more than',
  'Science and technology continue to',
];

function PredictionPanel({ form, setForm, onPredict, loading }) {
  const set = (k, v) => setForm(p => ({ ...p, [k]: v }));
  return (
    <div className="card">
      <div className="panel-header">
        <div><p className="label">Input</p><h2 className="card-title">Seed Text & Parameters</h2></div>
        <span className="kbd">⌘↵ to run</span>
      </div>

      {/* Seed input */}
      <div className="field">
        <label className="field-label">Seed Text</label>
        <textarea className="seed-input" rows={3} placeholder="Start typing… e.g. 'The future of'"
          value={form.seedText} onChange={e => set('seedText', e.target.value)}
          onKeyDown={e => { if ((e.ctrlKey||e.metaKey) && e.key==='Enter') onPredict(); }}
        />
        <div className="presets">
          {PRESETS.map(p => <button key={p} className="chip" onClick={() => set('seedText', p)}>{p}</button>)}
        </div>
      </div>

      {/* Controls */}
      <div className="controls-grid">
        <div className="ctrl">
          <label className="field-label">Words to Predict <span className="val">{form.nWords}</span></label>
          <input type="range" min={1} max={50} value={form.nWords} onChange={e => set('nWords', +e.target.value)} className="slider s-accent"/>
          <div className="ticks">{[1,10,20,30,40,50].map(n=><span key={n} onClick={()=>set('nWords',n)}>{n}</span>)}</div>
        </div>
        <div className="ctrl">
          <label className="field-label">Temperature <span className="val">{form.temperature.toFixed(1)}</span></label>
          <input type="range" min={0.1} max={2.0} step={0.1} value={form.temperature}
            onChange={e => set('temperature', +e.target.value)} className="slider s-pink"
            disabled={form.mode==='beam'}/>
          <p className="hint">{form.temperature<0.5?'🧊 Conservative':form.temperature<1.2?'⚖ Balanced':'🔥 Creative'}</p>
        </div>
        <div className="ctrl">
          <label className="field-label">Top-K Candidates <span className="val">{form.topK}</span></label>
          <input type="range" min={1} max={20} value={form.topK} onChange={e => set('topK', +e.target.value)}
            className="slider s-teal" disabled={form.mode==='beam'}/>
        </div>
        <div className="ctrl">
          <label className="field-label">Decoding Mode</label>
          <div className="mode-toggle">
            {[{id:'sample',icon:'🎲',label:'Sampling'},{id:'beam',icon:'🔭',label:'Beam Search'}].map(m=>(
              <button key={m.id} className={`mode-btn ${form.mode===m.id?'active':''}`} onClick={()=>set('mode',m.id)}>
                <span>{m.icon}</span><span>{m.label}</span>
              </button>
            ))}
          </div>
          <p className="hint">{form.mode==='beam'?'Deterministic — returns top-3 sentences':'Stochastic — uses temperature & top-K'}</p>
        </div>
      </div>

      <button className={`run-btn ${loading?'loading':''}`} onClick={onPredict} disabled={loading||!form.seedText.trim()}>
        {loading ? <><span className="spinner"/>Predicting…</> : <><span>⚡</span>Predict Next Words</>}
      </button>
    </div>
  );
}

function ResultPanel({ result }) {
  const [copied, setCopied] = useState(false);
  const words   = result.full_sentence.split(' ');
  const seedLen = result.seed.split(' ').length;
  const copy = () => { navigator.clipboard.writeText(result.full_sentence); setCopied(true); setTimeout(()=>setCopied(false),1800); };
  return (
    <div className="card" style={{animationDelay:'0.1s'}}>
      <div className="panel-header">
        <div><p className="label">Output</p><h2 className="card-title">Predicted Sentence</h2></div>
        <div style={{display:'flex',gap:'0.6rem',alignItems:'center'}}>
          <span className="badge online" style={{fontSize:'0.7rem'}}><span className="dot"/>{result.mode==='beam_search'?'Beam Search':'Sampling'}</span>
          <button className="copy-btn" onClick={copy}>{copied?'✓ Copied':'⎘ Copy'}</button>
        </div>
      </div>
      <div className="sentence-display">
        {words.map((w,i) => (
          <span key={i} className={i>=seedLen?'word predicted':'word seed'}
            style={i>=seedLen?{animationDelay:`${(i-seedLen)*0.08}s`}:{}}>
            {w}{' '}
          </span>
        ))}
      </div>
      <div className="stats-row">
        {[['Seed words',seedLen],['Predicted',result.predicted_words?.length,'accent'],['Total',words.length],['Chars',result.full_sentence.length]].map(([l,v,c])=>(
          <div key={l} className="stat"><span className={`stat-val ${c?'stat-accent':''}`}>{v}</span><span className="stat-label">{l}</span></div>
        ))}
      </div>
    </div>
  );
}

function StepsPanel({ steps }) {
  const [open, setOpen] = useState(0);
  return (
    <div className="card" style={{animationDelay:'0.2s'}}>
      <p className="label">Step-by-Step</p>
      <h2 className="card-title">Prediction Breakdown</h2>
      <p className="hint" style={{marginBottom:'1rem'}}>Click each step to see candidate probabilities.</p>
      <div className="steps-list">
        {steps.map((step,i) => {
          const max = Math.max(...step.candidates.map(c=>c.probability));
          return (
            <div key={i} className={`step-row ${open===i?'open':''}`}>
              <button className="step-summary" onClick={()=>setOpen(open===i?-1:i)}>
                <span className="step-num">#{i+1}</span>
                <span className="step-chosen">{step.chosen}</span>
                <span className="step-preview">…{step.input.slice(-30)}</span>
                <span>{open===i?'▲':'▼'}</span>
              </button>
              {open===i && (
                <div className="step-detail">
                  <p className="hint" style={{marginBottom:'0.75rem'}}>Context: <em>"{step.input}"</em></p>
                  {step.candidates.map((c,j)=>(
                    <div key={j} className={`cand-row ${c.word===step.chosen?'chosen':''}`}>
                      <span className="cand-rank">#{j+1}</span>
                      <span className="cand-word">{c.word}</span>
                      <div className="bar-wrap"><div className="bar" style={{width:`${(c.probability/max)*100}%`,animationDelay:`${j*0.05}s`}}/></div>
                      <span className="cand-prob">{c.probability.toFixed(1)}%</span>
                      {c.word===step.chosen && <span className="chosen-tag">✓</span>}
                    </div>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function BeamPanel({ beams, seed }) {
  const [copied, setCopied] = useState(null);
  const copy = (t,i) => { navigator.clipboard.writeText(t); setCopied(i); setTimeout(()=>setCopied(null),1800); };
  return (
    <div className="card" style={{animationDelay:'0.2s'}}>
      <p className="label">Beam Search</p>
      <h2 className="card-title">Top Candidate Sequences</h2>
      <div style={{display:'flex',flexDirection:'column',gap:'0.75rem',marginTop:'1rem'}}>
        {beams.map((b,i)=>{
          const words = b.sentence.split(' '), sl = seed.split(' ').length;
          return (
            <div key={i} className={`beam-item ${i===0?'best':''}`}>
              <div className="beam-rank"><span className="rank-num">#{i+1}</span>{i===0&&<span className="best-tag">Best</span>}</div>
              <div style={{flex:1}}>
                <div className="sentence-display" style={{padding:'0.75rem',marginBottom:'0.5rem',fontSize:'0.95rem'}}>
                  {words.map((w,j)=><span key={j} className={j>=sl?'word predicted':'word seed'}>{w} </span>)}
                </div>
                <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
                  <span className="hint">score: {b.score}</span>
                  <button className="copy-btn" onClick={()=>copy(b.sentence,i)}>{copied===i?'✓':'⎘'}</button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ── Main App ────────────────────────────────────────────────────────────────
export default function App() {
  const [form, setForm]     = useState({ seedText:'', nWords:5, temperature:1.0, topK:5, mode:'sample' });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError]   = useState(null);
  const [health, setHealth] = useState(null);

  useEffect(() => {
    fetch(`${API}/health`).then(r=>r.json()).then(setHealth).catch(()=>setHealth(null));
  }, []);

  const predict = async () => {
    if (!form.seedText.trim()) return;
    setLoading(true); setError(null); setResult(null);
    try {
      const res = await fetch(`${API}/predict`, {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ seed_text:form.seedText, n_words:form.nWords,
          temperature:form.temperature, top_k:form.topK, mode:form.mode }),
      });
      if (!res.ok) throw new Error(await res.text());
      setResult(await res.json());
    } catch(e) { setError(e.message); }
    finally { setLoading(false); }
  };

  return (
    <div className="app">
      <div className="noise"/>
      <div className="grid-bg"/>
      <Header health={health}/>
      <main className="main">
        <PredictionPanel form={form} setForm={setForm} onPredict={predict} loading={loading}/>
        {error && <div className="error-banner">⚠ {error}</div>}
        {result && <>
          <ResultPanel result={result}/>
          {result.mode==='sampling' && result.steps?.length>0 && <StepsPanel steps={result.steps}/>}
          {result.mode==='beam_search' && result.beam_results?.length>0 && <BeamPanel beams={result.beam_results} seed={result.seed}/>}
        </>}
      </main>
      <footer className="footer">
        <span>NextWordAI · Bidirectional LSTM · Flask + React</span>
        <a href="https://github.com/yourusername/next-word-prediction" target="_blank" rel="noreferrer">⭐ GitHub</a>
      </footer>
    </div>
  );
}
