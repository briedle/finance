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
    },
    {
      x: epsData.map(entry => entry.fiscal_date_ending),
      y: epsData.map(entry => entry.reported_eps + (entry.reported_eps - entry.estimated_eps)),
      type: 'bar',
      name: 'Surprise Amount',
      base: epsData.map(entry => entry.reported_eps),
    },
    {
      x: epsData.map(entry => entry.fiscal_date_ending),
      y: epsData.map(entry => (entry.reported_eps - entry.estimated_eps) / entry.estimated_eps * 100),
      type: 'bar',
      name: 'Surprise Percentage',
    },
  ];

  return (
    <Card>
      <Card.Body>
        <Plot
          data={epsPlotData}
          layout={{ width: 720, height: 440, title: 'EPS Metrics' }}
        />
      </Card.Body>
    </Card>
  );
};
