import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldAlert, Key, ServerCrash } from 'lucide-react';

function Activation() {
  const navigate = useNavigate();
  const [secretKey, setSecretKey] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleActivate = (e) => {
    e.preventDefault();
    setError('');

    // Strict 64-character validation
    if (secretKey.length !== 64) {
      setError(`INVALID KEY FORMAT: Expected 64 characters, got ${secretKey.length}.`);
      return;
    }

    setLoading(true);

    // Dummy API delay to simulate backend verification
    setTimeout(() => {
      // 1. System ko locally "Activated" mark kar do
      localStorage.setItem('netcraft_activated', 'true');
      
      // 2. Ab user ko properly Setup page par bhej do
      navigate('/setup');
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-slate-900 flex flex-col items-center justify-center p-6 font-sans text-slate-200">
      
      <div className="w-full max-w-2xl bg-slate-800 border border-slate-700 p-10 rounded-2xl shadow-2xl relative">
        
        {/* Premium Enterprise Header */}
        <div className="flex justify-center mb-6 text-blue-500">
          <ShieldAlert size={56} strokeWidth={1.5} />
        </div>
        <div className="text-center mb-10">
          <h1 className="text-3xl font-extrabold text-white tracking-tight mb-2">System Locked</h1>
          <p className="text-blue-400 text-sm font-semibold uppercase tracking-wider">
            NetCraft Middleware Engine Requires Initialization
          </p>
        </div>

        {error && (
          <div className="bg-red-500/10 border border-red-500 text-red-500 p-4 mb-6 rounded-lg flex items-center gap-3 text-sm font-semibold">
            <ServerCrash size={20} />
            {error}
          </div>
        )}

        <form onSubmit={handleActivate} className="space-y-6">
          <div>
            <label className="block text-slate-400 text-xs font-bold mb-3 uppercase tracking-wider text-center">
              Enter 64-Bit Enterprise Secret Code
            </label>
            <div className="relative">
              <Key className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-500" size={20} />
              <input 
                type="text" 
                required
                value={secretKey}
                onChange={(e) => setSecretKey(e.target.value)}
                maxLength={64}
                className="w-full bg-slate-900 border border-slate-600 text-blue-400 text-center rounded-xl py-4 pl-12 pr-4 focus:outline-none focus:border-blue-500 transition-colors font-mono tracking-widest text-sm shadow-inner"
                placeholder="0000000000000000000000000000000000000000000000000000000000000000"
              />
            </div>
            <div className="text-right mt-2 text-xs text-slate-500 font-mono">
              Length: {secretKey.length} / 64
            </div>
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-4 rounded-xl uppercase tracking-wider transition-all shadow-lg shadow-blue-500/30 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Verifying Integrity...' : 'Initialize System'}
          </button>
        </form>

      </div>
      
      <p className="text-slate-600 text-xs mt-8 font-semibold tracking-wider uppercase">
        Unauthorized access is strictly prohibited.
      </p>
    </div>
  );
}

export default Activation;