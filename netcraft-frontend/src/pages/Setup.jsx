import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Building2, ServerCrash, ArrowRight, Moon, Sun, Monitor } from 'lucide-react';
import axios from 'axios';

function Setup() {
  const navigate = useNavigate();
  const [orgName, setOrgName] = useState('');
  
  // Pehle se save ki hui theme check karo, warna 'dark' default rakho
  const [theme, setTheme] = useState(localStorage.getItem('netcraft_theme') || 'dark'); 
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // 🎨 INSTANT THEME CHANGER FUNCTION
  const changeTheme = (newTheme) => {
    setTheme(newTheme);
    localStorage.setItem('netcraft_theme', newTheme);
    
    const root = document.documentElement;
    if (newTheme === 'dark') {
      root.classList.add('dark');
    } else if (newTheme === 'light') {
      root.classList.remove('dark');
    } else {
      // System (Auto) Mode check
      if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        root.classList.add('dark');
      } else {
        root.classList.remove('dark');
      }
    }
  };

  // Jab page pehli baar load ho, toh purani theme apply kar do
  useEffect(() => {
    changeTheme(theme);
  }, []);

  const handleSetup = async (e) => {
    e.preventDefault();
    setError('');

    if (orgName.trim().length < 3) {
      setError('Organization name must be at least 3 characters long.');
      return;
    }

    setLoading(true);

    try {
      await axios.post('http://localhost:8000/api/core/company-profile/', {
        company_name: orgName
      });

      localStorage.setItem('netcraft_setup_complete', 'true');
      localStorage.setItem('netcraft_org_name', orgName);
      
      // Theme pehle hi save ho chuki hai instant click par
      navigate('/login');

    } catch (err) {
      if (err.response && err.response.data) {
        const errorMsg = err.response.data.detail || JSON.stringify(err.response.data);
        setError(`API Error: ${errorMsg}`);
      } else {
        setError('SERVER OFFLINE: Unable to connect to the Engine.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    // 🌗 Yahan 'dark:' classes ka jaadu dekho
    <div className="min-h-screen bg-gray-50 dark:bg-slate-900 flex flex-col items-center justify-center p-6 font-sans text-gray-900 dark:text-slate-200 transition-colors duration-300">
      
      <div className="w-full max-w-lg bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 p-10 rounded-2xl shadow-2xl relative transition-colors duration-300">
        
        {/* Header */}
        <div className="flex justify-center mb-6 text-blue-600 dark:text-blue-500">
          <Building2 size={56} strokeWidth={1.5} />
        </div>
        <div className="text-center mb-10">
          <h1 className="text-3xl font-extrabold text-gray-900 dark:text-white tracking-tight mb-2 transition-colors">Workspace Setup</h1>
          <p className="text-blue-600 dark:text-blue-400 text-sm font-semibold uppercase tracking-wider transition-colors">
            Configure Your {import.meta.env.VITE_APP_NAME} Environment
          </p>
        </div>

        {error && (
          <div className="bg-red-100 dark:bg-red-500/10 border border-red-400 dark:border-red-500 text-red-600 dark:text-red-500 p-4 mb-6 rounded-lg flex items-start gap-3 text-sm font-semibold overflow-hidden">
            <ServerCrash size={20} className="flex-shrink-0 mt-0.5" />
            <span className="break-all">{error}</span>
          </div>
        )}

        <form onSubmit={handleSetup} className="space-y-8">
          
          {/* Organization Name Input */}
          <div>
            <label className="block text-gray-600 dark:text-slate-400 text-xs font-bold mb-3 uppercase tracking-wider text-center transition-colors">
              Organization / Company Name
            </label>
            <input 
              type="text" 
              required
              value={orgName}
              onChange={(e) => setOrgName(e.target.value)}
              className="w-full bg-gray-100 dark:bg-slate-900 border border-gray-300 dark:border-slate-600 text-blue-700 dark:text-blue-400 text-center rounded-xl py-4 px-4 focus:outline-none focus:border-blue-500 transition-colors font-bold text-lg shadow-inner"
              placeholder="e.g. Stark Industries"
            />
          </div>

          {/* 🎨 Theme Selector Area */}
          <div>
            <label className="block text-gray-600 dark:text-slate-400 text-xs font-bold mb-3 uppercase tracking-wider text-center transition-colors">
              System Interface Theme
            </label>
            <div className="grid grid-cols-3 gap-3">
              <button
                type="button"
                onClick={() => changeTheme('light')}
                className={`flex flex-col items-center justify-center p-4 rounded-xl border-2 transition-all cursor-pointer ${
                  theme === 'light' 
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400' 
                    : 'border-gray-200 dark:border-slate-700 bg-gray-50 dark:bg-slate-900 text-gray-500 dark:text-slate-500 hover:border-gray-300 dark:hover:border-slate-500'
                }`}
              >
                <Sun size={24} className="mb-2" />
                <span className="text-xs font-bold uppercase">Light</span>
              </button>

              <button
                type="button"
                onClick={() => changeTheme('dark')}
                className={`flex flex-col items-center justify-center p-4 rounded-xl border-2 transition-all cursor-pointer ${
                  theme === 'dark' 
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400' 
                    : 'border-gray-200 dark:border-slate-700 bg-gray-50 dark:bg-slate-900 text-gray-500 dark:text-slate-500 hover:border-gray-300 dark:hover:border-slate-500'
                }`}
              >
                <Moon size={24} className="mb-2" />
                <span className="text-xs font-bold uppercase">Dark</span>
              </button>

              <button
                type="button"
                onClick={() => changeTheme('system')}
                className={`flex flex-col items-center justify-center p-4 rounded-xl border-2 transition-all cursor-pointer ${
                  theme === 'system' 
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400' 
                    : 'border-gray-200 dark:border-slate-700 bg-gray-50 dark:bg-slate-900 text-gray-500 dark:text-slate-500 hover:border-gray-300 dark:hover:border-slate-500'
                }`}
              >
                <Monitor size={24} className="mb-2" />
                <span className="text-xs font-bold uppercase">Auto</span>
              </button>
            </div>
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-4 rounded-xl uppercase tracking-wider transition-all shadow-lg shadow-blue-500/30 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            {loading ? 'Configuring Workspace...' : 'Continue to Login'}
            {!loading && <ArrowRight size={18} />}
          </button>
        </form>

      </div>
    </div>
  );
}

export default Setup;