import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Compass, User, Lock, Mail, AlertCircle, Coins } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const RegisterPage: React.FC = () => {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [preferredCurrency, setPreferredCurrency] = useState('INR');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setIsLoading(true);

    try {
      await register(email, password, fullName, preferredCurrency);
      navigate('/dashboard');
    } catch (err: any) {
      console.error('Registration error:', err);
      setErrorMsg(err.response?.data?.detail || 'Failed to create account. Please check your details.');
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
            Create Your Account
          </h2>
          <p className="text-xs text-[#5A6D7C]">
            Join TRIPORA.AI and orchestrate intelligent travel with specialized AI agents.
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
              Full Name
            </label>
            <div className="relative">
              <User className="w-4 h-4 text-[#8C9BA5] absolute left-3.5 top-3" />
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Eleanor Vance"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-[#CBD5E1] text-xs text-[#0F1E28] focus:ring-2 focus:ring-[#10B981] focus:outline-none"
              />
            </div>
          </div>

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
                placeholder="eleanor@example.com"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-[#CBD5E1] text-xs text-[#0F1E28] focus:ring-2 focus:ring-[#10B981] focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label className="text-[#143628] uppercase tracking-wider block mb-1">
              Password (min 6 chars)
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 text-[#8C9BA5] absolute left-3.5 top-3" />
              <input
                type="password"
                required
                minLength={6}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-[#CBD5E1] text-xs text-[#0F1E28] focus:ring-2 focus:ring-[#10B981] focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label className="text-[#143628] uppercase tracking-wider block mb-1">
              Default Currency
            </label>
            <div className="relative">
              <Coins className="w-4 h-4 text-[#8C9BA5] absolute left-3.5 top-3" />
              <select
                value={preferredCurrency}
                onChange={(e) => setPreferredCurrency(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-[#CBD5E1] text-xs text-[#0F1E28] focus:ring-2 focus:ring-[#10B981] focus:outline-none bg-white"
              >
                <option value="INR">INR (₹ Indian Rupee) - Default</option>
                <option value="USD">USD ($ US Dollar)</option>
                <option value="EUR">EUR (€ Euro)</option>
                <option value="GBP">GBP (£ British Pound)</option>
              </select>
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 rounded-xl bg-[#143628] hover:bg-[#1E4D3B] text-white text-xs font-bold transition-all shadow-md disabled:opacity-50 mt-2"
          >
            {isLoading ? 'Creating Account...' : 'Complete Registration'}
          </button>
        </form>

        <p className="text-center text-xs text-[#5A6D7C]">
          Already registered?{' '}
          <Link to="/login" className="text-[#059669] font-bold hover:underline">
            Sign In Here
          </Link>
        </p>
      </div>
    </div>
  );
};
