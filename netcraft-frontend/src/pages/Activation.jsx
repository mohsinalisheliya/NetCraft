import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldAlert, Key, ServerCrash, Copy, Check } from 'lucide-react';
import axios from 'axios';

function Activation() {
  const navigate = useNavigate();
  const [secretKey, setSecretKey] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [hardwareKey, setHardwareKey] = useState('GENERATING...'); // Dynamic state

  // ⚙️ SYSTEM LOGIC: Generate or Fetch Original Machine ID
  useEffect(() => {
    let storedHWID = localStorage.getItem('netcraft_hwid');
    
    if (!storedHWID) {
      // Generate a completely original 16-character Hex ID for this machine
      const generateHex = (size) => [...Array(size)].map(() => Math.floor(Math.random() * 16).toString(16).toUpperCase()).join('');
      storedHWID = `NC-HWID-${generateHex(4)}-${generateHex(4)}-${generateHex(4)}-${generateHex(4)}`;
      
      // Lock it permanently in local storage
      localStorage.setItem('netcraft_hwid', storedHWID);
    }
    setHardwareKey(storedHWID);
  }, []);

  const handleCopy = () => {
    navigator.clipboard.writeText(hardwareKey);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleActivate = async (e) => {
    e.preventDefault();
    setError('');

    if (secretKey.length !== 64) {
      setError(`INVALID KEY FORMAT: Expected 64 characters, got ${secretKey.length}.`);
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/api/core/verify-key/', {
        secret_key: secretKey,
        hardware_id: hardwareKey // Ab backend ko bhi pata chalega kis machine se request aayi
      });

      console.log(`[ENGINE]: ${response.data.message}`);
      localStorage.setItem('netcraft_activated', 'true');
      navigate('/setup');

    } catch (err) {
      if (err.response && err.response.data && err.response.data.message) {
        setError(err.response.data.message);
      } else {
        setError('SERVER OFFLINE: Unable to connect to the Engine.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 flex flex-col items-center justify-center p-6 font-sans text-slate-200">
      
      <div className="w-full max-w-2xl bg-slate-800 border border-slate-700 p-10 rounded-2xl shadow-2xl relative">
        
        {/* Header */}
        <div className="flex justify-center mb-6 text-blue-500">
          <ShieldAlert size={56} strokeWidth={1.5} />
        </div>
        <div className="text-center mb-10">
          <h1 className="text-3xl font-extrabold text-white tracking-tight mb-2">System Locked</h1>
          <p className="text-blue-400 text-sm font-semibold uppercase tracking-wider">
            {import.meta.env.VITE_APP_NAME} Middleware Engine Requires Initialization
          </p>
        </div>

        {/* 📋 UPDATED FEATURE: Original HWID & BIG/BOLD Font */}
        <div className="bg-slate-900 border border-slate-700 p-5 rounded-xl mb-6 flex items-center justify-between gap-4 shadow-inner">
          <div className="flex-1 min-w-0">
            <span className="block text-slate-500 text-[10px] font-bold uppercase tracking-widest mb-2">
              Machine Hardware Fingerprint (HWID)
            </span>
            {/* Yahan Font Bada (text-lg) aur Bold (font-extrabold) kar diya hai */}
            <code className="block text-lg font-extrabold font-mono text-blue-400 break-all select-all tracking-wider">
              {hardwareKey}
            </code>
          </div>
          <button
            onClick={handleCopy}
            type="button"
            title="Copy HWID"
            className={`p-3 rounded-lg border transition-all duration-200 flex-shrink-0 cursor-pointer ${
              copied 
                ? 'border-green-500/50 text-green-400 bg-green-500/10 scale-95' 
                : 'border-slate-600 text-slate-400 hover:text-white hover:border-slate-500 bg-slate-800 active:scale-95'
            }`}
          >
            {copied ? <Check size={24} /> : <Copy size={24} />}
          </button>
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
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-4 rounded-xl uppercase tracking-wider transition-all shadow-lg shadow-blue-500/30 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
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