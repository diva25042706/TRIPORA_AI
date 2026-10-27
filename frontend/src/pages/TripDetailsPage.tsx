import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Compass,
  Calendar,
  Wallet,
  Users,
  MapPin,
  RefreshCw,
  Share2,
  Trash2,
  Sparkles,
  CloudSun,
  ShieldCheck,
  Hotel,
  Plane,
  Layers,
  ArrowLeft,
  CheckCircle2,
} from 'lucide-react';
import { tripService } from '../services/tripService';
import { TripResponse, FullTripPlan, ItineraryItem } from '../types';
import { ItineraryView } from '../components/trip/ItineraryView';
import { TripMap } from '../components/map/TripMap';
import { BudgetChart } from '../components/trip/BudgetChart';
import { TransportComparison } from '../components/trip/TransportComparison';
import { HotelComparison } from '../components/trip/HotelComparison';
import { WeatherSafetyPanel } from '../components/trip/WeatherSafetyPanel';
import { AgentStatusTracker } from '../components/trip/AgentStatusTracker';
import { ReplanningModal } from '../components/trip/ReplanningModal';
import { TravelChatDrawer } from '../components/chat/TravelChatDrawer';

export const TripDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [trip, setTrip] = useState<TripResponse | null>(null);
  const [activeTab, setActiveTab] = useState<
    'itinerary' | 'budget' | 'hotels' | 'transports' | 'weather' | 'agents'
  >('itinerary');
  const [selectedMapDay, setSelectedMapDay] = useState<number | null>(null);
  const [isReplanModalOpen, setIsReplanModalOpen] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      loadTrip(id);
    }
  }, [id]);

  const loadTrip = async (tripId: string) => {
    setIsLoading(true);
    try {
      const data = await tripService.getTrip(tripId);
      setTrip(data);
    } catch (err: any) {
      console.error('Failed to load trip:', err);
      setErrorMsg(err.response?.data?.detail || 'Failed to load trip itinerary.');
    } finally {
      setIsLoading(false);
    }
  };

  const handlePlanUpdated = (updatedPlan: FullTripPlan) => {
    if (trip) {
      setTrip({
        ...trip,
        total_budget: updatedPlan.total_budget,
        travel_style: updatedPlan.travel_style,
        full_trip_data: updatedPlan,
      });
    }
  };

  const handleDelete = async () => {
    if (!id || !window.confirm('Are you sure you want to delete this trip itinerary?')) return;
    try {
      await tripService.deleteTrip(id);
      navigate('/dashboard');
    } catch (err) {
      console.error('Failed to delete trip:', err);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-[70vh] flex items-center justify-center">
        <div className="text-center space-y-3">
          <RefreshCw className="w-8 h-8 animate-spin text-[#10B981] mx-auto" />
          <p className="text-xs text-[#5A6D7C] font-semibold">
            Loading your verified trip itinerary...
          </p>
        </div>
      </div>
    );
  }

  if (errorMsg || !trip || !trip.full_trip_data) {
    return (
      <div className="max-w-md mx-auto py-16 px-4 text-center space-y-4">
        <p className="text-sm text-red-600 font-semibold">{errorMsg || 'Trip details not found.'}</p>
        <button
          onClick={() => navigate('/dashboard')}
          className="px-5 py-2.5 rounded-xl bg-[#143628] text-white text-xs font-bold"
        >
          Return to Dashboard
        </button>
      </div>
    );
  }

  const plan = trip.full_trip_data;
  const allActivities: ItineraryItem[] = plan.days.flatMap((d) => d.activities);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8 text-left">
      {/* Top Breadcrumb & Action Toolbar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <button
          onClick={() => navigate('/dashboard')}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#5A6D7C] hover:text-[#0F1E28] transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to All Trips</span>
        </button>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsReplanModalOpen(true)}
            className="px-4 py-2 rounded-xl bg-[#143628] hover:bg-[#1E4D3B] text-white text-xs font-bold flex items-center gap-2 shadow-sm transition-all"
          >
            <RefreshCw className="w-3.5 h-3.5 text-[#10B981]" />
            <span>Replan Itinerary</span>
          </button>

          <button
            onClick={handleDelete}
            className="p-2 text-[#5A6D7C] hover:text-red-600 hover:bg-red-50 rounded-xl transition-colors border border-[#E7E5DF]"
            title="Delete Trip"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Main Trip Header Card */}
      <div className="bg-white rounded-3xl border border-[#E7E5DF] shadow-md p-6 sm:p-8 space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="px-3 py-1 rounded-full bg-[#10B981]/15 text-[#059669] text-xs font-bold uppercase tracking-wider">
              {trip.travel_style} Pace
            </span>
            <span className="px-3 py-1 rounded-full bg-black/5 text-[#2C3E50] text-xs font-semibold">
              {trip.status === 'completed' ? 'Fully Orchestrated' : trip.status}
            </span>
          </div>

          <span className="text-xs text-[#5A6D7C]">
            Trip ID: <code className="text-[#0F1E28]">{trip.id.substring(0, 8)}</code>
          </span>
        </div>

        <div>
          <h1 className="font-editorial text-3xl sm:text-4xl font-bold text-[#0F1E28]">
            {trip.title}
          </h1>
          <div className="flex flex-wrap items-center gap-4 text-xs text-[#5A6D7C] mt-2">
            <span className="flex items-center gap-1 font-semibold text-[#0F1E28]">
              <MapPin className="w-4 h-4 text-[#10B981]" />
              {trip.origin} &rarr; {trip.destination}
            </span>
            <span className="flex items-center gap-1">
              <Calendar className="w-4 h-4 text-[#10B981]" />
              {trip.start_date} to {trip.end_date} ({trip.duration_days} Days)
            </span>
            <span className="flex items-center gap-1">
              <Users className="w-4 h-4 text-[#10B981]" />
              {trip.travellers} Traveller(s)
            </span>
            <span className="flex items-center gap-1 font-bold text-[#143628]">
              <Wallet className="w-4 h-4 text-[#10B981]" />
              {trip.currency} {trip.total_budget.toLocaleString()} Budget
            </span>
          </div>
        </div>

        {/* Itinerary Overview Explanation */}
        <div className="p-4 rounded-2xl bg-[#FAF9F5] border border-[#E7E5DF] text-xs text-[#475569] leading-relaxed flex items-start gap-2.5">
          <Sparkles className="w-4 h-4 text-[#10B981] shrink-0 mt-0.5" />
          <span>{plan.itinerary_explanation}</span>
        </div>
      </div>

      {/* Navigation View Tabs */}
      <div className="flex items-center gap-2 border-b border-[#E7E5DF] overflow-x-auto pb-2 scrollbar-none">
        <button
          onClick={() => setActiveTab('itinerary')}
          className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 whitespace-nowrap transition-all ${
            activeTab === 'itinerary'
              ? 'bg-[#143628] text-white shadow-sm'
              : 'text-[#5A6D7C] hover:text-[#0F1E28] hover:bg-white'
          }`}
        >
          <Compass className="w-4 h-4" />
          <span>Itinerary & Map</span>
        </button>

        <button
          onClick={() => setActiveTab('budget')}
          className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 whitespace-nowrap transition-all ${
            activeTab === 'budget'
              ? 'bg-[#143628] text-white shadow-sm'
              : 'text-[#5A6D7C] hover:text-[#0F1E28] hover:bg-white'
          }`}
        >
          <Wallet className="w-4 h-4" />
          <span>Budget & Contingency</span>
        </button>

        <button
          onClick={() => setActiveTab('hotels')}
          className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 whitespace-nowrap transition-all ${
            activeTab === 'hotels'
              ? 'bg-[#143628] text-white shadow-sm'
              : 'text-[#5A6D7C] hover:text-[#0F1E28] hover:bg-white'
          }`}
        >
          <Hotel className="w-4 h-4" />
          <span>Hotels & Lodging ({plan.hotels.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('transports')}
          className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 whitespace-nowrap transition-all ${
            activeTab === 'transports'
              ? 'bg-[#143628] text-white shadow-sm'
              : 'text-[#5A6D7C] hover:text-[#0F1E28] hover:bg-white'
          }`}
        >
          <Plane className="w-4 h-4" />
          <span>Transit Comparison ({plan.transports.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('weather')}
          className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 whitespace-nowrap transition-all ${
            activeTab === 'weather'
              ? 'bg-[#143628] text-white shadow-sm'
              : 'text-[#5A6D7C] hover:text-[#0F1E28] hover:bg-white'
          }`}
        >
          <CloudSun className="w-4 h-4" />
          <span>Weather & Safety</span>
        </button>

        <button
          onClick={() => setActiveTab('agents')}
          className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 whitespace-nowrap transition-all ${
            activeTab === 'agents'
              ? 'bg-[#143628] text-white shadow-sm'
              : 'text-[#5A6D7C] hover:text-[#0F1E28] hover:bg-white'
          }`}
        >
          <Layers className="w-4 h-4" />
          <span>Agent Telemetry</span>
        </button>
      </div>

      {/* Tab Panels */}
      {activeTab === 'itinerary' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          <div className="lg:col-span-7">
            <ItineraryView
              days={plan.days}
              currency={plan.currency}
              selectedDay={selectedMapDay}
              onDaySelect={(dayNum) => setSelectedMapDay(dayNum)}
            />
          </div>

          <div className="lg:col-span-5 sticky top-28 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-[#0F1E28] uppercase tracking-wider">
                Geographic Route Map
              </h3>
              {selectedMapDay && (
                <button
                  onClick={() => setSelectedMapDay(null)}
                  className="text-[11px] font-semibold text-[#059669] hover:underline"
                >
                  Show All Stops
                </button>
              )}
            </div>

            <TripMap
              destination={plan.destination}
              activities={allActivities}
              selectedDay={selectedMapDay}
            />

            <div className="p-4 rounded-xl bg-white border border-[#E7E5DF] text-[11px] text-[#5A6D7C] space-y-1">
              <p>
                <strong>Attribution:</strong> Map data &copy; OpenStreetMap contributors. Stop sequence connected via estimated travel routes.
              </p>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'budget' && (
        <BudgetChart budget={plan.budget} travellers={plan.travellers} />
      )}

      {activeTab === 'hotels' && (
        <HotelComparison
          hotels={plan.hotels}
          currency={plan.currency}
          durationDays={plan.duration_days}
        />
      )}

      {activeTab === 'transports' && (
        <TransportComparison
          transports={plan.transports}
          currency={plan.currency}
        />
      )}

      {activeTab === 'weather' && (
        <WeatherSafetyPanel
          weatherForecasts={plan.weather_forecasts}
          safetyFindings={plan.safety_findings}
        />
      )}

      {activeTab === 'agents' && (
        <AgentStatusTracker statuses={plan.agent_statuses} />
      )}

      {/* Intelligent Replanning Modal */}
      <ReplanningModal
        isOpen={isReplanModalOpen}
        onClose={() => setIsReplanModalOpen(false)}
        tripId={trip.id}
        totalDays={plan.duration_days}
        currentCurrency={plan.currency}
        onPlanUpdated={handlePlanUpdated}
      />

      {/* Grounded AI Assistant Drawer */}
      <TravelChatDrawer tripId={trip.id} destination={plan.destination} />
    </div>
  );
};
