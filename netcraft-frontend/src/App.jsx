import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Register from './pages/Register';
import Activation from './pages/Activation';
import Setup from './pages/Setup'; // Naya Setup page import kiya

// SMART SECURITY GUARD
const RouteGuard = ({ children, requireSetup = true }) => {
  const isActivated = localStorage.getItem('netcraft_activated') === 'true';
  const isSetupComplete = localStorage.getItem('netcraft_setup_complete') === 'true';
  
  if (!isActivated) {
    return <Navigate to="/activate" replace />;
  }
  
  if (requireSetup && !isSetupComplete) {
    return <Navigate to="/setup" replace />;
  }
  
  return children;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Step 1: Activation (No Guard needed) */}
        <Route path="/activate" element={<Activation />} />
        
        {/* Step 2: Setup (Needs Activation, but NOT setup) */}
        <Route path="/setup" element={
          <RouteGuard requireSetup={false}>
            <Setup />
          </RouteGuard>
        } />
        
        {/* Step 3: All other pages (Need BOTH Activation & Setup) */}
        <Route path="/" element={<RouteGuard><Dashboard /></RouteGuard>} />
        <Route path="/login" element={<RouteGuard><Login /></RouteGuard>} />
        <Route path="/register" element={<RouteGuard><Register /></RouteGuard>} />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;