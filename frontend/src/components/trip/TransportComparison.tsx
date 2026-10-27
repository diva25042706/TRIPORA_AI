import React, { useState } from 'react';
import { TransportOption } from '../../types';
import { Plane, Train, Bus, Car, CheckCircle2, Clock, MapPin, AlertCircle, Info, ShieldCheck, ArrowRightLeft, ExternalLink, Calendar, Ticket } from 'lucide-react';

interface TransportComparisonProps {
  transports: TransportOption[];
  currency: string;
}

export const TransportComparison: React.FC<TransportComparisonProps> = ({ transports = [], currency }) => {
  const [filterMode, setFilterMode] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'recommended' | 'duration' | 'price'>('recommended');

  const isFlight = (mode: string) => {
    const m = mode.toLowerCase();
    return m.includes('flight') || m.includes('airline') || m.includes('aviation') || m.includes('plane');
  };

  const isTrain = (mode: string) => {
    const m = mode.toLowerCase();
    return m.includes('train') || m.includes('rail');
  };

  const isBus = (mode: string) => {
    const m = mode.toLowerCase();
    return m.includes('bus') || m.includes('coach');
  };

  const isCab = (mode: string) => {
    const m = mode.toLowerCase();
    return m.includes('cab') || m.includes('car') || m.includes('taxi') || m.includes('self-drive');
  };

  const getModeIcon = (mode: string) => {
    if (isFlight(mode)) return <Plane className="w-5 h-5 text-blue-600" />;
    if (isTrain(mode)) return <Train className="w-5 h-5 text-emerald-600" />;
    if (isBus(mode)) return <Bus className="w-5 h-5 text-amber-600" />;
    return <Car className="w-5 h-5 text-purple-600" />;
  };

  // Pre-calculate counts for each mode
  const flightCount = transports.filter((t) => isFlight(t.mode)).length;
  const trainCount = transports.filter((t) => isTrain(t.mode)).length;
  const busCount = transports.filter((t) => isBus(t.mode)).length;
  const cabCount = transports.filter((t) => isCab(t.mode)).length;

  // Filter transports
  const filtered = transports.filter((t) => {
    if (filterMode === 'all') return true;
    if (filterMode === 'flight') return isFlight(t.mode);
    if (filterMode === 'train') return isTrain(t.mode);
    if (filterMode === 'bus') return isBus(t.mode);
    if (filterMode === 'cab') return isCab(t.mode);
    return true;
  });

  // Sort transports
  const sorted = [...filtered].sort((a, b) => {
    if (sortBy === 'duration') return a.duration_hours - b.duration_hours;
    if (sortBy === 'price') return a.estimated_cost - b.estimated_cost;
    // Default recommended first
    if (a.is_recommended && !b.is_recommended) return -1;
    if (!a.is_recommended && b.is_recommended) return 1;
    return a.duration_hours - b.duration_hours;
  });

  return (
    <div className="space-y-6">
      {/* Route-Aware Engine Header Info Box */}
      <div className="bg-[#FAF9F5] p-4 rounded-2xl border border-[#E7E5DF] flex items-start gap-3 shadow-sm">
        <Info className="w-5 h-5 text-[#059669] shrink-0 mt-0.5" />
        <div className="text-xs text-[#5A6D7C] leading-relaxed space-y-1 text-left">
          <p>
            <strong className="text-[#0F1E28]">Route-Aware Multi-Modal Transit Engine:</strong> Transportation options are evaluated against verified geographic coordinates, active commercial airports, rail networks, and road corridors. Modes are disqualified if verified infrastructure does not exist for the journey.
          </p>
        </div>
      </div>

      {/* Disqualified Flight Advisory Banner when 0 flights are verified for destination */}
      {flightCount === 0 && (
        <div className="p-3.5 bg-amber-50/80 border border-amber-200/90 rounded-2xl flex items-start gap-3 text-xs text-amber-950 shadow-sm text-left">
          <AlertCircle className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
          <div className="space-y-0.5">
            <span className="font-bold text-amber-900">No Commercial Passenger Airport Serving Destination</span>
            <p className="text-[11px] text-amber-800 leading-relaxed">
              Commercial scheduled flights are disqualified because the destination has no commercial airport (e.g. Tiruvannamalai). High-safety Southern Railway services, express buses, and national highway road transport are verified and recommended below.
            </p>
          </div>
        </div>
      )}

      {/* Controls: Mode Filter Chips & Sort Selector */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
        <div className="flex flex-wrap gap-1.5">
          {[
            { id: 'all', label: `All Eligible (${transports.length})` },
            { id: 'cab', label: `Cab / Road (${cabCount})` },
            { id: 'train', label: `Express Rail (${trainCount})` },
            { id: 'bus', label: `Intercity Bus (${busCount})` },
            { id: 'flight', label: `Flights (${flightCount})` },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => setFilterMode(item.id)}
              className={`px-3 py-1.5 rounded-xl font-bold border transition-all ${
                filterMode === item.id
                  ? 'bg-[#143628] text-white border-[#143628] shadow-sm'
                  : 'bg-white text-[#5A6D7C] border-[#E7E5DF] hover:border-[#10B981]'
              }`}
            >
              {item.label}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-2 self-start sm:self-auto">
          <span className="text-[#8C9BA5] font-semibold">Sort by:</span>
          <select
            value={sortBy}
            onChange={(e: any) => setSortBy(e.target.value)}
            className="px-2.5 py-1.5 rounded-xl bg-white border border-[#CBD5E1] font-semibold text-[#0F1E28] focus:outline-none focus:ring-1 focus:ring-[#10B981]"
          >
            <option value="recommended">Recommended First</option>
            <option value="duration">Fastest Duration</option>
            <option value="price">Lowest Fare</option>
          </select>
        </div>
      </div>

      {/* Empty State when filter yields 0 options */}
      {sorted.length === 0 && (
        <div className="p-8 text-center bg-white rounded-2xl border border-dashed border-[#CBD5E1] space-y-3">
          <div className="w-12 h-12 rounded-full bg-amber-50 text-amber-700 flex items-center justify-center mx-auto">
            <AlertCircle className="w-6 h-6" />
          </div>
          <h4 className="text-sm font-bold text-[#0F1E28]">
            {filterMode === 'flight'
              ? 'No Commercial Passenger Flights on this Route'
              : 'No verified options matching this filter'}
          </h4>
          <p className="text-xs text-[#5A6D7C] max-w-md mx-auto leading-relaxed">
            {filterMode === 'flight'
              ? 'Only 6 certified commercial passenger airports operate in Tamil Nadu (Chennai MAA, Coimbatore CJB, Madurai IXM, Tiruchirappalli TRZ, Salem SXV, Thoothukudi TCR). Direct flights to destinations without commercial airports are strictly disqualified to prevent hallucinated bookings.'
              : 'Try selecting "All Eligible" above to see the active transportation modes evaluated for this trip.'}
          </p>
          <button
            onClick={() => setFilterMode('all')}
            className="px-4 py-2 rounded-xl bg-[#143628] text-white text-xs font-bold hover:bg-[#1E4D3B] transition-colors"
          >
            View All Verified Options
          </button>
        </div>
      )}

      {/* Transports Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {sorted.map((t) => (
          <div
            key={t.id}
            className={`p-5 rounded-2xl border transition-all text-left flex flex-col justify-between ${
              t.is_recommended
                ? 'bg-white border-[#10B981] shadow-md ring-2 ring-[#10B981]/25'
                : 'bg-white border-[#E7E5DF] shadow-sm hover:border-[#CBD5E1]'
            }`}
          >
            <div>
              {/* Header: Mode & Badges */}
              <div className="flex items-start justify-between gap-3 mb-3">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-black/5 flex items-center justify-center shrink-0">
                    {getModeIcon(t.mode)}
                  </div>
                  <div>
                    <h4 className="text-base font-bold text-[#0F1E28]">{t.mode}</h4>
                    <span className="text-xs text-[#5A6D7C] flex items-center gap-1 font-semibold">
                      <MapPin className="w-3.5 h-3.5 text-[#10B981]" /> {t.origin} &rarr; {t.destination}
                    </span>
                  </div>
                </div>

                <div className="flex flex-col items-end gap-1">
                  {t.is_recommended && (
                    <span className="px-2.5 py-1 rounded-full bg-[#10B981]/15 text-[#059669] text-[11px] font-bold flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Recommended
                    </span>
                  )}
                  {t.verification_status === 'verified' ? (
                    <span className="px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200 text-[10px] font-bold flex items-center gap-1">
                      <ShieldCheck className="w-3 h-3 text-emerald-600" /> Verified Route
                    </span>
                  ) : (
                    <span className="px-2 py-0.5 rounded-md bg-amber-50 text-amber-800 border border-amber-200 text-[10px] font-bold">
                      Estimated Benchmark
                    </span>
                  )}
                </div>
              </div>

              {/* Verified Service Specific Badges: Train Name/Number or Flight Operator */}
              {(t.train_number || t.train_name || t.flight_operator || t.flight_number) && (
                <div className="mb-2.5 px-3 py-1.5 rounded-xl bg-emerald-50/70 border border-emerald-200/80 text-emerald-950 text-xs flex items-center justify-between gap-2">
                  <div className="flex items-center gap-1.5 font-bold truncate">
                    <Ticket className="w-3.5 h-3.5 text-emerald-700 shrink-0" />
                    <span className="truncate">
                      {t.train_name ? `${t.train_name} ${t.train_number ? `(#${t.train_number})` : ''}` : ''}
                      {t.flight_operator ? `${t.flight_operator} ${t.flight_number ? `(${t.flight_number})` : ''}` : ''}
                    </span>
                  </div>
                  {t.departure_time && (
                    <span className="text-[10px] font-bold text-emerald-800 bg-emerald-100/70 px-2 py-0.5 rounded-md shrink-0">
                      Dep: {t.departure_time.split(' ')[0]}
                    </span>
                  )}
                </div>
              )}

              {/* Station / Terminal / Airport Breakdown when available */}
              {(t.origin_station_or_airport || t.destination_station_or_airport) && (
                <div className="mb-3 px-3 py-2 bg-[#FAF9F5] rounded-xl border border-[#E7E5DF] text-[11px] text-[#475569] flex items-center justify-between gap-2">
                  <span className="font-semibold truncate">{t.origin_station_or_airport || t.origin}</span>
                  <ArrowRightLeft className="w-3.5 h-3.5 text-[#10B981] shrink-0" />
                  <span className="font-semibold truncate text-right">{t.destination_station_or_airport || t.destination}</span>
                </div>
              )}

              {/* Verified Schedule & Live Status Row */}
              {(t.departure_time || t.live_availability_status) && (
                <div className="mb-3 px-3 py-2 bg-slate-50/80 rounded-xl border border-slate-200 text-[11px] text-slate-700 space-y-1">
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="font-medium text-slate-500 flex items-center gap-1">
                      <Calendar className="w-3.5 h-3.5 text-emerald-600" /> Timings:
                    </span>
                    <span className="font-semibold text-slate-900 truncate">
                      {t.departure_time || 'Daily Scheduled Departures'} {t.arrival_time ? `→ Arr: ${t.arrival_time}` : ''}
                    </span>
                  </div>
                  {t.live_availability_status && (
                    <div className="flex items-center justify-between text-[10px] pt-1 border-t border-slate-200/60">
                      <span className="text-slate-500">Live Status:</span>
                      <span className="font-bold text-emerald-700 bg-emerald-100/60 px-1.5 py-0.5 rounded border border-emerald-300/50">
                        {t.live_availability_status}
                      </span>
                    </div>
                  )}
                </div>
              )}

              {/* Key Metrics Grid */}
              <div className="grid grid-cols-2 gap-3 py-3 border-y border-[#F1F0EB] text-xs">
                <div>
                  <span className="text-[#8C9BA5] block text-[10px] uppercase font-semibold">
                    Journey Duration
                  </span>
                  <span className="text-sm font-bold text-[#0F1E28] flex items-center gap-1 mt-0.5">
                    <Clock className="w-3.5 h-3.5 text-[#10B981]" /> {t.duration_hours} hrs
                  </span>
                </div>
                <div>
                  <span className="text-[#8C9BA5] block text-[10px] uppercase font-semibold">
                    Distance & Transfers
                  </span>
                  <span className="text-sm font-bold text-[#0F1E28] mt-0.5 block">
                    {t.distance_km} km &bull; {t.transfers === 0 ? 'Direct' : `${t.transfers} transfer`}
                  </span>
                </div>
                <div>
                  <span className="text-[#8C9BA5] block text-[10px] uppercase font-semibold">
                    Estimated Group Fare
                  </span>
                  <span className="text-base font-bold text-[#143628] mt-0.5 block">
                    {currency} {t.estimated_cost.toLocaleString()}
                  </span>
                </div>
                <div>
                  <span className="text-[#8C9BA5] block text-[10px] uppercase font-semibold">
                    Price Range
                  </span>
                  <span className="text-xs font-semibold text-[#5A6D7C] mt-0.5 block">
                    {currency} {t.price_range_low.toLocaleString()} - {currency} {t.price_range_high.toLocaleString()}
                  </span>
                </div>
              </div>

              {/* Agent Rationale */}
              <p className="text-xs text-[#475569] mt-3 leading-relaxed">
                <strong className="text-[#0F1E28]">Agent Rationale:</strong> {t.recommendation_rationale}
              </p>

              {/* Official Booking CTA button */}
              {t.booking_url && (
                <div className="mt-3">
                  <a
                    href={t.booking_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center justify-center gap-1.5 w-full py-2 px-3 rounded-xl bg-[#143628] hover:bg-[#1E4D3B] text-white text-xs font-bold transition-all shadow-sm group"
                  >
                    <span>
                      {isTrain(t.mode)
                        ? 'Book on Official IRCTC Portal'
                        : isFlight(t.mode)
                        ? 'Book on Official Airline Portal'
                        : 'Official Booking Platform'}
                    </span>
                    <ExternalLink className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
                  </a>
                </div>
              )}
            </div>

            {/* Provider and Advisory Notes */}
            <div className="mt-4 pt-3 border-t border-[#F1F0EB] space-y-1.5">
              <div className="flex items-center justify-between text-[10px] text-[#8C9BA5]">
                <span><strong>Data Provider:</strong> {t.provider || t.source}</span>
                <span>{t.data_timestamp}</span>
              </div>
              <div className="text-[11px] text-[#64748b] bg-black/5 rounded-lg p-2.5 flex items-start gap-1.5">
                <AlertCircle className="w-3.5 h-3.5 text-amber-600 shrink-0 mt-0.5" />
                <span>{t.booking_advisory}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

