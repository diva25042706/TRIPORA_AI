import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Compass, Sparkles, MapPin, Plus, LogOut, User as UserIcon, LayoutDashboard, Settings } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout, loginAsDemo } = useAuth();
  const navigate = useNavigate();

  return (
    <header className="sticky top-0 z-50 backdrop-blur-md bg-[#FAF9F5]/90 border-b border-[#E7E5DF] transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-11 h-11 rounded-xl bg-gradient-to-tr from-[#143628] to-[#10B981] flex items-center justify-center text-white shadow-md shadow-[#143628]/15 group-hover:scale-105 transition-transform duration-300">
            <Compass className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-editorial text-2xl font-bold tracking-tight text-[#0F1E28]">
                TRIPORA<span className="text-[#10B981]">.AI</span>
              </span>
              <span className="bg-[#10B981]/15 text-[#059669] text-[10px] font-bold px-1.5 py-0.5 rounded-full tracking-wider uppercase">
                Multi-Agent
              </span>
            </div>
            <p className="text-[11px] font-medium text-[#5A6D7C] tracking-wide hidden sm:block">
              Your Journey. Intelligently Orchestrated.
            </p>
          </div>
        </Link>

        {/* Navigation Links */}
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-[#2C3E50]">
          <Link to="/" className="hover:text-[#10B981] transition-colors">
            Discover
          </Link>
          <a href="/#agents" className="hover:text-[#10B981] transition-colors">
            Six Specialized Agents
          </a>
          {isAuthenticated && (
            <Link to="/dashboard" className="hover:text-[#10B981] flex items-center gap-1.5 transition-colors">
              <LayoutDashboard className="w-4 h-4 text-[#10B981]" />
              My Dashboard
            </Link>
          )}
        </nav>

        {/* Action Controls */}
        <div className="flex items-center gap-3">
          {isAuthenticated ? (
            <div className="flex items-center gap-3">
              <Link
                to="/wizard"
                className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#143628] hover:bg-[#1E4D3B] text-white text-sm font-semibold shadow-sm hover:shadow transition-all duration-200"
              >
                <Plus className="w-4 h-4 text-[#10B981]" />
                <span className="hidden sm:inline">Plan New Trip</span>
              </Link>
              <div className="h-6 w-px bg-[#E2E0D8] mx-1" />
              <Link
                to="/settings"
                className="p-2 text-[#5A6D7C] hover:text-[#0F1E28] hover:bg-black/5 rounded-lg transition-colors"
                title="Settings"
              >
                <Settings className="w-5 h-5" />
              </Link>
              <button
                onClick={() => {
                  logout();
                  navigate('/');
                }}
                className="p-2 text-[#5A6D7C] hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                title="Logout"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2 sm:gap-3">
              <button
                onClick={loginAsDemo}
                className="px-3.5 py-2 text-xs font-semibold text-[#059669] bg-[#10B981]/10 hover:bg-[#10B981]/20 rounded-xl border border-[#10B981]/25 transition-all flex items-center gap-1.5"
              >
                <Sparkles className="w-3.5 h-3.5 text-[#10B981]" />
                <span className="hidden sm:inline">Quick Demo Login</span>
                <span className="sm:hidden">Demo</span>
              </button>
              <Link
                to="/login"
                className="px-4 py-2 text-sm font-semibold text-[#0F1E28] hover:text-[#10B981] transition-colors"
              >
                Sign In
              </Link>
              <Link
                to="/register"
                className="px-4 py-2 rounded-xl bg-[#143628] hover:bg-[#1E4D3B] text-white text-sm font-semibold shadow-sm transition-all"
              >
                Get Started
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
