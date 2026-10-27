import React, { useState, useEffect } from 'react';
import { User, Coins, Shield, Cpu, CheckCircle2, Server, Globe, AlertCircle, RefreshCw } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

export const SettingsPage: React.FC = () => {
  const { user, updateProfile } = useAuth();
  const [fullName, setFullName] = useState(user?.full_name || 'Divakaran');
  const [email, setEmail] = useState(user?.email || 'demo@tripora.ai');
  const [preferredCurrency, setPreferredCurrency] = useState(user?.preferred_currency || 'INR');
  const [healthData, setHealthData] = useState<any>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    checkHealth();
  }, []);

  useEffect(() => {
    if (user) {
      setFullName(user.full_name || '');
      setEmail(user.email || '');
      setPreferredCurrency(user.preferred_currency || 'INR');
    }
  }, [user]);

  const checkHealth = async () => {
    try {
      const res = await api.get('/health/');
      setHealthData(res.data);
    } catch (err) {
      console.error('Failed to fetch system health:', err);
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setErrorMsg(null);

    try {
      await updateProfile(fullName, email, preferredCurrency);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3500);
    } catch (err: any) {
      console.error('Update profile error:', err);
      setErrorMsg(err.response?.data?.detail || 'Failed to update profile settings.');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8 text-left">
      <div>
        <span className="text-xs font-bold text-[#059669] uppercase tracking-wider">
          Configuration & Preferences
        </span>
        <h1 className="font-editorial text-3xl font-bold text-[#0F1E28] mt-1">
          User Settings & Profile Configuration
        </h1>
        <p className="text-xs text-[#5A6D7C] mt-1">
          Customize your traveler name, email address, currency preferences, and review system orchestrator status.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* User Profile & Currency Settings */}
        <div className="bg-white p-6 sm:p-8 rounded-3xl border border-[#E7E5DF] shadow-sm space-y-6">
          <div className="flex items-center gap-2.5 pb-3 border-b border-[#E7E5DF]">
            <User className="w-5 h-5 text-[#10B981]" />
            <h3 className="text-base font-bold text-[#0F1E28]">
              Account Profile & Traveler Identity
            </h3>
          </div>

          <form onSubmit={handleSave} className="space-y-4 text-xs font-semibold">
            {errorMsg && (
              <div className="p-3 bg-red-50 text-red-700 rounded-xl text-xs flex items-center gap-2 border border-red-200">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{errorMsg}</span>
              </div>
            )}

            <div>
              <label className="text-[#143628] uppercase tracking-wider block mb-1">
                Full Name
              </label>
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Enter your name"
                className="w-full px-4 py-2.5 rounded-xl border border-[#CBD5E1] text-xs text-[#0F1E28] focus:ring-2 focus:ring-[#10B981] focus:outline-none"
              />
            </div>

            <div>
              <label className="text-[#143628] uppercase tracking-wider block mb-1">
                Registered Email
              </label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="traveller@example.com"
                className="w-full px-4 py-2.5 rounded-xl border border-[#CBD5E1] text-xs text-[#0F1E28] focus:ring-2 focus:ring-[#10B981] focus:outline-none"
              />
            </div>

            <div>
              <label className="text-[#143628] uppercase tracking-wider block mb-1">
                Preferred Currency Standard
              </label>
              <div className="relative">
                <Coins className="w-4 h-4 text-[#8C9BA5] absolute left-3.5 top-3" />
                <select
                  value={preferredCurrency}
                  onChange={(e) => setPreferredCurrency(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-[#CBD5E1] text-xs text-[#0F1E28] bg-white focus:ring-2 focus:ring-[#10B981] focus:outline-none"
                >
                  <option value="INR">INR (₹ Indian Rupee) - Primary Academic Spec</option>
                  <option value="USD">USD ($ US Dollar)</option>
                  <option value="EUR">EUR (€ Euro)</option>
                  <option value="GBP">GBP (£ British Pound)</option>
                </select>
              </div>
            </div>

            {saveSuccess && (
              <div className="p-3 bg-emerald-50 text-emerald-800 rounded-xl text-xs flex items-center gap-2 border border-emerald-200 animate-fade-in">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>Profile and traveler name updated successfully!</span>
              </div>
            )}

            <button
              type="submit"
              disabled={isSaving}
              className="px-6 py-2.5 rounded-xl bg-[#143628] hover:bg-[#1E4D3B] text-white text-xs font-bold transition-all shadow-sm flex items-center gap-2 disabled:opacity-50"
            >
              {isSaving ? (
                <>
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  <span>Saving...</span>
                </>
              ) : (
                <span>Save Profile Changes</span>
              )}
            </button>
          </form>
        </div>

        {/* System & Architecture Diagnostics */}
        <div className="bg-white p-6 sm:p-8 rounded-3xl border border-[#E7E5DF] shadow-sm space-y-6">
          <div className="flex items-center gap-2.5 pb-3 border-b border-[#E7E5DF]">
            <Server className="w-5 h-5 text-[#10B981]" />
            <h3 className="text-base font-bold text-[#0F1E28]">
              Multi-Agent Orchestrator Status
            </h3>
          </div>

          <div className="space-y-4 text-xs">
            <div className="p-4 rounded-2xl bg-[#FAF9F5] border border-[#E7E5DF] space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-[#0F1E28]">Orchestration Framework</span>
                <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">
                  LangGraph 1.2+ Active
                </span>
              </div>
              <p className="text-[11px] text-[#5A6D7C]">
                Shared state typed dict with conditional transitions, conflict resolution, and deterministic budgeting.
              </p>
            </div>

            <div className="p-4 rounded-2xl bg-[#FAF9F5] border border-[#E7E5DF] space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-[#0F1E28]">System Health & Mode</span>
                <span className="px-2 py-0.5 rounded bg-blue-100 text-blue-800 font-bold text-[10px]">
                  {healthData?.demo_mode ? 'Deterministic Fallback / Offline Ready' : 'Live Production'}
                </span>
              </div>
              <p className="text-[11px] text-[#5A6D7C]">
                When external paid credentials are not present, TRIPORA utilizes realistic geographic and climatological algorithms without failing.
              </p>
            </div>

            <div className="space-y-2">
              <h4 className="text-[11px] font-bold text-[#143628] uppercase tracking-wider">
                Configured Data Adapters:
              </h4>
              <ul className="space-y-1.5 text-[11px] text-[#475569]">
                <li className="flex items-center justify-between p-2 rounded-lg bg-black/5">
                  <span>Open-Meteo Meteorological API</span>
                  <span className="text-emerald-700 font-bold">Online</span>
                </li>
                <li className="flex items-center justify-between p-2 rounded-lg bg-black/5">
                  <span>OpenStreetMap Nominatim Geocoding</span>
                  <span className="text-emerald-700 font-bold">Online</span>
                </li>
                <li className="flex items-center justify-between p-2 rounded-lg bg-black/5">
                  <span>TRIPORA Distance & Fare Benchmark</span>
                  <span className="text-emerald-700 font-bold">Verified</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
