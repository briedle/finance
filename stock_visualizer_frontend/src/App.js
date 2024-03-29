import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import CompanyDetail from './components/CompanyDetail';
import CompanyComparison from './components/CompanyComparison';
import Home from './components/Home'; // Make sure this path is correct

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/detail/:symbol" element={<CompanyDetail />} />
        <Route path="/compare" element={<CompanyComparison />} />
        <Route path="/" element={<Home />} />
      </Routes>
    </Router>
  );
}

export default App;







// Notes from GPT Grimoire:
// For a redirection to, let's say, the CompanyDetail component (you can replace 'some-default-symbol' with a valid default symbol or implement logic to select one dynamically):
// import { Redirect } from 'react-router-dom';

// <Route path="/">
//   <Redirect to={`/detail/some-default-symbol`} />
// </Route>


// App.js

