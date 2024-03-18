import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';

function App() {
  const [selectedSymbol, setSelectedSymbol] = useState(null);

  return (
    <div>
      <h1>Stock Visualizer</h1>
      <StockSelector onSelect={setSelectedSymbol} />
      {selectedSymbol && <TimeSeries symbol={selectedSymbol} />}
    </div>
  );
}

function StockSelector({ onSelect }) {
  const [symbols, setSymbols] = useState([]);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/symbols/`)
      .then(response => response.json())
      .then(data => setSymbols(data));
  }, []);

  return (
    <select onChange={(e) => onSelect(e.target.value)}>
      {symbols.map(symbol => (
        <option key={symbol} value={symbol}>{symbol}</option>
      ))}
    </select>
  );
}

function TimeSeries({ symbol }) {
  const [timeSeries, setTimeSeries] = useState([]);

  useEffect(() => {
    if (symbol) {
      fetch(`${process.env.REACT_APP_API_URL}/time_series/${symbol}/`)
        .then(response => response.json())
        .then(data => setTimeSeries(data));
    }
  }, [symbol]);

  return (
    <Plot
      data={[
        {
          x: timeSeries.map(entry => entry.date),
          y: timeSeries.map(entry => entry.adj_close),
          type: 'scatter',
          mode: 'lines+markers',
          marker: { color: 'black' },
        },
      ]}
      layout={{ width: 720, height: 440, title: `Time Series for ${symbol}` }}
    />
  );
}

export default App;

