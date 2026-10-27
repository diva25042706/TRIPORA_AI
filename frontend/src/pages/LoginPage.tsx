import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Compass, Sparkles, Lock, Mail, AlertCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const { login, loginAsDemo } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setIsLoading(true);

    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err: any) {
      console.error('Login error:', err);
      setErrorMsg(err.response?.data?.detail || 'Incorrect email or password.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemo = async () => {
    setIsLoading(true);
    try {
      await loginAsDemo();
      navigate('/dashboard');
    } catch (err) {
      setErrorMsg('Failed to log in with demo credentials.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4 py-12">
      <div className="max-w-md w-full bg-white rounded-3xl border border-[#E7E5DF] shadow-xl p-8 space-y-6 text-left">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-[#143628] text-white flex items-center justify-center mx-auto shadow-md">
            <Compass className="w-7 h-7 text-[#10B981]" />
          </div>
          <h2 className="font-editorial text-2xl font-bold text-[#0F1E28]">
            Welcome Back to TRIPORA
          </h2>
          <p className="text-xs text-[#5A6D7C]">
            Sign in to access your saved itineraries and multi-agent travel plans.
          </p>
        </div>

        {errorMsg && (
          <div className="p-3 bg-red-50 border border-red-200 text-red-700 text-xs rounded-xl flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4 text-xs font-semibold">
          <div>
            <label className="text-[#143628] uppercase tracking-wider block mb-1">
              Email Address
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 text-[#8C9BA5] absolute left-3.5 top-3" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="traveller@example.com"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-[#CBD5E1] text-xs text-[#0F1E28] focus:ring-2 focus:ring-[#10B981] focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label className="text-[#143628] uppercase tracking-wider block mb-1">
              Password
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 text-[#8C9BA5] absolute left-3.5 top-3" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-[#CBD5E1] text-xs text-[#0F1E28] focus:ring-2 focus:ring-[#10B981] focus:outline-none"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 rounded-xl bg-[#143628] hover:bg-[#1E4D3B] text-white text-xs font-bold transition-all shadow-md disabled:opacity-50 mt-2"
          >
            {isLoading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>

        <div className="relative flex py-1 items-center">
          <div className="flex-grow border-t border-[#E7E5DF]"></div>
          <span className="flex-shrink mx-4 text-[10px] text-[#8C9BA5] uppercase font-bold">
            Or Quick Access
          </span>
          <div className="flex-grow border-t border-[#E7E5DF]"></div>
        </div>

        <button
          type="button"
          onClick={handleDemo}
          disabled={isLoading}
          className="w-full py-2.5 rounded-xl bg-[#10B981]/10 hover:bg-[#10B981]/20 border border-[#10B981]/30 text-[#059669] text-xs font-bold flex items-center justify-center gap-2 transition-all"
        >
          <Sparkles className="w-4 h-4 text-[#10B981]" />
          <span>One-Click Demo Login (demo@tripora.ai)</span>
        </button>

        <p className="text-center text-xs text-[#5A6D7C]">
          Don't have an account?{' '}
          <Link to="/register" className="text-[#059669] font-bold hover:underline">
            Register Here
          </Link>
        </p>
      </div>
    </div>
  );
};
