import React, { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [num, setNum] = useState(1);
  const [result, setResult] = useState("");

  const handlePredict = async () => {
    const res = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ text, num })
    });

    const data = await res.json();
    setResult(data.result);
  };

  return (
    <div className="container">
      <h1>AI Next Word Predictor</h1>

      <input
        type="text"
        placeholder="Enter text"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <input
        type="number"
        value={num}
        onChange={(e) => setNum(e.target.value)}
      />

      <button onClick={handlePredict}>Predict</button>

      <h3>Output:</h3>
      <p>{result}</p>
    </div>
  );
}

export default App;
