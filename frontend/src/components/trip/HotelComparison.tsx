import React from 'react';
import { HotelOption } from '../../types';
import { Hotel, Star, MapPin, Check, ExternalLink, Sparkles } from 'lucide-react';

interface HotelComparisonProps {
  hotels: HotelOption[];
  currency: string;
  durationDays: number;
}

export const HotelComparison: React.FC<HotelComparisonProps> = ({ hotels, currency, durationDays }) => {
  const nights = Math.max(1, durationDays - 1);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {hotels.map((h, idx) => (
          <div
            key={h.id}
            className={`p-5 rounded-2xl border transition-all ${
              idx === 0
                ? 'bg-white border-[#10B981] shadow-md ring-1 ring-[#10B981]/30'
                : 'bg-white border-[#E7E5DF] shadow-sm hover:border-[#CBD5E1]'
            }`}
          >
            <div className="flex items-start justify-between gap-3 mb-2">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-[#059669] bg-[#10B981]/10 px-2 py-0.5 rounded-md">
                  {idx === 0 ? 'Top Agent Recommendation' : 'Alternative Selection'}
                </span>
                <h4 className="text-base font-bold text-[#0F1E28] mt-1.5 flex items-center gap-2">
                  <Hotel className="w-4 h-4 text-[#10B981]" /> {h.name}
                </h4>
                <span className="text-xs text-[#5A6D7C] flex items-center gap-1 mt-0.5">
                  <MapPin className="w-3 h-3 text-[#10B981]" /> {h.location} ({h.distance_to_center_km} km to center)
                </span>
              </div>
              {h.rating && (
                <div className="flex items-center gap-1 bg-amber-50 text-amber-800 border border-amber-200 px-2 py-1 rounded-lg text-xs font-bold shrink-0">
                  <Star className="w-3.5 h-3.5 fill-amber-500 text-amber-500" /> {h.rating}
                </div>
              )}
            </div>

            <p className="text-xs text-[#475569] mt-2 leading-relaxed">
              {h.description}
            </p>

            {/* Amenities List */}
            <div className="flex flex-wrap gap-1.5 my-3">
              {h.amenities.map((am) => (
                <span
                  key={am}
                  className="text-[10px] font-medium bg-[#FAF9F5] text-[#2C3E50] border border-[#E7E5DF] px-2 py-0.5 rounded-md flex items-center gap-1"
                >
                  <Check className="w-2.5 h-2.5 text-[#10B981]" /> {am}
                </span>
              ))}
            </div>

            <div className="grid grid-cols-2 gap-3 py-3 border-t border-[#F1F0EB] text-xs">
              <div>
                <span className="text-[#8C9BA5] text-[10px] uppercase font-semibold block">
                  Nightly Rate
                </span>
                <span className="text-sm font-bold text-[#0F1E28] mt-0.5 block">
                  {currency} {h.price_per_night.toLocaleString()} / night
                </span>
              </div>
              <div>
                <span className="text-[#8C9BA5] text-[10px] uppercase font-semibold block">
                  Total for {nights} Night(s)
                </span>
                <span className="text-base font-bold text-[#143628] mt-0.5 block">
                  {currency} {h.total_price.toLocaleString()}
                </span>
              </div>
            </div>

            <div className="mt-2 text-[11px] text-[#059669] bg-[#10B981]/10 rounded-lg p-2.5 flex items-start gap-1.5 border border-[#10B981]/20">
              <Sparkles className="w-3.5 h-3.5 shrink-0 mt-0.5" />
              <span>{h.ranking_rationale}</span>
            </div>

            {h.booking_url && (
              <a
                href={h.booking_url}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-3.5 w-full py-2 px-3 rounded-xl bg-black/5 hover:bg-black/10 text-[#0F1E28] text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors"
              >
                <span>View on External Travel Portals</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
