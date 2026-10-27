import React, { useState } from 'react';
import { RefreshCw, Sparkles, Check, AlertCircle, ArrowRight, X } from 'lucide-react';
import { tripService } from '../../services/tripService';
import { ReplanResponse, FullTripPlan } from '../../types';

interface ReplanningModalProps {
  isOpen: boolean;
  onClose: () => void;
  tripId: string;
  totalDays: number;
  currentCurrency: string;
  onPlanUpdated: (updatedPlan: FullTripPlan) => void;
}

export const ReplanningModal: React.FC<ReplanningModalProps> = ({
  isOpen,
  onClose,
  tripId,
  totalDays,
  currentCurrency,
  onPlanUpdated,
}) => {
  const [instruction, setInstruction] = useState<string>('');
  const [specificDay, setSpecificDay] = useState<number | ''>('');
  const [isReplanning, setIsReplanning] = useState<boolean>(false);
  const [diffResult, setDiffResult] = useState<ReplanResponse | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  if (!isOpen) return null;

  const quickPresets = [
    { label: '🌧️ Rain Alert: Swap Outdoor Venues', text: 'Rain predicted on Day 2 - swap outdoor activities for indoor museums and cultural centers' },
    { label: '💰 Budget Cut: Reduce Overall Cost by 20%', text: 'Reduce my budget by 20% and switch to economical accommodation' },
    { label: '🧘 Relax Pace: Max 2 Activities per Day', text: 'Make the itinerary more relaxed with longer leisure intervals' },
    { label: '🏛️ Deep Culture: Add Heritage Attractions', text: 'Add more historic architecture, heritage monuments, and museums' },
  ];

  const handleExecuteReplan = async (customText?: string) => {
    const textToRun = customText || instruction;
    if (!textToRun.trim()) {
      setErrorMsg('Please enter a replanning instruction or select a preset.');
      return;
    }

    setIsReplanning(true);
    setErrorMsg(null);

    try {
      const res = await tripService.replanTrip(tripId, {
        instruction: textToRun,
        specific_day: specificDay ? Number(specificDay) : undefined,
      });
      setDiffResult(res);
    } catch (err: any) {
      console.error('Replanning error:', err);
      setErrorMsg(err.response?.data?.detail || 'Failed to execute replanning workflow. Please retry.');
    } finally {
      setIsReplanning(false);
    }
  };

  const handleConfirmAndApply = () => {
    if (diffResult) {
      onPlanUpdated(diffResult.updated_plan);
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
      <div className="bg-white rounded-3xl max-w-2xl w-full border border-[#E7E5DF] shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="p-6 bg-[#FAF9F5] border-b border-[#E7E5DF] flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-[#143628] flex items-center justify-center text-[#10B981]">
              <RefreshCw className="w-5 h-5 animate-spin-reverse" />
            </div>
            <div>
              <h3 className="font-editorial text-xl font-bold text-[#0F1E28]">
                Intelligent Itinerary Replanning
              </h3>
              <p className="text-xs text-[#5A6D7C]">
                Multi-agent state recomputation with constraint diff comparison
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-[#5A6D7C] hover:text-[#0F1E28] hover:bg-black/5 rounded-full transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-6">
          {!diffResult ? (
            <>
              {/* Quick Presets */}
              <div>
                <label className="text-xs font-bold text-[#143628] uppercase tracking-wider block mb-2.5">
                  Quick Optimization Presets
                </label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  {quickPresets.map((preset, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => {
                        setInstruction(preset.text);
                        handleExecuteReplan(preset.text);
                      }}
                      className="p-3 rounded-xl border border-[#E7E5DF] bg-[#FAF9F5] hover:border-[#10B981] hover:bg-[#10B981]/5 text-left transition-all text-xs font-semibold text-[#0F1E28] flex items-center justify-between"
                    >
                      <span>{preset.label}</span>
                      <ArrowRight className="w-3.5 h-3.5 text-[#10B981]" />
                    </button>
                  ))}
                </div>
              </div>

              {/* Custom Input */}
              <div>
                <label className="text-xs font-bold text-[#143628] uppercase tracking-wider block mb-2">
                  Or Describe Your Exact Changes
                </label>
                <textarea
                  value={instruction}
                  onChange={(e) => setInstruction(e.target.value)}
                  placeholder="e.g. Reduce budget by 20%, focus on historical sights, or swap Day 2 activities because of rain..."
                  rows={3}
                  className="w-full px-4 py-3 rounded-xl border border-[#CBD5E1] focus:ring-2 focus:ring-[#10B981] focus:border-transparent text-sm text-[#0F1E28] placeholder-[#94A3B8]"
                />
              </div>

              {/* Scope Options */}
              <div className="flex items-center gap-4 text-xs">
                <span className="font-semibold text-[#5A6D7C]">Replan Scope:</span>
                <select
                  value={specificDay}
                  onChange={(e) => setSpecificDay(e.target.value ? Number(e.target.value) : '')}
                  className="px-3 py-1.5 rounded-lg border border-[#CBD5E1] text-xs font-semibold text-[#0F1E28]"
                >
                  <option value="">Entire Itinerary (All Days)</option>
                  {Array.from({ length: totalDays }, (_, i) => (
                    <option key={i + 1} value={i + 1}>
                      Day {i + 1} Only
                    </option>
                  ))}
                </select>
              </div>

              {errorMsg && (
                <div className="p-3 bg-red-50 text-red-700 text-xs rounded-xl flex items-center gap-2 border border-red-200">
                  <AlertCircle className="w-4 h-4 shrink-0" />
                  <span>{errorMsg}</span>
                </div>
              )}
            </>
          ) : (
            /* Diff Comparison View */
            <div className="space-y-5 animate-fade-in">
              <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-2xl flex items-start gap-3">
                <Check className="w-5 h-5 text-emerald-700 shrink-0 mt-0.5" />
                <div>
                  <h4 className="text-sm font-bold text-emerald-900">
                    Replanning Candidate Computed
                  </h4>
                  <p className="text-xs text-emerald-800 mt-0.5">
                    Review the changes below before saving to your live itinerary. Your original trip will not be overwritten until you confirm.
                  </p>
                </div>
              </div>

              {/* Financial Variance Diff */}
              <div className="grid grid-cols-3 gap-3 p-4 bg-[#FAF9F5] border border-[#E7E5DF] rounded-2xl text-center">
                <div>
                  <span className="text-[10px] font-semibold text-[#8C9BA5] uppercase block">
                    Previous Total
                  </span>
                  <span className="text-sm font-bold text-[#5A6D7C]">
                    {currentCurrency} {diffResult.diff_summary.previous_total.toLocaleString()}
                  </span>
                </div>
                <div>
                  <span className="text-[10px] font-semibold text-[#8C9BA5] uppercase block">
                    Revised Total
                  </span>
                  <span className="text-base font-bold text-[#143628]">
                    {currentCurrency} {diffResult.diff_summary.new_total.toLocaleString()}
                  </span>
                </div>
                <div>
                  <span className="text-[10px] font-semibold text-[#8C9BA5] uppercase block">
                    Net Difference
                  </span>
                  <span
                    className={`text-sm font-bold ${
                      diffResult.diff_summary.cost_difference <= 0
                        ? 'text-[#059669]'
                        : 'text-amber-700'
                    }`}
                  >
                    {diffResult.diff_summary.cost_difference <= 0 ? 'Saved ' : '+'}
                    {currentCurrency} {Math.abs(diffResult.diff_summary.cost_difference).toLocaleString()}
                  </span>
                </div>
              </div>

              {/* Changes Summary Checklist */}
              <div>
                <h5 className="text-xs font-bold text-[#143628] uppercase tracking-wider mb-2">
                  Summary of Orchestrated Modifications:
                </h5>
                <ul className="space-y-2">
                  {diffResult.diff_summary.changes_summary.map((change, i) => (
                    <li
                      key={i}
                      className="p-2.5 rounded-xl bg-white border border-[#E7E5DF] text-xs text-[#2C3E50] flex items-center gap-2"
                    >
                      <Sparkles className="w-3.5 h-3.5 text-[#10B981] shrink-0" />
                      <span>{change}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="p-6 bg-[#FAF9F5] border-t border-[#E7E5DF] flex items-center justify-between">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2.5 rounded-xl border border-[#CBD5E1] text-xs font-semibold text-[#5A6D7C] hover:bg-black/5"
          >
            Cancel
          </button>

          {!diffResult ? (
            <button
              type="button"
              disabled={isReplanning || !instruction.trim()}
              onClick={() => handleExecuteReplan()}
              className="px-6 py-2.5 rounded-xl bg-[#143628] hover:bg-[#1E4D3B] text-white text-xs font-bold flex items-center gap-2 disabled:opacity-50 transition-all shadow-sm"
            >
              {isReplanning ? (
                <>
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  <span>Re-running Multi-Agent Graph...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-3.5 h-3.5 text-[#10B981]" />
                  <span>Execute Replanning</span>
                </>
              )}
            </button>
          ) : (
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setDiffResult(null)}
                className="px-4 py-2.5 rounded-xl border border-[#CBD5E1] text-xs font-semibold text-[#5A6D7C]"
              >
                Back to Edit
              </button>
              <button
                type="button"
                onClick={handleConfirmAndApply}
                className="px-6 py-2.5 rounded-xl bg-[#059669] hover:bg-[#047857] text-white text-xs font-bold shadow-md flex items-center gap-2 transition-all"
              >
                <Check className="w-4 h-4" />
                <span>Save & Apply New Itinerary</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
