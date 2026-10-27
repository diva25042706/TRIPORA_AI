import React from 'react';
import { Compass, Shield, CloudSun, Hotel, Plane, Wallet, Cpu } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-[#143628] text-white/80 border-t border-white/10 mt-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10">
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-[#10B981] flex items-center justify-center text-[#143628] font-bold">
                <Compass className="w-6 h-6" />
              </div>
              <span className="font-editorial text-2xl font-bold tracking-tight text-white">
                TRIPORA<span className="text-[#10B981]">.AI</span>
              </span>
            </div>
            <p className="text-sm text-white/70 max-w-md leading-relaxed">
              Agentic AI Travel Planner — Intelligent multi-agent collaborative trip planning, deterministic financial reconciliation, real-time weather safeguarding, and context-grounded AI travel assistance.
            </p>
            <div className="flex items-center gap-2 pt-2">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-white/10 text-emerald-300 border border-emerald-400/20">
                <Cpu className="w-3.5 h-3.5" /> LangGraph 1.2 Multi-Agent Engine
              </span>
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-white/10 text-amber-300 border border-amber-400/20">
                Deterministic INR Budgeting
              </span>
            </div>
          </div>

          <div>
            <h4 className="text-white text-sm font-semibold uppercase tracking-wider mb-4">
              Specialized Agents
            </h4>
            <ul className="space-y-2.5 text-sm text-white/70">
              <li className="flex items-center gap-2">
                <Compass className="w-4 h-4 text-emerald-400" /> Trip Planner Agent
              </li>
              <li className="flex items-center gap-2">
                <Wallet className="w-4 h-4 text-emerald-400" /> Budget Optimization Agent
              </li>
              <li className="flex items-center gap-2">
                <Plane className="w-4 h-4 text-emerald-400" /> Transportation Agent
              </li>
              <li className="flex items-center gap-2">
                <Hotel className="w-4 h-4 text-emerald-400" /> Hotel & Lodging Agent
              </li>
              <li className="flex items-center gap-2">
                <CloudSun className="w-4 h-4 text-emerald-400" /> Weather Intelligence Agent
              </li>
              <li className="flex items-center gap-2">
                <Shield className="w-4 h-4 text-emerald-400" /> Safety & Reliability Agent
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-white text-sm font-semibold uppercase tracking-wider mb-4">
              Integrations & Standards
            </h4>
            <ul className="space-y-2.5 text-sm text-white/70">
              <li>OpenStreetMap & Nominatim</li>
              <li>Open-Meteo Meteorological API</li>
              <li>IRCTC / Intercity Fare Models</li>
              <li>Transparent Estimates (Demo Mode)</li>
              <li>Pydantic Structured Validation</li>
              <li>Strict Data Ownership Checks</li>
            </ul>
          </div>
        </div>

        <div className="border-t border-white/10 mt-12 pt-8 flex flex-col sm:flex-row items-center justify-between text-xs text-white/50 gap-4">
          <p>© {new Date().getFullYear()} TRIPORA.AI. All rights reserved. Built for Agentic AI Travel Assistant.</p>
          <p className="flex items-center gap-1">
            <span>Orchestrated with</span>
            <span className="text-emerald-400 font-semibold">LangGraph & FastAPI</span>
          </p>
        </div>
      </div>
    </footer>
  );
};
