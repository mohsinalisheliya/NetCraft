import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  ShieldCheck, Cpu, UploadCloud, Clock, CheckCircle, 
  Moon, Sun, Monitor, Briefcase, Database,
  Eye, EyeOff, Copy, Check, RefreshCw
} from 'lucide-react';

function Dashboard() {
  // --- STATES ---
  const [isDark, setIsDark] = useState(true);
  const [themeName, setThemeName] = useState(localStorage.getItem('netcraft_ui_style') || 'enterprise');
  
  const [sysInfo, setSysInfo] = useState({ name: 'System Loading...', version: '...' });
  const [licenseData, setLicenseData] = useState({
    status: 'LOADING...', remainingDays: '...', modules: '...', key: '...', mac: '...', exactExpiry: '...'
  });

  // 🚀 NAYE STATES (Hide/Unhide, Copy, aur Update Checking ke liye)
  const [showKey, setShowKey] = useState(false);
  const [copied, setCopied] = useState(false);
  const [isChecking, setIsChecking] = useState(false);
  const [updateMsg, setUpdateMsg] = useState('Click the button below to check servers.');

  // --- EFFECTS ---
  useEffect(() => { localStorage.setItem('netcraft_ui_style', themeName); }, [themeName]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/core/system-info/')
      .then(res => setSysInfo({ name: res.data.app_name, version: res.data.version }))
      .catch(() => setSysInfo({ name: 'NetCraft (Offline)', version: '1.0.0' }));
  }, []);

  useEffect(() => {
    axios.get('http://localhost:8000/api/core/license-status/')
      .then(res => {
        const info = res.data.license_info || {};
        setLicenseData({
          status: info.status ? info.status.toUpperCase() : 'UNKNOWN', 
          remainingDays: info.remaining_days !== undefined ? info.remaining_days : '0',
          modules: info.allowed_modules && info.allowed_modules.length > 0 ? info.allowed_modules.join(', ') : 'NONE',
          key: info.secret_key || 'NO-KEY-FOUND',
          mac: info.hardware_mac || 'UNKNOWN MAC',
          exactExpiry: info.expiry_exact_date || 'Lifetime'
        });
      })
      .catch(() => {
        setLicenseData({ status: 'ERROR', remainingDays: '0', modules: 'ERROR', key: 'NO-KEY', mac: 'UNKNOWN', exactExpiry: 'Error' });
      });
  }, []);

  // --- FUNCTIONS ---
  // Hardware MAC Copy karne ka function
  const handleCopyMac = () => {
    navigator.clipboard.writeText(licenseData.mac);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // OTA Update Check karne ka function
  const handleCheckUpdate = () => {
    setIsChecking(true);
    setUpdateMsg("Checking secure servers...");
    
    axios.get('http://localhost:8000/api/core/check-update/')
      .then(res => {
        setUpdateMsg(res.data.message);
        setIsChecking(false);
      })
      .catch(err => {
        setUpdateMsg("Failed to connect to update server.");
        setIsChecking(false);
      });
  };

  // --- THEMES CONFIG (Shortened for space, keeping your logic) ---
  const themes = {
    retro: { 
      bg: isDark ? 'bg-[#000080]' : 'bg-[#c0c0c0]', text: isDark ? 'text-white' : 'text-black',
      card: isDark ? 'bg-[#0000aa] border-[3px] border-white' : 'bg-[#c0c0c0] border-4 border-gray-600',
      accent: isDark ? 'text-yellow-400' : 'text-blue-900', iconBg: 'bg-transparent',
      btn: 'bg-yellow-400 text-black font-bold uppercase', radius: 'rounded-none', border: 'border-white',
      fontFamily: 'font-mono tracking-widest', fontSize: 'text-sm font-bold',
      inputBg: isDark ? 'bg-black/50' : 'bg-white/50'
    },
    enterprise: { 
      bg: isDark ? 'bg-slate-900' : 'bg-slate-50', text: isDark ? 'text-slate-200' : 'text-slate-800',
      card: isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-300',
      accent: isDark ? 'text-blue-400' : 'text-blue-600', iconBg: isDark ? 'bg-blue-500/10' : 'bg-blue-100',
      btn: 'bg-blue-600 text-white font-semibold', radius: 'rounded-lg', border: isDark ? 'border-slate-700' : 'border-slate-300',
      fontFamily: 'font-sans', fontSize: 'text-base', inputBg: isDark ? 'bg-slate-900' : 'bg-slate-100'
    },
    modern: { 
      bg: isDark ? 'bg-zinc-950' : 'bg-zinc-100', text: isDark ? 'text-zinc-100' : 'text-zinc-900',
      card: isDark ? 'bg-white/5 border-white/10 backdrop-blur-2xl' : 'bg-white/60 border-white backdrop-blur-xl',
      accent: isDark ? 'text-cyan-400' : 'text-blue-600', iconBg: isDark ? 'bg-cyan-500/10' : 'bg-blue-100',
      btn: 'bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow-lg', radius: 'rounded-3xl', border: isDark ? 'border-white/10' : 'border-black/5',
      fontFamily: 'font-sans font-light tracking-wide', fontSize: 'text-sm', inputBg: isDark ? 'bg-black/20' : 'bg-white/40'
    }
  };
  const t = themes[themeName] || themes['enterprise'];

  // Key Masking Logic
  const displayKey = showKey 
    ? licenseData.key 
    : `****************************************`;

  // --- RENDER ---
  return (
    <div className={`min-h-screen p-6 md:p-10 transition-colors duration-500 ${t.bg} ${t.text} ${t.fontFamily} ${t.fontSize}`}>
      
      {/* HEADER SECTION (Same as before) */}
      <header className={`flex justify-between items-center mb-8 pb-6 border-b ${t.border}`}>
        <div>
          <h1 className={`text-3xl font-extrabold tracking-tight ${t.accent}`}>{sysInfo.name}</h1>
          <p className="opacity-70 mt-1 uppercase text-xs font-semibold">Engine v{sysInfo.version}</p>
        </div>
        <div className="flex gap-4">
          <button onClick={() => setIsDark(!isDark)} className={`p-2 border ${t.border} ${t.radius}`}>
            {isDark ? <Sun size={18} /> : <Moon size={18} />}
          </button>
          <div className="flex gap-2">
            <button onClick={() => setThemeName('retro')} className={`p-2 border ${t.border} ${t.radius}`}><Database size={18}/></button>
            <button onClick={() => setThemeName('enterprise')} className={`p-2 border ${t.border} ${t.radius}`}><Briefcase size={18}/></button>
            <button onClick={() => setThemeName('modern')} className={`p-2 border ${t.border} ${t.radius}`}><Monitor size={18}/></button>
          </div>
        </div>
      </header>

      {/* 🚀 TOP ROW: 3 MAIN CARDS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        
        {/* CARD 1: License Status & Hide/Unhide Key */}
        <div className={`border p-6 ${t.card} ${t.radius} flex flex-col justify-between`}>
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="opacity-70 text-xs uppercase font-bold mb-1">License Status</p>
              <h3 className="text-2xl font-bold flex items-center gap-2">
                {licenseData.status} 
                <span className={`w-3 h-3 rounded-full ${licenseData.status === 'ACTIVE' ? 'bg-green-500' : 'bg-red-500'} animate-pulse`}></span>
              </h3>
            </div>
            <div className={`p-3 ${t.iconBg} ${t.radius} ${t.accent}`}><ShieldCheck size={28} /></div>
          </div>
          
          <div className="mt-2">
            <p className="text-[10px] uppercase opacity-70 mb-1">Current License Key</p>
            <div className={`flex items-center justify-between p-2 border ${t.border} ${t.radius} ${t.inputBg}`}>
              <span className="font-mono text-xs tracking-wider truncate mr-2">{displayKey}</span>
              <button onClick={() => setShowKey(!showKey)} className="opacity-60 hover:opacity-100 cursor-pointer transition-opacity">
                {showKey ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </div>
        </div>

        {/* CARD 2: Expiry Days & Exact Time */}
        <div className={`border p-6 ${t.card} ${t.radius}`}>
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="opacity-70 text-xs uppercase font-bold mb-1">Time Remaining</p>
              <h3 className="text-2xl font-bold">{licenseData.remainingDays} DAYS</h3>
            </div>
            <div className={`p-3 ${t.iconBg} ${t.radius} ${t.accent}`}><Clock size={28} /></div>
          </div>
          <div className={`mt-4 p-2 border ${t.border} ${t.radius} ${t.inputBg} text-center`}>
            <p className="text-xs opacity-80">Expires: <span className="font-bold">{licenseData.exactExpiry}</span></p>
          </div>
        </div>

        {/* CARD 3: Active Modules */}
        <div className={`border p-6 ${t.card} ${t.radius}`}>
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="opacity-70 text-xs uppercase font-bold mb-1">Active Modules</p>
              <h3 className="text-2xl font-bold truncate max-w-[150px]">{licenseData.modules}</h3>
            </div>
            <div className={`p-3 ${t.iconBg} ${t.radius} ${t.accent}`}><Cpu size={28} /></div>
          </div>
          <p className="text-xs opacity-60 mt-4">RESTRICTED ACCESS: FALSE</p>
        </div>
      </div>

      {/* 🚀 MIDDLE ROW: Hardware ID & OTA Update */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        
        {/* Hardware ID Copy Card */}
        <div className={`border p-6 ${t.card} ${t.radius}`}>
          <h3 className="text-lg font-bold mb-2 uppercase">Hardware Identification</h3>
          <p className="text-xs opacity-70 mb-4">Provide this MAC ID to support for manual key generation or renewal.</p>
          
          <div className={`flex items-center justify-between p-4 border ${t.border} ${t.radius} ${t.inputBg}`}>
            <span className="font-mono text-lg tracking-widest">{licenseData.mac}</span>
            <button onClick={handleCopyMac} className={`p-2 cursor-pointer rounded hover:bg-black/10 transition-colors ${copied ? 'text-green-500' : t.accent}`}>
              {copied ? <Check size={20} /> : <Copy size={20} />}
            </button>
          </div>
        </div>

        {/* OTA Update Checker Card */}
        <div className={`border p-6 ${t.card} ${t.radius} flex flex-col justify-between`}>
          <div className="flex justify-between items-center mb-2">
            <h3 className="text-lg font-bold uppercase">Software Update</h3>
            <span className={`px-2 py-1 text-[10px] uppercase font-bold border ${t.border} rounded-full`}>Current: v{sysInfo.version}</span>
          </div>
          <p className="text-xs opacity-70 mb-4 text-center">{updateMsg}</p>
          
          <button 
            onClick={handleCheckUpdate} 
            disabled={isChecking}
            className={`w-full py-3 flex items-center justify-center gap-2 uppercase tracking-wider cursor-pointer ${t.btn} ${t.radius} ${isChecking ? 'opacity-50' : ''}`}
          >
            <RefreshCw size={18} className={isChecking ? 'animate-spin' : ''} />
            {isChecking ? 'Checking Servers...' : 'Check For Updates'}
          </button>
        </div>

      </div>

      {/* 🚀 BOTTOM ROW: Offline Patch Drag & Drop */}
      <div className={`border-2 border-dashed p-10 text-center transition-all ${t.card} ${t.border} ${t.radius} hover:opacity-90`}>
        <div className="flex justify-center mb-4">
          <div className={`p-4 ${t.iconBg} rounded-full ${t.accent}`}>
            <UploadCloud size={40} strokeWidth={1.5} />
          </div>
        </div>
        <h2 className="text-xl font-bold mb-2 uppercase">Offline System Patch</h2>
        <p className="opacity-80 text-xs mb-6 max-w-md mx-auto leading-relaxed">
          DRAG AND DROP THE VERIFIED {sysInfo.name.toUpperCase()} [.ZIP] PATCH FILE HERE TO SECURELY UPGRADE SYSTEM OFFLINE.
        </p>
        <button className={`py-2 px-6 text-sm uppercase tracking-wider cursor-pointer border ${t.border} ${t.radius} hover:bg-white/10`}>
          Browse Patch File
        </button>
      </div>

    </div>
  );
}

export default Dashboard;