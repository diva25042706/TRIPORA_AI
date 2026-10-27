import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Compass,
  Plus,
  MapPin,
  Calendar,
  Wallet,
  ArrowRight,
  Trash2,
  Sparkles,
  Luggage,
  Clock,
  TrendingUp,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { tripService } from '../services/tripService';
import { TripSummary } from '../types';

export const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [trips, setTrips] = useState<TripSummary[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [deleteId, setDeleteId] = useState<string | null>(null);

  useEffect(() => {
    loadTrips();
  }, []);

  const loadTrips = async () => {
    setIsLoading(true);
    try {
      const data = await tripService.listTrips();
      setTrips(data);
    } catch (err) {
      console.error('Failed to load trips:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteTrip = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!window.confirm('Are you sure you want to delete this trip itinerary?')) return;

    try {
      await tripService.deleteTrip(id);
      setTrips((prev) => prev.filter((t) => t.id !== id));
    } catch (err) {
      console.error('Failed to delete trip:', err);
    }
  };

  // Calculations
  const totalPlannedBudget = trips.reduce((acc, t) => acc + t.total_budget, 0);
  const totalDaysPlanned = trips.reduce((acc, t) => acc + t.duration_days, 0);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10 text-left">
      {/* Welcome Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-[#E7E5DF]">
        <div>
          <span className="text-xs font-bold text-[#059669] uppercase tracking-wider">
            Traveler Dashboard
          </span>
          <div className="flex flex-wrap items-center gap-3 mt-1">
            <h1 className="font-editorial text-3xl sm:text-4xl font-bold text-[#0F1E28]">
              Welcome back, {user?.full_name || 'Explorer'}
            </h1>
            <Link
              to="/settings"
              className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-emerald-50 hover:bg-emerald-100 text-[#059669] border border-emerald-200 transition-colors"
              title="Change your traveler profile name"
            >
              Change Name
            </Link>
          </div>
          <p className="text-xs text-[#5A6D7C] mt-1">
            Review your autonomous itineraries, replan active journeys, and monitor budget allocations.
          </p>
        </div>

        <Link
          to="/wizard"
          className="px-6 py-3 rounded-2xl bg-[#143628] hover:bg-[#1E4D3B] text-white text-xs font-bold shadow-md shadow-[#143628]/15 flex items-center gap-2 transition-all self-start"
        >
          <Plus className="w-4 h-4 text-[#10B981]" />
          <span>Plan New Journey</span>
        </Link>
      </div>

      {/* Stats Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-5 rounded-2xl bg-white border border-[#E7E5DF] shadow-sm flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-emerald-50 text-[#059669] flex items-center justify-center shrink-0">
            <Luggage className="w-6 h-6" />
          </div>
          <div>
            <span className="text-[10px] font-semibold text-[#8C9BA5] uppercase">Total Journeys</span>
            <div className="text-2xl font-bold text-[#0F1E28]">{trips.length}</div>
            <span className="text-[11px] text-[#5A6D7C]">Orchestrated with AI</span>
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-white border border-[#E7E5DF] shadow-sm flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
            <Calendar className="w-6 h-6" />
          </div>
          <div>
            <span className="text-[10px] font-semibold text-[#8C9BA5] uppercase">Total Days Planned</span>
            <div className="text-2xl font-bold text-[#0F1E28]">{totalDaysPlanned}</div>
            <span className="text-[11px] text-[#5A6D7C]">Scheduled with time slots</span>
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-white border border-[#E7E5DF] shadow-sm flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center shrink-0">
            <Wallet className="w-6 h-6" />
          </div>
          <div>
            <span className="text-[10px] font-semibold text-[#8C9BA5] uppercase">Combined Budget</span>
            <div className="text-2xl font-bold text-[#0F1E28]">
              {user?.preferred_currency || 'INR'} {totalPlannedBudget.toLocaleString()}
            </div>
            <span className="text-[11px] text-[#059669] font-medium">Deterministic accounting</span>
          </div>
        </div>
      </div>

      {/* Saved Trips Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="font-editorial text-2xl font-bold text-[#0F1E28]">
            Your Saved Itineraries
          </h2>
          <span className="text-xs text-[#5A6D7C] font-semibold">
            {trips.length} {trips.length === 1 ? 'Trip' : 'Trips'} Available
          </span>
        </div>

        {isLoading ? (
          <div className="p-12 text-center text-[#5A6D7C] text-xs">
            Loading your saved trips...
          </div>
        ) : trips.length === 0 ? (
          /* Empty State */
          <div className="bg-white border border-[#E7E5DF] rounded-3xl p-12 text-center max-w-lg mx-auto space-y-4 shadow-sm">
            <div className="w-14 h-14 rounded-2xl bg-[#FAF9F5] border border-[#E7E5DF] text-[#10B981] flex items-center justify-center mx-auto">
              <Compass className="w-8 h-8" />
            </div>
            <h3 className="font-editorial text-xl font-bold text-[#0F1E28]">
              No Travel Plans Yet
            </h3>
            <p className="text-xs text-[#5A6D7C] leading-relaxed">
              You haven't planned any trips yet. Launch our multi-agent trip wizard to generate day-by-day itineraries with live weather, maps, and budget reconciliation.
            </p>
            <Link
              to="/wizard"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-[#143628] text-white text-xs font-bold shadow-md hover:bg-[#1E4D3B] transition-all"
            >
              <Plus className="w-4 h-4 text-[#10B981]" />
              <span>Create Your First Trip</span>
            </Link>
          </div>
        ) : (
          /* Trip Cards Grid */
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {trips.map((t) => (
              <div
                key={t.id}
                onClick={() => navigate(`/trips/${t.id}`)}
                className="bg-white rounded-2xl border border-[#E7E5DF] shadow-sm hover:shadow-lg hover:border-[#10B981]/50 cursor-pointer transition-all flex flex-col justify-between overflow-hidden group"
              >
                <div className="p-6 space-y-4">
                  <div className="flex items-start justify-between gap-2">
                    <span className="px-2.5 py-0.5 rounded-full bg-[#10B981]/15 text-[#059669] text-[10px] font-bold uppercase tracking-wider">
                      {t.travel_style} Pace
                    </span>
                    <button
                      onClick={(e) => handleDeleteTrip(t.id, e)}
                      className="p-1.5 text-[#8C9BA5] hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                      title="Delete Trip"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>

                  <div>
                    <h3 className="font-editorial text-xl font-bold text-[#0F1E28] group-hover:text-[#10B981] transition-colors">
                      {t.title}
                    </h3>
                    <div className="flex items-center gap-1.5 text-xs text-[#5A6D7C] mt-1">
                      <MapPin className="w-3.5 h-3.5 text-[#10B981]" />
                      <span>{t.origin} &rarr; {t.destination}</span>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-2 pt-3 border-t border-[#F1F0EB] text-xs">
                    <div>
                      <span className="text-[10px] font-semibold text-[#8C9BA5] uppercase block">
                        Dates & Duration
                      </span>
                      <span className="font-semibold text-[#0F1E28] flex items-center gap-1 mt-0.5">
                        <Calendar className="w-3.5 h-3.5 text-[#5A6D7C]" />
                        {t.duration_days} Days ({t.start_date})
                      </span>
                    </div>

                    <div>
                      <span className="text-[10px] font-semibold text-[#8C9BA5] uppercase block">
                        Budget Limit
                      </span>
                      <span className="font-bold text-[#143628] mt-0.5 block">
                        {t.currency} {t.total_budget.toLocaleString()}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="px-6 py-3 bg-[#FAF9F5] border-t border-[#E7E5DF] flex items-center justify-between text-xs font-bold text-[#143628]">
                  <span className="flex items-center gap-1 text-[11px] text-[#059669]">
                    <Sparkles className="w-3.5 h-3.5 text-[#10B981]" /> Fully Orchestrated
                  </span>
                  <div className="flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                    <span>View Itinerary</span>
                    <ArrowRight className="w-3.5 h-3.5 text-[#10B981]" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
