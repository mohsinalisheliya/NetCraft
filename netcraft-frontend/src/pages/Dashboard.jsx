import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, Cpu, UploadCloud, Clock, CheckCircle, 
  Moon, Sun, Monitor, Briefcase, Database 
} from 'lucide-react';

function Dashboard() {
  const [isDark, setIsDark] = useState(true);
  
  // 🔧 FIX 1: Iska naam 'netcraft_ui_style' kar diya taaki Setup wale Light/Dark mode ('netcraft_theme') se na takraye
  const [themeName, setThemeName] = useState(localStorage.getItem('netcraft_ui_style') || 'enterprise');

  // Change hone par naya UI style save karne ke liye
  useEffect(() => {
    localStorage.setItem('netcraft_ui_style', themeName);
  }, [themeName]);

  const themes = {
    retro: { 
      bg: isDark ? 'bg-[#000080]' : 'bg-[#c0c0c0]', 
      text: isDark ? 'text-white' : 'text-black',
      card: isDark 
        ? 'bg-[#0000aa] border-[3px] border-white shadow-[6px_6px_0px_#c0c0c0]' 
        : 'bg-[#c0c0c0] border-t-[3px] border-l-[3px] border-white border-b-[3px] border-r-[3px] border-gray-600',
      accent: isDark ? 'text-yellow-400' : 'text-blue-900', 
      iconBg: 'bg-transparent',
      btn: isDark 
        ? 'bg-yellow-400 text-[#000080] border-2 border-white hover:bg-white uppercase font-extrabold transition-none' 
        : 'bg-[#c0c0c0] border-t-2 border-l-2 border-white border-b-2 border-r-2 border-gray-800 text-black uppercase font-bold transition-none hover:bg-[#d0d0d0]',
      radius: 'rounded-none',
      border: isDark ? 'border-white' : 'border-gray-500',
      fontFamily: 'font-mono tracking-widest', 
      fontSize: 'text-base uppercase font-bold' 
    },
    enterprise: { 
      bg: isDark ? 'bg-slate-900' : 'bg-slate-50',
      text: isDark ? 'text-slate-200' : 'text-slate-800',
      card: isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-300',
      accent: isDark ? 'text-blue-400' : 'text-blue-600',
      iconBg: isDark ? 'bg-blue-500/10' : 'bg-blue-100',
      btn: 'bg-blue-600 hover:bg-blue-700 text-white font-semibold',
      radius: 'rounded-lg',
      border: isDark ? 'border-slate-700' : 'border-slate-300',
      fontFamily: 'font-sans', 
      fontSize: 'text-base'
    },
    modern: { 
      bg: isDark ? 'bg-zinc-950' : 'bg-zinc-100',
      text: isDark ? 'text-zinc-100' : 'text-zinc-900',
      card: isDark ? 'bg-white/5 border-white/10 backdrop-blur-2xl shadow-2xl' : 'bg-white/60 border-white backdrop-blur-xl shadow-xl',
      accent: isDark ? 'text-cyan-400' : 'text-blue-600',
      iconBg: isDark ? 'bg-cyan-500/10' : 'bg-blue-100',
      btn: 'bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-90 text-white shadow-lg shadow-blue-500/30',
      radius: 'rounded-3xl',
      border: isDark ? 'border-white/10' : 'border-black/5',
      fontFamily: 'font-sans font-light tracking-wide', 
      fontSize: 'text-sm'
    }
  };

  // 🔧 FIX 2: Safety Net (Fallback). Agar galti se koi galat theme name aa bhi jaye, toh app crash na ho aur 'enterprise' load kar le.
  const t = themes[themeName] || themes['enterprise'];

  return (
    <div className={`min-h-screen p-6 md:p-10 transition-colors duration-500 ${t.bg} ${t.text} ${t.fontFamily} ${t.fontSize}`}>
      
      <header className={`flex flex-col md:flex-row justify-between items-start md:items-center mb-10 pb-6 border-b ${t.border}`}>
        <div className="mb-4 md:mb-0">
          <h1 className={`text-4xl font-extrabold tracking-tight ${t.accent}`}>
            NetCraft_OS
          </h1>
          <p className="opacity-70 mt-1 uppercase text-xs font-semibold">License Middleware Engine v1.0.0</p>
        </div>

        <div className="flex flex-col gap-3">
          <div className="flex items-center justify-end gap-2">
            <button 
              onClick={() => setIsDark(!isDark)}
              className={`flex items-center gap-2 px-4 py-2 border ${t.border} ${t.radius} hover:opacity-70 transition-all cursor-pointer`}
            >
              {isDark ? <Sun size={16} /> : <Moon size={16} />}
              <span className="text-xs uppercase font-bold">{isDark ? 'Light Mode' : 'Dark Mode'}</span>
            </button>
          </div>

          <div className="flex gap-2 justify-end">
            <button onClick={() => setThemeName('retro')} className={`p-2 border cursor-pointer ${themeName === 'retro' ? t.accent + ' ' + t.border : 'border-transparent opacity-50'} ${t.radius}`} title="1990s Database (Old Uncle)">
              <Database size={20} />
            </button>
            <button onClick={() => setThemeName('enterprise')} className={`p-2 border cursor-pointer ${themeName === 'enterprise' ? t.accent + ' ' + t.border : 'border-transparent opacity-50'} ${t.radius}`} title="Enterprise (Professional)">
              <Briefcase size={20} />
            </button>
            <button onClick={() => setThemeName('modern')} className={`p-2 border cursor-pointer ${themeName === 'modern' ? t.accent + ' ' + t.border : 'border-transparent opacity-50'} ${t.radius}`} title="Modern (Sleek)">
              <Monitor size={20} />
            </button>
          </div>
        </div>
      </header>

      <div className={`mb-8 p-4 border ${t.border} ${t.radius} ${t.card} flex items-center justify-between`}>
        <div className="flex items-center gap-3">
          <CheckCircle size={24} className={t.accent} />
          <span className="font-bold">System Timed Plan Active & MAC Verified</span>
        </div>
        <span className={`px-3 py-1 text-xs uppercase border ${t.border} ${t.radius} ${t.accent}`}>Online</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        <div className={`border p-6 ${t.card} ${t.radius} transition-transform hover:scale-[1.02]`}>
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="opacity-70 text-xs uppercase font-bold mb-2">License Status</p>
              <h3 className="text-2xl font-bold">VALID</h3>
            </div>
            <div className={`p-3 ${t.iconBg} ${t.radius} ${t.accent}`}>
              <ShieldCheck size={28} />
            </div>
          </div>
          <p className="text-xs opacity-60">KEY: NC-****-****-9A2F</p>
        </div>

        <div className={`border p-6 ${t.card} ${t.radius} transition-transform hover:scale-[1.02]`}>
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="opacity-70 text-xs uppercase font-bold mb-2">Time to Expiry</p>
              <h3 className="text-2xl font-bold">365 DAYS</h3>
            </div>
            <div className={`p-3 ${t.iconBg} ${t.radius} ${t.accent}`}>
              <Clock size={28} />
            </div>
          </div>
          <p className="text-xs opacity-60">RENEWAL: JULY 2027</p>
        </div>

        <div className={`border p-6 ${t.card} ${t.radius} transition-transform hover:scale-[1.02]`}>
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="opacity-70 text-xs uppercase font-bold mb-2">Active Modules</p>
              <h3 className="text-2xl font-bold">CRM, DxR</h3>
            </div>
            <div className={`p-3 ${t.iconBg} ${t.radius} ${t.accent}`}>
              <Cpu size={28} />
            </div>
          </div>
          <p className="text-xs opacity-60">RESTRICTED ACCESS: FALSE</p>
        </div>
      </div>

      <div className={`border-2 border-dashed p-12 text-center transition-all ${t.card} ${t.border} ${t.radius} hover:opacity-90`}>
        <div className="flex justify-center mb-6">
          <div className={`p-5 ${t.iconBg} rounded-full ${t.accent}`}>
            <UploadCloud size={48} strokeWidth={1.5} />
          </div>
        </div>
        <h2 className="text-2xl font-bold mb-3 uppercase">Offline System Patch</h2>
        <p className="opacity-80 text-sm mb-8 max-w-md mx-auto leading-relaxed">
          DRAG AND DROP THE VERIFIED NETCRAFT [.ZIP] PATCH FILE HERE TO SECURELY UPGRADE SYSTEM OFFLINE.
        </p>
        <button className={`py-3 px-8 uppercase tracking-wider cursor-pointer ${t.btn} ${t.radius}`}>
          Browse Patch File
        </button>
      </div>

    </div>
  );
}

export default Dashboard;