import React, { useState, useEffect, useMemo } from 'react';
import Plot from 'react-plotly.js';
import { Container, Row, Col, Form, Card, Table } from 'react-bootstrap';
import { useTable, useFlexLayout } from 'react-table';
import Select from 'react-select';

export default function App() {
  const [selectedSymbol, setSelectedSymbol] = useState(null);

  const [selectedBalanceSheetMetrics, setSelectedBalanceSheetMetrics] = (
    useState([balanceSheetMetrics[0].value])
  );

  const [selectedIncomeStatementMetrics, setSelectedIncomeStatementMetrics] = (
    useState([incomeStatementMetrics[0].value])
  );

  const [selectedCashFlowMetrics, setSelectedCashFlowMetrics] = (
    useState([cashFlowMetrics[0].value])
  );


  const { data: balanceSheetData, loading: loadingBalanceSheet, error: errorBalanceSheet } = (
    useFetchFinancialData(selectedSymbol, 'balance_sheet')
  );
  const { data: incomeStatementData, loading: loadingIncomeStatement, error: errorIncomeStatement } = (
    useFetchFinancialData(selectedSymbol, 'income_statement')
  );
  const { data: cashFlowData, loading: loadingCashFlow, error: errorCashFlow } = (
    useFetchFinancialData(selectedSymbol, 'cash_flow')
  );

  const balanceSheetSelector = (
    <FinancialMetricsSelector
      label="Select Balance Sheet Metrics"
      metrics={balanceSheetMetrics}
      onSelect={setSelectedBalanceSheetMetrics}
      defaultSelected={['total_liabilities', 'total_shareholder_equity', 'total_assets']}
    />
  );

  const balanceSheetPlot = (
    <FinancialMetricPlot
      data={balanceSheetData}
      selectedMetrics={selectedBalanceSheetMetrics}
      metricsList={balanceSheetMetrics}
      titlePrefix="Balance Sheet"
    />
  );


  const incomeStatementSelector = (
    <FinancialMetricsSelector
      label="Select Income Statement Metrics"
      metrics={incomeStatementMetrics}
      onSelect={setSelectedIncomeStatementMetrics}
      defaultSelected={['net_income', 'operating_income', 'gross_profit']}
    />
  );

  
  const incomeStatementPlot = (
    <FinancialMetricPlot
      data={incomeStatementData}
      selectedMetrics={selectedIncomeStatementMetrics}
      metricsList={incomeStatementMetrics}
      titlePrefix="Income Statement"
    />
  );

  const cashFlowSelector = (<FinancialMetricsSelector
    label="Select Cash Flow Metrics"
    metrics={cashFlowMetrics}
    onSelect={setSelectedCashFlowMetrics}
    defaultSelected={['operating_cashflow', 'cashflow_from_investment', 'cashflow_from_financing']}

  />
  );

  const cashFlowPlot = (
    <FinancialMetricPlot
      data={cashFlowData}
      selectedMetrics={selectedCashFlowMetrics}
      metricsList={cashFlowMetrics}
      titlePrefix="Cash Flow"
    />
  );

    // // Prepare the components outside the return statement for cleaner JSX
    // const balanceSheetComponent = renderFinancialData(
    //   loadingBalanceSheet,
    //   errorBalanceSheet,
    //   balanceSheetPlot,
    //   balanceSheetData,
    //   selectedBalanceSheetMetrics
    // );
  
    // const incomeStatementComponent = renderFinancialData(
    //   loadingIncomeStatement,
    //   errorIncomeStatement,
    //   incomeStatementPlot,
    //   incomeStatementData,
    //   selectedIncomeStatementMetrics
    // );
  
    // const cashFlowComponent = renderFinancialData(
    //   loadingCashFlow,
    //   errorCashFlow,
    //   cashFlowPlot,
    //   cashFlowData,
    //   selectedCashFlowMetrics
    // );
  
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
              <Row>
                <AnalystRatingTable selectedSymbols={[selectedSymbol]} />
                <FinancialPerformanceTable selectedSymbol={selectedSymbol} />
                {balanceSheetSelector}
                {balanceSheetPlot}
                {incomeStatementSelector}
                {incomeStatementPlot}
                {cashFlowSelector}
                {cashFlowPlot}
                </Row>
          </>
          )}
        </Col>
      </Row>
    </Container>
  );
}

/**
 * Custom hook to fetch financial data for a given symbol and financial statement type.
 *
 * @param {string} selectedSymbol - The stock symbol for which to fetch the data.
 * @param {string} path - The API endpoint path segment corresponding to the financial data type (e.g., 'balance_sheet').
 * @returns {Object} An object containing the fetched data, loading state, and any error occurred.
 */
function useFetchFinancialData(selectedSymbol, path) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (selectedSymbol) {
      setLoading(true);
      const fetchData = async () => {
        try {
          const response = await fetch(`${process.env.REACT_APP_API_URL}/${path}/${selectedSymbol}/`);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const json = await response.json();
          setData(json);
        } catch (error) {
          setError(error);
          console.error("Failed to fetch data:", error);
        } finally {
          setLoading(false);
        }
      };

      fetchData();
    }
  }, [selectedSymbol, path]);

  return { data, loading, error };
}


/**
 * Renders the financial data component based on the current loading and error states.
 *
 * This function conditionally renders a loading message, an error message, or the financial data component
 * depending on whether the data is currently being fetched, if an error has occurred during data fetching,
 * or if the data is ready to be displayed, respectively.
 *
 * @param {boolean} loading - Indicates whether the data is currently being loaded.
 * @param {Object} error - An error object that might have occurred during data fetching. If no error has occurred, this should be null.
 * @param {React.Component} Component - The React component that should be rendered when data is ready and there are no errors. This component is expected to accept `data` and `selectedMetrics` as props.
 * @param {Array} data - The data to be passed to the `Component` for rendering. Should be an array of data points.
 * @param {Array} selectedMetrics - The metrics selected by the user, to be passed to the `Component`.
 *
 * @returns {React.Element} A React element that is either a loading message, an error message, or the `Component` rendered with `data` and `selectedMetrics`.
 */
function renderFinancialData(loading, error, Component, data, selectedMetrics) {
  if (loading) {
    return <div>Loading data...</div>;
  }

  if (error) {
    return <div>Error fetching data: {error.message}</div>;
  }

  return <Component data={data} selectedMetrics={selectedMetrics} />;
}



// STOCK SELECTOR ----------------------------------------------------------------------------
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


// ADJUSTED STOCK PRICE PLOT ----------------------------------------------------------------------------
function AdjustedStockPricePlot({ symbol }) {
  const [timeSeries, setTimeSeries] = useState([]);

  useEffect(() => {
    if (symbol) {
      fetch(`${process.env.REACT_APP_API_URL}/adjusted_stock_price/${symbol}/`)
        .then(response => response.json())
        .then(data => setTimeSeries(data));
    }
  }, [symbol]);

  const layout = {
    autosize: true,
    margin: {
      l: '5%',
      r: '5%',
      b: '5%',
      t: '5%',
    },
    title: `Adjusted Stock Price for ${symbol}`,
  };

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
          layout={layout}
          useResizeHandler={true}
          style={{ width: "100%", height: "100%" }}
        />
      </Card.Body>
    </Card>
  );
}


// EARNINGS PER SHARE PLOT ----------------------------------------------------------------------------
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
      name: 'EPS',
      yaxis: 'y1',
    },
    {
      x: epsData.map(entry => entry.fiscal_date_ending),
      y: epsData.map(entry => (entry.surprise_percentage)),
      type: 'bar',
      name: 'Surprise %',
      yaxis: 'y2',
    },
  ];

  const layout = {
    autosize: true,
    margin: {
      l: '0%',
      r: '5%',
      b: '5%',
      t: '5%',
    },
    title: `EPS Metrics for ${symbol}`,
    showlegend: false,
    yaxis: { // First y-axis configuration (left)
      title: 'Reported EPS ($)',
      titlefont: {color: '#1f77b4'},
      tickfont: {color: '#1f77b4'},
    },
    yaxis2: { // Second y-axis configuration (right)
      title: 'Surprise %',
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
          useResizeHandler={true}
          style={{ width: "100%", height: "100%" }}
        />
      </Card.Body>
    </Card>
  );
};


// ANALYST RATING TABLE ----------------------------------------------------------------------------
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
    <Table striped bordered hover responsive>
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



// FINANCIAL PERFORMANCE TABLE ----------------------------------------------------------------------------
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
    <Table striped bordered hover responsive>
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


// HELPERS FOR BALANCE SHEET, INCOME STATEMENT, AND CASH FLOW STATEMENT METRICS ----------------------------------------------------------------------------

function FinancialMetricsSelector({ label, metrics, onSelect, defaultSelected }) {
  const options = metrics.map(metric => ({
    value: metric.value,
    label: metric.label,
  }));

  // Convert defaultSelected to the format expected by react-select
  const defaultValue = options.filter(option => defaultSelected.includes(option.value));

  // Notify parent component of the default selections on mount
  useEffect(() => {
    onSelect(defaultSelected);
  }, []); // Empty dependency array to run only once on mount

  const handleChange = selectedOptions => {
    const values = selectedOptions ? selectedOptions.map(option => option.value) : [];
    onSelect(values);
  };

  return (
    <Form.Group controlId={`${label.replace(/\s/g, '')}MetricSelect`}>
      <Form.Label>{label}</Form.Label>
      <Select
        isMulti
        options={options}
        defaultValue={defaultValue}
        onChange={handleChange}
        className="basic-multi-select"
        classNamePrefix="select"
      />
    </Form.Group>
  );
}



// function FinancialMetricPlot({ data, selectedMetrics, metricsList, titlePrefix }) {
//   if (!data || data.length === 0 || !selectedMetrics || selectedMetrics.length === 0) {
//     return <div>No data or metrics selected.</div>;
//   }

//   const layout = {
//     autosize: true,
//     title: `Plot of Various ${titlePrefix} Metrics for ${data[0].stock_id || 'Unknown Stock'}`,
//   };

//   const plotData = selectedMetrics.map(metric => {
//     const metricLabel = metricsList.find(m => m.value === metric)?.label || 'Unknown Metric';
//     return {
//       x: data.map(entry => entry.date),
//       y: data.map(entry => entry[metric]),
//       type: 'scatter',
//       mode: 'lines+markers',
//       name: metricLabel,
//     };
//   });

//   return (
//     <Plot data={plotData} layout={layout} useResizeHandler={true} style={{ width: "100%", height: "100%" }} />
//   );
// }

// function FinancialMetricPlot({ data, selectedMetrics, metricsList, titlePrefix }) {
//   const [plotData, setPlotData] = useState([]);

//   useEffect(() => {
//     if (data && data.length > 0 && selectedMetrics && selectedMetrics.length > 0) {
//       const newPlotData = selectedMetrics.map(metric => {
//         const metricLabel = metricsList.find(m => m.value === metric)?.label || 'Unknown Metric';
//         return {
//           x: data.map(entry => entry.date),
//           y: data.map(entry => entry[metric]),
//           type: 'scatter',
//           mode: 'lines+markers',
//           name: metricLabel,
//         };
//       });
//       setPlotData(newPlotData);
//     }
//   }, [data, selectedMetrics, metricsList]);  // Re-calculate plot data when dependencies change

//   if (!data || data.length === 0 || !selectedMetrics || selectedMetrics.length === 0) {
//     return <div>No data or metrics selected.</div>;
//   }

//   const layout = {
//     autosize: true,
//     title: `Plot of Various ${titlePrefix} Metrics for ${data[0]?.stock_id || 'Unknown Stock'}`,
//   };

//   return (
//     <Plot data={plotData} layout={layout} useResizeHandler={true} style={{ width: "100%", height: "100%" }} />
//   );
// }

function FinancialMetricPlot({ data, selectedMetrics, metricsList, titlePrefix }) {
  const [plotData, setPlotData] = useState([]);

  useEffect(() => {
    // Check if both data and selectedMetrics are ready
    if (data && data.length > 0 && selectedMetrics && selectedMetrics.length > 0) {
      const newPlotData = selectedMetrics.map(metric => {
        const metricLabel = metricsList.find(m => m.value === metric)?.label || 'Unknown Metric';
        return {
          x: data.map(entry => entry.date),
          y: data.map(entry => entry[metric]),
          type: 'scatter',
          mode: 'lines+markers',
          name: metricLabel,
        };
      });
      setPlotData(newPlotData);
    } else {
      // Clear plot data if the conditions are not met
      setPlotData([]);
    }
  }, [data, selectedMetrics, metricsList]);

  if (!plotData || plotData.length === 0) {
    return <div>No data or metrics selected.</div>;
  }

  const layout = {
    autosize: true,
    title: `Plot of Various ${titlePrefix} Metrics for ${data?.[0]?.stock_id || 'Unknown Stock'}`,
  };

  return (
    <Plot data={plotData} layout={layout} useResizeHandler={true} style={{ width: "100%", height: "100%" }} />
  );
}



// BALANCE SHEET METRICS ----------------------------------------------------------------------------
const balanceSheetMetrics = [
  { label: 'Total Assets', value: 'total_assets' },
  { label: 'Total Current Assets', value: 'total_current_assets' },
  { label: 'Cash and Cash Equivalents at Carrying Value', value: 'cash_and_cash_equivalents_at_carrying_value' },
  { label: 'Cash and Short Term Investments', value: 'cash_and_short_term_investments' },
  { label: 'Inventory', value: 'inventory' },
  { label: 'Current Net Receivables', value: 'current_net_receivables' },
  { label: 'Total Non-Current Assets', value: 'total_non_current_assets' },
  { label: 'Property, Plant, and Equipment', value: 'property_plant_equipment' },
  { label: 'Accumulated Depreciation, Amortization PPE', value: 'accumulated_depreciation_amortization_ppe' },
  { label: 'Intangible Assets', value: 'intangible_assets' },
  { label: 'Intangible Assets Excluding Goodwill', value: 'intangible_assets_excluding_goodwill' },
  { label: 'Goodwill', value: 'goodwill' },
  { label: 'Investments', value: 'investments' },
  { label: 'Long Term Investments', value: 'long_term_investments' },
  { label: 'Short Term Investments', value: 'short_term_investments' },
  { label: 'Other Current Assets', value: 'other_current_assets' },
  { label: 'Other Non-Current Assets', value: 'other_non_current_assets' },
  { label: 'Total Liabilities', value: 'total_liabilities' },
  { label: 'Total Current Liabilities', value: 'total_current_liabilities' },
  { label: 'Current Accounts Payable', value: 'current_accounts_payable' },
  { label: 'Deferred Revenue', value: 'deferred_revenue' },
  { label: 'Current Debt', value: 'current_debt' },
  { label: 'Short Term Debt', value: 'short_term_debt' },
  { label: 'Total Non-Current Liabilities', value: 'total_non_current_liabilities' },
  { label: 'Capital Lease Obligations', value: 'capital_lease_obligations' },
  { label: 'Long Term Debt', value: 'long_term_debt' },
  { label: 'Current Long Term Debt', value: 'current_long_term_debt' },
  { label: 'Long Term Debt Noncurrent', value: 'long_term_debt_noncurrent' },
  { label: 'Short Long Term Debt Total', value: 'short_long_term_debt_total' },
  { label: 'Other Current Liabilities', value: 'other_current_liabilities' },
  { label: 'Other Non-Current Liabilities', value: 'other_non_current_liabilities' },
  { label: 'Total Shareholder Equity', value: 'total_shareholder_equity' },
  { label: 'Treasury Stock', value: 'treasury_stock' },
  { label: 'Retained Earnings', value: 'retained_earnings' },
  { label: 'Common Stock', value: 'common_stock' },
  { label: 'Common Stock Shares Outstanding', value: 'common_stock_shares_outstanding' },
];


function BalanceSheetMetricPlot({ data, selectedMetrics }) {
  // Ensure data and selectedMetrics are available before proceeding
  if (!data || data.length === 0 || !selectedMetrics || selectedMetrics.length === 0) {
    return <div>No data or metrics selected.</div>;
  }

  const layout = {
    autosize: true,
    title: `Plot of Various Balance Sheet Metrics for ${data[0].stock_id || ''}`,
  };
  // ${selectedMetrics.map(metric => balanceSheetMetrics.find(m => m.value === metric)?.label || '').join(", ")}

  const plotData = selectedMetrics.map(metric => ({
    x: data.map(entry => entry.date),
    y: data.map(entry => entry[metric]),
    type: 'scatter',
    mode: 'lines+markers',
    name: balanceSheetMetrics.find(m => m.value === metric)?.label || 'Unknown Metric',
  }));

  return (
    <Plot data={plotData} layout={layout} useResizeHandler={true} style={{ width: "100%", height: "100%" }} />
  );
}


// INCOME STATEMENT METRICS ----------------------------------------------------------------------------
const incomeStatementMetrics = [
  { label: 'Gross Profit', value: 'gross_profit' },
  { label: 'Total Revenue', value: 'total_revenue' },
  { label: 'Cost of Revenue', value: 'cost_of_revenue' },
  { label: 'COGS', value: 'cogs' },
  { label: 'Operating Income', value: 'operating_income' },
  { label: 'Net Investment Income', value: 'net_investment_income' },
  { label: 'Net Interest Income', value: 'net_interest_income' },
  { label: 'Interest Income', value: 'interest_income' },
  { label: 'Interest Expense', value: 'interest_expense' },
  { label: 'Non-Interest Income', value: 'non_interest_income' },
  { label: 'Other Non-Operating Income', value: 'other_non_operating_income' },
  { label: 'Depreciation', value: 'depreciation' },
  { label: 'Depreciation & Amortization', value: 'depreciation_amortization' },
  { label: 'Income Before Tax', value: 'income_before_tax' },
  { label: 'Income Tax Expense', value: 'income_tax_expense' },
  { label: 'Interest & Debt Expense', value: 'interest_and_debt_expense' },
  { label: 'Net Income from Continuing Operations', value: 'net_income_from_continuing_operations' },
  { label: 'Comprehensive Income', value: 'comprehensive_income' },
  { label: 'EBIT', value: 'ebit' },
  { label: 'EBITDA', value: 'ebitda' },
  { label: 'Net Income', value: 'net_income' },
];


function IncomeStatementMetricPlot({ data, selectedMetrics }) {
  if (!data || data.length === 0 || !selectedMetrics || selectedMetrics.length === 0) {
    return <div>No data or metrics selected.</div>;
  }

  const layout = {
    autosize: true,
    title: `Plot of Various Income Statement Metrics for ${data[0].stock_id || ''}`,
  };

  const plotData = selectedMetrics.map(metric => ({
    x: data.map(entry => entry.date),
    y: data.map(entry => entry[metric]),
    type: 'scatter',
    mode: 'lines+markers',
    name: incomeStatementMetrics.find(m => m.value === metric)?.label || 'Unknown Metric',
  }));

  return (
    <Plot data={plotData} layout={layout} useResizeHandler={true} style={{ width: "100%", height: "100%" }} />
  );
}


// CASH FLOW STATEMENT METRICS ----------------------------------------------------------------------------
const cashFlowMetrics = [
  { label: 'Operating Cash Flow', value: 'operating_cashflow' },
  { label: 'Payments for Operating Activities', value: 'payments_for_operating_activities' },
  { label: 'Proceeds from Operating Activities', value: 'proceeds_from_operating_activities' },
  { label: 'Change in Operating Liabilities', value: 'change_in_operating_liabilities' },
  { label: 'Change in Operating Assets', value: 'change_in_operating_assets' },
  { label: 'Depreciation, Depletion and Amortization', value: 'depreciation_depletion_and_amortization' },
  { label: 'Capital Expenditures', value: 'capital_expenditures' },
  { label: 'Change in Receivables', value: 'change_in_receivables' },
  { label: 'Change in Inventory', value: 'change_in_inventory' },
  { label: 'Profit/Loss', value: 'profit_loss' },
  { label: 'Cash Flow from Investment', value: 'cashflow_from_investment' },
  { label: 'Cash Flow from Financing', value: 'cashflow_from_financing' },
  { label: 'Proceeds from Repayments of Short Term Debt', value: 'proceeds_from_repayments_of_short_term_debt' },
  { label: 'Payments for Repurchase of Common Stock', value: 'payments_for_repurchase_of_common_stock' },
  { label: 'Payments for Repurchase of Equity', value: 'payments_for_repurchase_of_equity' },
  { label: 'Payments for Repurchase of Preferred Stock', value: 'payments_for_repurchase_of_preferred_stock' },
  { label: 'Dividend Payout', value: 'dividend_payout' },
  { label: 'Dividend Payout Common Stock', value: 'dividend_payout_common_stock' },
  { label: 'Dividend Payout Preferred Stock', value: 'dividend_payout_preferred_stock' },
  { label: 'Proceeds from Issuance of Common Stock', value: 'proceeds_from_issuance_of_common_stock' },
  { label: 'Proceeds from Issuance of Long-term Debt and Capital Securities Net', value: 'proceeds_issuance_long_term_debt_capital_sec_net' },
  { label: 'Proceeds from Issuance of Preferred Stock', value: 'proceeds_from_issuance_of_preferred_stock' },
  { label: 'Proceeds from Repurchase of Equity', value: 'proceeds_from_repurchase_of_equity' },
  { label: 'Proceeds from Sale of Treasury Stock', value: 'proceeds_from_sale_of_treasury_stock' },
  { label: 'Change in Cash and Cash Equivalents', value: 'change_in_cash_and_cash_equivalents' },
  { label: 'Change in Exchange Rate', value: 'change_in_exchange_rate' },
  { label: 'Net Income', value: 'net_income' },
];


function CashFlowMetricPlot({ data, selectedMetrics }) {
  if (!data || data.length === 0 || !selectedMetrics || selectedMetrics.length === 0) {
    return <div>No data or metrics selected.</div>;
  }

  const layout = {
    autosize: true,
    title: `Plot of Various Cash Flow Metrics for ${data[0].stock_id || 'Unknown Stock'}`,
  };

  const plotData = selectedMetrics.map(metric => ({
    x: data.map(entry => entry.date),
    y: data.map(entry => entry[metric]),
    type: 'scatter',
    mode: 'lines+markers',
    name: cashFlowMetrics.find(m => m.value === metric)?.label || 'Unknown Metric',
  }));

  return (
    <Plot data={plotData} layout={layout} useResizeHandler={true} style={{ width: "100%", height: "100%" }} />
  );
}






