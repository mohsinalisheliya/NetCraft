import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { Lock, User, Mail, UserPlus } from 'lucide-react';

function Register() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ username: '', email: '', password: '', confirmPassword: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    
    // Password match validation
    if (formData.password !== formData.confirmPassword) {
      setError("Passwords don't match!");
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Jab Django connect hoga, yeh API naya user banayegi
      // await axios.post('http://127.0.0.1:8000/api/register/', formData);
      
      console.log("Sending Register Data to Backend:", formData);
      
      // Dummy success for now
      setTimeout(() => {
        navigate('/login'); // Register hone ke baad Login page par bhej dega
      }, 1000);
      
    } catch (err) {
      setError('Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-6 font-sans">
      <div className="bg-slate-800 border border-slate-700 p-8 rounded-2xl shadow-2xl w-full max-w-md">
        
        <div className="text-center mb-8">
          <h1 className="text-3xl font-extrabold text-blue-400 tracking-tight">Join NetCraft</h1>
          <p className="text-slate-400 text-sm mt-2">Create your Enterprise Account</p>
        </div>

        {error && <div className="bg-red-500/10 border border-red-500 text-red-500 p-3 rounded-lg mb-4 text-sm text-center">{error}</div>}

        <form onSubmit={handleRegister} className="space-y-4">
          <div>
            <label className="block text-slate-300 text-xs font-bold mb-1 uppercase">Username</label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-500" size={18} />
              <input type="text" name="username" required onChange={handleChange} className="w-full bg-slate-900 border border-slate-700 text-white rounded-lg py-3 pl-10 pr-4 focus:outline-none focus:border-blue-500" placeholder="Choose a username" />
            </div>
          </div>

          <div>
            <label className="block text-slate-300 text-xs font-bold mb-1 uppercase">Email Address</label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-500" size={18} />
              <input type="email" name="email" required onChange={handleChange} className="w-full bg-slate-900 border border-slate-700 text-white rounded-lg py-3 pl-10 pr-4 focus:outline-none focus:border-blue-500" placeholder="Enter your email" />
            </div>
          </div>

          <div>
            <label className="block text-slate-300 text-xs font-bold mb-1 uppercase">Password</label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-500" size={18} />
              <input type="password" name="password" required onChange={handleChange} className="w-full bg-slate-900 border border-slate-700 text-white rounded-lg py-3 pl-10 pr-4 focus:outline-none focus:border-blue-500" placeholder="Create a password" />
            </div>
          </div>

          <div>
            <label className="block text-slate-300 text-xs font-bold mb-1 uppercase">Confirm Password</label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-500" size={18} />
              <input type="password" name="confirmPassword" required onChange={handleChange} className="w-full bg-slate-900 border border-slate-700 text-white rounded-lg py-3 pl-10 pr-4 focus:outline-none focus:border-blue-500" placeholder="Confirm your password" />
            </div>
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-all disabled:opacity-50 mt-2"
          >
            {loading ? 'Creating Account...' : <><UserPlus size={18} /> Register Account</>}
          </button>
        </form>

        <p className="text-center text-slate-400 text-sm mt-6">
          Already have an account? <Link to="/login" className="text-blue-400 hover:text-blue-300 font-semibold">Sign In</Link>
        </p>
      </div>
    </div>
  );
}

export default Register;