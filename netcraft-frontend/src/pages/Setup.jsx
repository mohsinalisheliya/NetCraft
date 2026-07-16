import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Settings, Palette, Building, CheckCircle2 } from 'lucide-react';

function Setup() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    orgName: '',
    theme: 'enterprise'
  });
  const [loading, setLoading] = useState(false);

  const handleComplete = (e) => {
    e.preventDefault();
    setLoading(true);

    setTimeout(() => {
      // 1. Setup complete ka tag memory mein daal do
      localStorage.setItem('netcraft_setup_complete', 'true');
      
      // 2. User ki chuni hui theme aur naam save kar lo
      localStorage.setItem('netcraft_theme', formData.theme);
      localStorage.setItem('netcraft_org', formData.orgName);
      
      // 3. Setup hone ke baad Login page par bhej do
      navigate('/login');
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-slate-900 flex flex-col items-center justify-center p-6 font-sans text-slate-200">
      <div className="w-full max-w-2xl bg-slate-800 border border-slate-700 p-10 rounded-2xl shadow-2xl relative">
        
        <div className="flex justify-center mb-6 text-blue-500">
          <Settings size={56} strokeWidth={1.5} className="animate-[spin_4s_linear_infinite]" />
        </div>
        <div className="text-center mb-10">
          <h1 className="text-3xl font-extrabold text-white tracking-tight mb-2">System Initialization</h1>
          <p className="text-blue-400 text-sm font-semibold uppercase tracking-wider">
            Configure Your NetCraft Environment
          </p>
        </div>

        <form onSubmit={handleComplete} className="space-y-8">
          
          {/* Setting 1: Organization Name */}
          <div className="bg-slate-900/50 p-6 rounded-xl border border-slate-700">
            <label className="flex items-center gap-2 text-slate-300 text-sm font-bold mb-4 uppercase tracking-wider">
              <Building size={18} className="text-blue-400" />
              Organization / ISP Name
            </label>
            <input 
              type="text" 
              required
              value={formData.orgName}
              onChange={(e) => setFormData({...formData, orgName: e.target.value})}
              className="w-full bg-slate-900 border border-slate-600 text-white rounded-lg py-3 px-4 focus:outline-none focus:border-blue-500 transition-colors"
              placeholder="e.g. Reliance Jio or My Local ISP"
            />
          </div>

          {/* Setting 2: Default Theme Selection */}
          <div className="bg-slate-900/50 p-6 rounded-xl border border-slate-700">
            <label className="flex items-center gap-2 text-slate-300 text-sm font-bold mb-4 uppercase tracking-wider">
              <Palette size={18} className="text-blue-400" />
              Select Default Interface Theme
            </label>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              
              <div 
                onClick={() => setFormData({...formData, theme: 'retro'})}
                className={`cursor-pointer border-2 rounded-lg p-4 text-center transition-all ${formData.theme === 'retro' ? 'border-blue-500 bg-blue-500/10' : 'border-slate-700 hover:border-slate-500'}`}
              >
                <div className="font-mono text-xs mb-2 text-slate-400">1990s MySQL</div>
                <div className="font-bold">Retro Database</div>
              </div>

              <div 
                onClick={() => setFormData({...formData, theme: 'enterprise'})}
                className={`cursor-pointer border-2 rounded-lg p-4 text-center transition-all ${formData.theme === 'enterprise' ? 'border-blue-500 bg-blue-500/10' : 'border-slate-700 hover:border-slate-500'}`}
              >
                <div className="font-sans text-xs mb-2 text-blue-400">Professional</div>
                <div className="font-bold">Enterprise Blue</div>
              </div>

              <div 
                onClick={() => setFormData({...formData, theme: 'modern'})}
                className={`cursor-pointer border-2 rounded-lg p-4 text-center transition-all ${formData.theme === 'modern' ? 'border-blue-500 bg-blue-500/10' : 'border-slate-700 hover:border-slate-500'}`}
              >
                <div className="font-sans font-light text-xs mb-2 text-cyan-400">Sleek & Glass</div>
                <div className="font-bold">Modern UI</div>
              </div>

            </div>
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-4 rounded-xl uppercase tracking-wider transition-all shadow-lg shadow-blue-500/30 disabled:opacity-50 flex justify-center items-center gap-2"
          >
            {loading ? 'Applying Settings...' : <><CheckCircle2 size={20} /> Complete Setup</>}
          </button>
        </form>

      </div>
    </div>
  );
}

export default Setup;