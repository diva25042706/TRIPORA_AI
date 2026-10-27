import React, { useState } from 'react';
import { DayPlan, ItineraryItem } from '../../types';
import { Clock, IndianRupee, Sun, CloudRain, MapPin, Sparkles, ShieldCheck } from 'lucide-react';

interface ItineraryViewProps {
  days: DayPlan[];
  currency: string;
  onDaySelect?: (dayNumber: number | null) => void;
  selectedDay?: number | null;
}

export const ItineraryView: React.FC<ItineraryViewProps> = ({
  days,
  currency,
  onDaySelect,
  selectedDay = null,
}) => {
  const [activeTab, setActiveTab] = useState<number | null>(selectedDay);

  const handleTabChange = (dayNum: number | null) => {
    setActiveTab(dayNum);
    if (onDaySelect) {
      onDaySelect(dayNum);
    }
  };

  const displayedDays = activeTab ? days.filter((d) => d.day_number === activeTab) : days;

  return (
    <div className="space-y-6">
      {/* Day Selector Navigation */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
        <button
          onClick={() => handleTabChange(null)}
          className={`px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
            activeTab === null
              ? 'bg-[#143628] text-white shadow-sm'
              : 'bg-white hover:bg-[#F4F3EE] text-[#5A6D7C] border border-[#E7E5DF]'
          }`}
        >
          All Days ({days.length})
        </button>
        {days.map((d) => (
          <button
            key={d.day_number}
            onClick={() => handleTabChange(d.day_number)}
            className={`px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all flex items-center gap-2 ${
              activeTab === d.day_number
                ? 'bg-[#143628] text-white shadow-sm'
                : 'bg-white hover:bg-[#F4F3EE] text-[#5A6D7C] border border-[#E7E5DF]'
            }`}
          >
            <span>Day {d.day_number}</span>
            <span className="text-[10px] opacity-70">({d.activities.length} stops)</span>
          </button>
        ))}
      </div>

      {/* Days List */}
      <div className="space-y-8">
        {displayedDays.map((day) => (
          <div
            key={day.day_number}
            className="bg-white rounded-2xl border border-[#E7E5DF] shadow-sm overflow-hidden"
          >
            {/* Day Header */}
            <div className="bg-[#FAF9F5] border-b border-[#E7E5DF] px-6 py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 rounded-full bg-[#143628] text-white text-xs font-bold">
                    Day {day.day_number}
                  </span>
                  <span className="text-xs text-[#5A6D7C] font-medium">{day.date}</span>
                </div>
                <h3 className="font-editorial text-lg font-bold text-[#0F1E28] mt-1">
                  {day.theme}
                </h3>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs font-semibold text-[#143628] bg-[#10B981]/15 px-3 py-1 rounded-lg">
                  Est. Day Cost: {currency} {day.day_cost.toLocaleString()}
                </span>
              </div>
            </div>

            {/* Activities Timeline */}
            <div className="p-6 space-y-6">
              {day.activities.map((act, index) => (
                <div
                  key={act.id}
                  className="relative pl-8 before:absolute before:left-3 before:top-3 before:bottom-0 before:w-px before:bg-[#E2E8F0] last:before:hidden"
                >
                  {/* Timeline bullet */}
                  <div className="absolute left-1.5 top-2 w-3.5 h-3.5 rounded-full bg-[#10B981] border-2 border-white shadow-sm" />

                  <div className="p-4 rounded-xl border border-[#F1F0EB] bg-[#FCFBF8] hover:border-[#10B981]/40 transition-colors">
                    <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-2">
                      <div>
                        <div className="flex flex-wrap items-center gap-2 mb-1.5">
                          <span className="text-xs font-bold text-[#059669] flex items-center gap-1">
                            <Clock className="w-3.5 h-3.5" /> {act.suggested_start_time}
                          </span>
                          <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-black/5 text-[#2C3E50]">
                            {act.category}
                          </span>
                          {act.is_outdoor ? (
                            <span className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-amber-50 text-amber-700 border border-amber-200/50 flex items-center gap-1">
                              <Sun className="w-3 h-3" /> Outdoor
                            </span>
                          ) : (
                            <span className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-blue-50 text-blue-700 border border-blue-200/50 flex items-center gap-1">
                              <CloudRain className="w-3 h-3" /> Sheltered / Indoor
                            </span>
                          )}
                        </div>
                        <h4 className="text-base font-bold text-[#0F1E28]">
                          {act.activity_name}
                        </h4>
                        <p className="text-xs text-[#5A6D7C] flex items-center gap-1 mt-0.5">
                          <MapPin className="w-3 h-3 text-[#10B981]" /> {act.location}
                        </p>
                      </div>

                      <div className="text-right sm:self-start">
                        <div className="text-sm font-bold text-[#0F1E28]">
                          {act.estimated_cost === 0 ? (
                            <span className="text-[#059669]">Free Entry</span>
                          ) : (
                            `${currency} ${act.estimated_cost.toLocaleString()}`
                          )}
                        </div>
                        <span className="text-[11px] text-[#8C9BA5]">
                          Approx. {act.estimated_duration_hours} hrs
                        </span>
                      </div>
                    </div>

                    <p className="text-xs text-[#475569] mt-3 leading-relaxed">
                      {act.description}
                    </p>

                    {act.relevant_notes && (
                      <div className="mt-3 text-[11px] text-[#059669] bg-[#10B981]/10 rounded-lg p-2.5 flex items-start gap-2 border border-[#10B981]/20">
                        <Sparkles className="w-3.5 h-3.5 shrink-0 mt-0.5" />
                        <span>{act.relevant_notes}</span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
