import React, { useState, useEffect, useMemo } from 'react';
import Plot from 'react-plotly.js';
import { Container, Row, Col, Form, Card, Table } from 'react-bootstrap';
import { useTable, useFlexLayout } from 'react-table';

export default function App() {
  const [selectedSymbol, setSelectedSymbol] = useState(null);

  return (
    <Container>
      <Row className="justify-content-md-center">
        <Col>
          <h1 className="text-center mb-4">Stock Visualizer</h1>
          <StockSelector onSelect={setSelectedSymbol} />
          {selectedSymbol && (
            <>
            <Row>
              <Col md={6}>
                <AdjustedStockPricePlot symbol={selectedSymbol} />
              </Col>
              <Col md={6}>
                <EarningsPerSharePlot symbol={selectedSymbol} />
              </Col>
            </Row>
            <AnalystRatingTable selectedSymbols={[selectedSymbol]} />
            <FinancialPerformanceTable selectedSymbol={selectedSymbol} />
          </>
          )}
        </Col>
      </Row>
    </Container>
  );
}


function StockSelector({ onSelect }) {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/stocks/`)
      .then(response => response.json())
      .then(data => setStocks(data));
  }, []);

  return (
    <Form.Group controlId="stockSelect">
      <Form.Label>Select a Stock</Form.Label>
      <Form.Control as="select" onChange={(e) => onSelect(e.target.value)}>
        {stocks.map(stock => (
          <option key={stock.symbol} value={stock.symbol}>{stock.name}</option>
        ))}
      </Form.Control>
    </Form.Group>
  );
}

function AdjustedStockPricePlot({ symbol }) {
  const [timeSeries, setTimeSeries] = useState([]);

  useEffect(() => {
    if (symbol) {
      fetch(`${process.env.REACT_APP_API_URL}/adjusted_stock_price_ts/${symbol}/`)
        .then(response => response.json())
        .then(data => setTimeSeries(data));
    }
  }, [symbol]);

  return (
    <Card>
      <Card.Body>
        <Plot
          data={[
            {
              x: timeSeries.map(entry => entry.date),
              y: timeSeries.map(entry => entry.adj_close),
              type: 'scatter',
              mode: 'lines+markers',
              marker: { color: 'green' },
            },
          ]}
          layout={{ width: 720, height: 440, title: `Adjusted Stock Price for ${symbol}` }}
        />
      </Card.Body>
    </Card>
  );
}


const EarningsPerSharePlot = ({ symbol }) => {
  const [epsData, setEpsData] = useState([]);

  useEffect(() => {
    if (symbol) {
      fetch(`${process.env.REACT_APP_API_URL}/earnings/${symbol}/`)
        .then(response => response.json())
        .then(data => setEpsData(data));
    }
  }, [symbol]);

  const epsPlotData = [
    {
      x: epsData.map(entry => entry.fiscal_date_ending),
      y: epsData.map(entry => entry.reported_eps),
      type: 'scatter',
      mode: 'lines+markers',
      name: 'Reported EPS',
      yaxis: 'y1',
    },
    {
      x: epsData.map(entry => entry.fiscal_date_ending),
      y: epsData.map(entry => (entry.surprise_percentage)),
      type: 'bar',
      name: 'Surprise Percentage',
      yaxis: 'y2',
    },
  ];

  const layout = {
    width: 720,
    height: 440,
    title: `EPS Metrics for ${symbol}`,
    yaxis: { // First y-axis configuration (left)
      title: 'Reported EPS ($)',
      titlefont: {color: '#1f77b4'},
      tickfont: {color: '#1f77b4'},
    },
    yaxis2: { // Second y-axis configuration (right)
      title: 'Surprise Percentage (%)',
      titlefont: {color: '#ff7f0e'},
      tickfont: {color: '#ff7f0e'},
      overlaying: 'y',
      side: 'right',
    },
  };

  return (
    <Card>
      <Card.Body>
        <Plot
          data={epsPlotData}
          layout={layout}
        />
      </Card.Body>
    </Card>
  );
};



const AnalystRatingTable = ({ selectedSymbols }) => {
  const [quarterlyData, setQuarterlyData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const dataPromises = selectedSymbols.map(symbol =>
          fetch(`${process.env.REACT_APP_API_URL}/quarterly_overview/${symbol}/`)
            .then(response => response.json())
        );
        const responses = await Promise.all(dataPromises);
        const data = responses.flat(); // Flattening array of arrays if necessary
        setQuarterlyData(data);
      } catch (error) {
        console.error('Failed to fetch quarterly data', error);
      }
    };

    fetchData();
  }, [selectedSymbols]);

  const columns = [
    { label: 'Name', accessor: 'stock__name' },
    { label: 'Ticker', accessor: 'stock__symbol' },
    { label: 'Analyst Target Price', accessor: 'analyst_target_price', type: 'currency'},
    { label: 'Analyst Rating Strong Buy', accessor: 'analyst_rating_strong_buy' },
    { label: 'Analyst Rating Buy', accessor: 'analyst_rating_buy' },
    { label: 'Analyst Rating Hold', accessor: 'analyst_rating_hold' },
    { label: 'Analyst Rating Sell', accessor: 'analyst_rating_sell' },
    { label: 'Analyst Rating Strong Sell', accessor: 'analyst_rating_strong_sell' },
    // You can add more columns here based on your model fields
  ];

  return (
    <Table striped bordered hover>
      <thead>
        <tr>
          {columns.map(column => (
            <th key={column.accessor}>{column.label}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {quarterlyData.map((item, index) => (
          <tr key={index}>
            {columns.map(column => (
              <td key={column.accessor}>
                {formatValue(item[column.accessor], column.type)}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </Table>
  );
};


// Helper function to abbreviate large numbers
const abbreviateNumber = (value) => {
  let newValue = value;
  if (value >= 1e9) {
    newValue = (value / 1e9).toFixed(1) + 'B';
  } else if (value >= 1e6) {
    newValue = (value / 1e6).toFixed(1) + 'M';
  } else if (value >= 1e3) {
    newValue = (value / 1e3).toFixed(1) + 'K';
  }
  return newValue;
};

// Updated formatValue function to handle null and formatting
const formatValue = (value, type) => {
  if (value === null || value === undefined) {
    return ''; // Return empty string for null or undefined values
  }

  switch (type) {
    case 'currency':
      return `$${abbreviateNumber(value)}`;
    case 'percentage':
      return `${Number(value).toFixed(2)}%`;
    case 'ratio':
      return Number(value).toFixed(2);
    default:
      return value;
  }
};

// Component for Financial Performance Table
const FinancialPerformanceTable = ({ selectedSymbol }) => {
  const [financialData, setFinancialData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/quarterly_overview/${selectedSymbol}/`);
        const data = await response.json();
        setFinancialData(data);
      } catch (error) {
        console.error('Failed to fetch financial performance data', error);
      }
    };

    if (selectedSymbol) {
      fetchData();
    }
  }, [selectedSymbol]);

  const metrics = [
    { label: 'Name', accessor: 'stock__name' },
    { label: 'Ticker', accessor: 'stock__symbol' },
    { label: 'Revenue (TTM)', accessor: 'revenue_ttm', type: 'currency' },
    { label: 'Gross Profit (TTM)', accessor: 'gross_profit_ttm', type: 'currency' },
    { label: 'Diluted EPS (TTM)', accessor: 'diluted_eps_ttm', type: 'currency' },
    { label: 'EBITDA', accessor: 'ebitda', type: 'currency' },
    { label: 'P/E Ratio', accessor: 'pe_ratio', type: 'ratio' },
    { label: 'PEG Ratio', accessor: 'peg_ratio', type: 'ratio' },
    // What is this book value?  Perhaps in billions?
    { label: 'Book Value', accessor: 'book_value', type: 'currency' },
    { label: 'Profit Margin', accessor: 'profit_margin', type: 'percentage' },
    { label: 'Operating Margin (TTM)', accessor: 'operating_margin_ttm', type: 'percentage' },
    { label: 'Return on Assets (TTM)', accessor: 'return_on_assets_ttm', type: 'percentage' },
    { label: 'Return on Equity (TTM)', accessor: 'return_on_equity_ttm', type: 'percentage' },
    { label: 'Market Capitalization', accessor: 'market_capitalization', type: 'currency' },
  ];

  return (
    <Table striped bordered hover>
      <thead>
        <tr>
          {metrics.map(metric => (
            <th key={metric.accessor}>{metric.label}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {financialData.length > 0 ? (
          <tr>
            {metrics.map(metric => (
              <td key={metric.accessor}>
                {formatValue(financialData[0][metric.accessor], metric.type)}
              </td>
            ))}
          </tr>
        ) : (
          <tr>
            <td colSpan={metrics.length}>Loading...</td>
          </tr>
        )}
      </tbody>
    </Table>
  );
};






// function QuarterlyOverview({ symbol }) {
//   const [quarterlyData, setQuarterlyData] = useState([]);

//   useEffect(() => {
//       if (symbol) {
//           fetch(`http://127.0.0.1:8000/quarterly_overview/${symbol}/`)
//               .then(response => response.json())
//               .then(data => setQuarterlyData(data));
//       }
//   }, [symbol]);

//   if (!quarterlyData.length) return null;

//   const keys = Object.keys(quarterlyData[0]);

//   return (
//       <Card>
//           <Card.Body>
//               <div className="grid-table">
//                   {keys.map(key => (
//                       <div key={key} className="header">{key}</div>
//                   ))}
//                   {quarterlyData.map((data, rowIndex) => (
//                       keys.map(key => (
//                           <div key={`${key}-${rowIndex}`}>{data[key]}</div>
//                       ))
//                   ))}
//               </div>
//           </Card.Body>
//       </Card>
//   );
// }


