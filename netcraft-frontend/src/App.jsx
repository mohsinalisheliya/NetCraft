import React, { useEffect } from 'react'; // 🔧 Naya: useEffect import kiya
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Register from './pages/Register';
import Activation from './pages/Activation';
import Setup from './pages/Setup';

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
  
  // 🎨 GLOBAL THEME APPLIER (App load hote hi theme lagayega)
  useEffect(() => {
    const theme = localStorage.getItem('netcraft_theme') || 'dark';
    const root = document.documentElement;
    
    if (theme === 'dark') {
      root.classList.add('dark');
    } else if (theme === 'light') {
      root.classList.remove('dark');
    } else {
      // Auto (System) mode ke liye
      if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        root.classList.add('dark');
      } else {
        root.classList.remove('dark');
      }
    }
  }, []); // [] ka matlab hai yeh app khulte hi sirf ek baar chalega

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