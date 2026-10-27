import React from 'react';
import { WeatherForecast, SafetyFinding } from '../../types';
import { CloudSun, CloudRain, Sun, ShieldAlert, AlertTriangle, Info, CheckCircle2, Umbrella } from 'lucide-react';

interface WeatherSafetyPanelProps {
  weatherForecasts: WeatherForecast[];
  safetyFindings: SafetyFinding[];
}

export const WeatherSafetyPanel: React.FC<WeatherSafetyPanelProps> = ({
  weatherForecasts,
  safetyFindings,
}) => {
  const getSeverityBadge = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'high':
        return (
          <span className="px-2 py-0.5 rounded-md bg-red-100 text-red-800 text-[10px] font-bold uppercase flex items-center gap-1">
            <AlertTriangle className="w-3 h-3 text-red-600" /> High Alert
          </span>
        );
      case 'medium':
        return (
          <span className="px-2 py-0.5 rounded-md bg-amber-100 text-amber-800 text-[10px] font-bold uppercase flex items-center gap-1">
            <AlertTriangle className="w-3 h-3 text-amber-600" /> Advisory
          </span>
        );
      case 'low':
        return (
          <span className="px-2 py-0.5 rounded-md bg-yellow-50 text-yellow-800 text-[10px] font-bold uppercase flex items-center gap-1">
            <Info className="w-3 h-3 text-yellow-600" /> Notice
          </span>
        );
      default:
        return (
          <span className="px-2 py-0.5 rounded-md bg-blue-50 text-blue-800 text-[10px] font-bold uppercase flex items-center gap-1">
            <Info className="w-3 h-3 text-blue-600" /> Verified Info
          </span>
        );
    }
  };

  return (
    <div className="space-y-8">
      {/* Weather Forecast Section */}
      <div className="bg-white p-6 rounded-2xl border border-[#E7E5DF] shadow-sm">
        <div className="flex items-center gap-2 mb-4">
          <CloudSun className="w-5 h-5 text-[#10B981]" />
          <h3 className="text-base font-bold text-[#0F1E28]">
            Meteorological Forecast & Outdoor Viability
          </h3>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {weatherForecasts.map((w) => (
            <div
              key={w.day_number}
              className={`p-4 rounded-xl border transition-all ${
                w.is_rainy
                  ? 'bg-blue-50/60 border-blue-200'
                  : 'bg-[#FAF9F5] border-[#E7E5DF]'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold text-[#143628]">
                  Day {w.day_number} &bull; {w.date}
                </span>
                {w.is_rainy ? (
                  <span className="text-[10px] font-bold text-blue-700 bg-blue-100 px-2 py-0.5 rounded flex items-center gap-1">
                    <CloudRain className="w-3 h-3" /> {w.precipitation_chance}% Rain
                  </span>
                ) : (
                  <span className="text-[10px] font-bold text-amber-700 bg-amber-100 px-2 py-0.5 rounded flex items-center gap-1">
                    <Sun className="w-3 h-3" /> Favorable
                  </span>
                )}
              </div>

              <div className="text-lg font-bold text-[#0F1E28] mt-1 flex items-baseline gap-2">
                <span>{w.condition}</span>
                <span className="text-xs text-[#5A6D7C] font-normal">
                  {w.temp_high_c}° / {w.temp_low_c}°C
                </span>
              </div>

              <p className="text-[11px] text-[#475569] mt-2 leading-relaxed">
                {w.risk_assessment}
              </p>

              {w.is_rainy && w.suggested_alternatives.length > 0 && (
                <div className="mt-3 pt-2 border-t border-blue-200/60 text-[11px] text-blue-900">
                  <span className="font-bold flex items-center gap-1 mb-1">
                    <Umbrella className="w-3 h-3 text-blue-700" /> Recommended Indoor Backup:
                  </span>
                  <ul className="list-disc list-inside text-[10px] space-y-0.5 text-blue-800">
                    {w.suggested_alternatives.map((alt, idx) => (
                      <li key={idx}>{alt}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Safety & Reliability Findings */}
      <div className="bg-white p-6 rounded-2xl border border-[#E7E5DF] shadow-sm">
        <div className="flex items-center gap-2 mb-4">
          <ShieldAlert className="w-5 h-5 text-[#10B981]" />
          <h3 className="text-base font-bold text-[#0F1E28]">
            Safety, Schedule Feasibility & Travel Advisories
          </h3>
        </div>

        <div className="space-y-3">
          {safetyFindings.map((f) => (
            <div
              key={f.id}
              className="p-4 rounded-xl border border-[#F1F0EB] bg-[#FAF9F5] hover:border-[#E2E0D8] transition-colors"
            >
              <div className="flex flex-wrap items-center justify-between gap-2 mb-1.5">
                <div className="flex items-center gap-2">
                  <h4 className="text-sm font-bold text-[#0F1E28]">{f.title}</h4>
                  <span className="text-[10px] font-semibold text-[#5A6D7C] bg-black/5 px-2 py-0.5 rounded">
                    {f.category}
                  </span>
                </div>
                {getSeverityBadge(f.severity)}
              </div>

              <p className="text-xs text-[#475569] leading-relaxed mb-2">
                {f.description}
              </p>

              <div className="text-[11px] text-[#059669] bg-[#10B981]/10 rounded-lg p-2.5 flex items-start gap-1.5">
                <CheckCircle2 className="w-3.5 h-3.5 shrink-0 mt-0.5" />
                <span>
                  <strong>Recommended Action:</strong> {f.recommended_action}
                </span>
              </div>

              <div className="mt-2 text-[10px] text-[#8C9BA5] flex items-center justify-between">
                <span>Source: {f.supporting_source}</span>
                <span>{f.confidence_notes}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
