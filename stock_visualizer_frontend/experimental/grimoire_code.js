export default function App() {
  // State and custom hook calls remain the same



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
                <BalanceSheetMetricsSelector onSelect={setSelectedBalanceSheetMetrics} />
                {balanceSheetComponent}
                <IncomeStatementMetricsSelector onSelect={setSelectedIncomeStatementMetrics} />
                {incomeStatementComponent}
                <CashFlowMetricsSelector onSelect={setSelectedCashFlowMetrics} />
                {cashFlowComponent}
              </Row>
            </>
          )}
        </Col>
      </Row>
    </Container>
  );
}
