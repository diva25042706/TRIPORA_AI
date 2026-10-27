import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Compass,
  Sparkles,
  Wallet,
  Plane,
  Hotel,
  CloudSun,
  ShieldCheck,
  ArrowRight,
  MapPin,
  Calendar,
  CheckCircle2,
  Cpu,
  Layers,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const LandingPage: React.FC = () => {
  const { isAuthenticated, loginAsDemo } = useAuth();
  const navigate = useNavigate();

  const handleStartPlanning = () => {
    if (isAuthenticated) {
      navigate('/wizard');
    } else {
      navigate('/wizard');
    }
  };

  const agents = [
    {
      title: 'Trip Planner Agent',
      icon: <Compass className="w-6 h-6 text-[#10B981]" />,
      role: 'Chronological Itinerary Scheduling',
      desc: 'Schedules morning, afternoon, and evening stops. Groups geographically close attractions to minimize transit fatigue.',
    },
    {
      title: 'Budget Optimization Agent',
      icon: <Wallet className="w-6 h-6 text-[#10B981]" />,
      role: 'Deterministic Financial Math',
      desc: 'Calculates exact transport, hotel, dining, and attraction costs in INR with a 5% contingency reserve. Detects deficits.',
    },
    {
      title: 'Transportation Agent',
      icon: <Plane className="w-6 h-6 text-[#10B981]" />,
      role: 'Multi-Modal Route Comparison',
      desc: 'Evaluates flight, express railway, sleeper bus, and private cab options with journey durations and estimated fares.',
    },
    {
      title: 'Hotel & Lodging Agent',
      icon: <Hotel className="w-6 h-6 text-[#10B981]" />,
      role: 'Accommodation Discovery & Ranking',
      desc: 'Discovers verified hotels and boutiques, matches traveller preferences, calculates room costs, and measures distance to sights.',
    },
    {
      title: 'Weather Intelligence Agent',
      icon: <CloudSun className="w-6 h-6 text-[#10B981]" />,
      role: 'Forecast Analysis & Rain Safeguards',
      desc: 'Tracks precipitation and temperature via Open-Meteo. Automatically swaps open-air excursions for sheltered museums when rain threatens.',
    },
    {
      title: 'Safety & Reliability Agent',
      icon: <ShieldCheck className="w-6 h-6 text-[#10B981]" />,
      role: 'Feasibility & Authoritative Checks',
      desc: 'Flags excessive itinerary density, highlights verified vs synthetic POIs, and shares authoritative consular travel baselines.',
    },
  ];

  const featuredDestinations = [
    {
      city: 'Goa',
      country: 'India',
      img: 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80',
      tag: 'Sun & Portuguese Heritage',
      count: '10 Curated Landmarks',
    },
    {
      city: 'Paris',
      country: 'France',
      img: 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=800&q=80',
      tag: 'Art, Architecture & Gastronomy',
      count: '8 Verified Sights',
    },
    {
      city: 'Tokyo',
      country: 'Japan',
      img: 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=800&q=80',
      tag: 'Futurism & Sacred Temples',
      count: '7 Verified Landmarks',
    },
    {
      city: 'Jaipur',
      country: 'India',
      img: 'https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80',
      tag: 'Palaces & Royal Astronomy',
      count: '7 Curated Fortresses',
    },
  ];

  return (
    <div className="space-y-24">
      {/* Hero Section */}
      <section className="relative pt-12 pb-20 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            {/* Left Column: Headlines */}
            <div className="lg:col-span-7 space-y-6 text-left">
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#10B981]/15 text-[#059669] text-xs font-bold border border-[#10B981]/30">
                <Sparkles className="w-3.5 h-3.5" />
                <span>Next-Generation Agentic AI Travel Assistant</span>
              </div>

              <h1 className="font-editorial text-4xl sm:text-6xl font-extrabold text-[#0F1E28] leading-[1.12] tracking-tight">
                Your Journey. <br />
                <span className="text-[#143628] italic">Intelligently</span> Orchestrated.
              </h1>

              <p className="text-base sm:text-lg text-[#5A6D7C] max-w-xl leading-relaxed">
                Six specialized AI agents collaborate across a typed LangGraph workflow to build personalized itineraries, calculate deterministic budgets, benchmark transports, and safeguard your journey from adverse weather.
              </p>

              {/* Action Buttons */}
              <div className="flex flex-wrap items-center gap-4 pt-2">
                <button
                  onClick={handleStartPlanning}
                  className="px-8 py-4 rounded-2xl bg-[#143628] hover:bg-[#1E4D3B] text-white text-base font-bold shadow-lg shadow-[#143628]/20 flex items-center gap-3 transition-all hover:scale-105"
                >
                  <span>Build Your Trip Now</span>
                  <ArrowRight className="w-5 h-5 text-[#10B981]" />
                </button>
                <button
                  onClick={loginAsDemo}
                  className="px-6 py-4 rounded-2xl bg-white hover:bg-[#FAF9F5] text-[#143628] border border-[#E7E5DF] text-sm font-bold shadow-sm transition-all flex items-center gap-2"
                >
                  <Sparkles className="w-4 h-4 text-[#10B981]" />
                  <span>Instant Demo Workspace</span>
                </button>
              </div>

              {/* Trust Badges */}
              <div className="pt-6 grid grid-cols-3 gap-4 border-t border-[#E7E5DF] text-xs text-[#5A6D7C]">
                <div>
                  <span className="font-bold text-sm text-[#0F1E28] block">6 Agents</span>
                  Autonomous LangGraph
                </div>
                <div>
                  <span className="font-bold text-sm text-[#0F1E28] block">INR Native</span>
                  Deterministic Math
                </div>
                <div>
                  <span className="font-bold text-sm text-[#0F1E28] block">Live Weather</span>
                  Rain Self-Healing
                </div>
              </div>
            </div>

            {/* Right Column: Hero Cinematic Showcase Card */}
            <div className="lg:col-span-5 relative">
              <div className="relative rounded-3xl overflow-hidden shadow-2xl border-4 border-white">
                <img
                  src="https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=1000&q=80"
                  alt="Travel Orchestration"
                  className="w-full h-[480px] object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-[#0F1E28]/90 via-[#0F1E28]/30 to-transparent" />

                <div className="absolute bottom-6 left-6 right-6 text-white text-left space-y-2">
                  <span className="bg-[#10B981] text-[#143628] text-[10px] font-extrabold uppercase px-2.5 py-1 rounded-md tracking-wider">
                    Agentic Orchestration Active
                  </span>
                  <h3 className="text-xl font-bold font-editorial">
                    Collaborative Multi-Agent Architecture
                  </h3>
                  <p className="text-xs text-white/80 leading-relaxed">
                    Planner, Budget, Transport, Hotel, Weather, and Safety agents actively coordinating to synthesize your ideal trip.
                  </p>
                </div>
              </div>

              {/* Floating Stat Card */}
              <div className="absolute -bottom-6 -left-6 bg-white/95 backdrop-blur-md p-4 rounded-2xl border border-[#E7E5DF] shadow-xl text-left hidden sm:flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-emerald-100 flex items-center justify-center text-emerald-800">
                  <CheckCircle2 className="w-5 h-5" />
                </div>
                <div>
                  <span className="text-xs font-bold text-[#0F1E28] block">
                    Zero Hallucinated Bookings
                  </span>
                  <span className="text-[11px] text-[#5A6D7C]">
                    Honest provider labeling & live APIs
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Six Specialized AI Agents Showcase */}
      <section id="agents" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto space-y-3 mb-16">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#10B981]/15 text-[#059669] text-xs font-bold">
            <Cpu className="w-3.5 h-3.5" />
            <span>Academic PPT Foundation</span>
          </div>
          <h2 className="font-editorial text-3xl sm:text-5xl font-bold text-[#0F1E28]">
            Six Specialized Autonomous Agents
          </h2>
          <p className="text-sm sm:text-base text-[#5A6D7C]">
            Unlike generic chatbots, TRIPORA deploys a modular swarm of six domain-specific agents connected via LangGraph typed shared state.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent, idx) => (
            <div
              key={idx}
              className="p-6 rounded-2xl bg-white border border-[#E7E5DF] shadow-sm hover:shadow-md hover:border-[#10B981]/40 transition-all text-left flex flex-col justify-between"
            >
              <div>
                <div className="w-12 h-12 rounded-xl bg-[#FAF9F5] border border-[#E7E5DF] flex items-center justify-center mb-4">
                  {agent.icon}
                </div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-[#059669] block mb-1">
                  {agent.role}
                </span>
                <h3 className="text-lg font-bold text-[#0F1E28] mb-2">{agent.title}</h3>
                <p className="text-xs text-[#5A6D7C] leading-relaxed">{agent.desc}</p>
              </div>

              <div className="mt-6 pt-4 border-t border-[#F1F0EB] flex items-center justify-between text-[11px] font-semibold text-[#143628]">
                <span>Validated with Pydantic</span>
                <CheckCircle2 className="w-4 h-4 text-[#10B981]" />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Featured Destinations */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-10 gap-4 text-left">
          <div>
            <h2 className="font-editorial text-3xl sm:text-4xl font-bold text-[#0F1E28]">
              Verified Destination Catalog
            </h2>
            <p className="text-sm text-[#5A6D7C] mt-1">
              Curated locations with verified GPS coordinates, operating hours, and realistic pricing.
            </p>
          </div>
          <button
            onClick={handleStartPlanning}
            className="text-xs font-bold text-[#143628] hover:text-[#10B981] flex items-center gap-1.5 transition-colors self-start"
          >
            <span>Explore All Coordinates</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {featuredDestinations.map((d, i) => (
            <div
              key={i}
              onClick={handleStartPlanning}
              className="group cursor-pointer rounded-2xl overflow-hidden bg-white border border-[#E7E5DF] shadow-sm hover:shadow-lg transition-all"
            >
              <div className="relative h-48 overflow-hidden">
                <img
                  src={d.img}
                  alt={d.city}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent" />
                <span className="absolute bottom-3 left-3 text-white text-base font-bold font-editorial">
                  {d.city}, {d.country}
                </span>
              </div>
              <div className="p-4 text-left">
                <span className="text-[11px] font-semibold text-[#10B981] block">{d.tag}</span>
                <span className="text-xs text-[#5A6D7C] mt-1 flex items-center gap-1">
                  <MapPin className="w-3 h-3 text-[#5A6D7C]" /> {d.count}
                </span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Call to Action Banner */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        <div className="rounded-3xl bg-gradient-to-r from-[#143628] to-[#1E4D3B] p-10 sm:p-16 text-center text-white relative overflow-hidden shadow-2xl">
          <div className="relative z-10 max-w-2xl mx-auto space-y-6">
            <h2 className="font-editorial text-3xl sm:text-5xl font-bold leading-tight">
              Ready to Experience Agentic AI Travel?
            </h2>
            <p className="text-sm sm:text-base text-white/80 leading-relaxed">
              Launch your personalized multi-agent trip planning session. Generate day-by-day itineraries, optimize budgets, and travel with peace of mind.
            </p>
            <div className="pt-2 flex flex-wrap justify-center gap-4">
              <button
                onClick={handleStartPlanning}
                className="px-8 py-4 rounded-2xl bg-[#10B981] hover:bg-[#059669] text-[#143628] text-sm font-bold shadow-lg transition-all hover:scale-105"
              >
                Start Guided Trip Wizard
              </button>
              <button
                onClick={loginAsDemo}
                className="px-6 py-4 rounded-2xl bg-white/10 hover:bg-white/20 text-white border border-white/20 text-sm font-semibold transition-all"
              >
                Sign In with Demo Account
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
