import React from 'react';
import { TransportOption } from '../../types';
import { Plane, Train, Bus, Car, CheckCircle2, Clock, MapPin, AlertCircle, Info } from 'lucide-react';

interface TransportComparisonProps {
  transports: TransportOption[];
  currency: string;
}

export const TransportComparison: React.FC<TransportComparisonProps> = ({ transports, currency }) => {
  const getModeIcon = (mode: string) => {
    const m = mode.toLowerCase();
    if (m.includes('flight') || m.includes('air')) return <Plane className="w-5 h-5 text-blue-600" />;
    if (m.includes('train') || m.includes('rail')) return <Train className="w-5 h-5 text-emerald-600" />;
    if (m.includes('bus') || m.includes('coach')) return <Bus className="w-5 h-5 text-amber-600" />;
    return <Car className="w-5 h-5 text-purple-600" />;
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#FAF9F5] p-4 rounded-xl border border-[#E7E5DF] flex items-start gap-3">
        <Info className="w-5 h-5 text-[#059669] shrink-0 mt-0.5" />
        <p className="text-xs text-[#5A6D7C] leading-relaxed">
          <strong className="text-[#0F1E28]">Multi-Modal Transit Evaluation:</strong> Our Transportation Agent compares travel options balancing transit time, road/rail distance, and total group cost. Prices are benchmarked against regional carrier averages and labeled honestly.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {transports.map((t) => (
          <div
            key={t.id}
            className={`p-5 rounded-2xl border transition-all ${
              t.is_recommended
                ? 'bg-white border-[#10B981] shadow-md ring-1 ring-[#10B981]/30'
                : 'bg-white border-[#E7E5DF] shadow-sm hover:border-[#CBD5E1]'
            }`}
          >
            <div className="flex items-start justify-between gap-3 mb-3">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-black/5 flex items-center justify-center">
                  {getModeIcon(t.mode)}
                </div>
                <div>
                  <h4 className="text-base font-bold text-[#0F1E28]">{t.mode}</h4>
                  <span className="text-xs text-[#5A6D7C] flex items-center gap-1">
                    <MapPin className="w-3 h-3 text-[#10B981]" /> {t.origin} &rarr; {t.destination}
                  </span>
                </div>
              </div>
              {t.is_recommended && (
                <span className="px-2.5 py-1 rounded-full bg-[#10B981]/15 text-[#059669] text-[11px] font-bold flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5" /> Recommended
                </span>
              )}
            </div>

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
                  Distance
                </span>
                <span className="text-sm font-bold text-[#0F1E28] mt-0.5 block">
                  {t.distance_km} km
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

            <p className="text-xs text-[#475569] mt-3 leading-relaxed">
              <strong className="text-[#0F1E28]">Agent Rationale:</strong> {t.recommendation_rationale}
            </p>

            <div className="mt-3 text-[11px] text-[#64748b] bg-black/5 rounded-lg p-2 flex items-start gap-1.5">
              <AlertCircle className="w-3.5 h-3.5 text-amber-600 shrink-0 mt-0.5" />
              <span>{t.booking_advisory}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
