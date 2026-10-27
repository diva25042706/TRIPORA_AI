import React from 'react';
import { AgentExecutionStatus } from '../../types';
import { Cpu, CheckCircle2, XCircle, Clock, Sparkles } from 'lucide-react';

interface AgentStatusTrackerProps {
  statuses: AgentExecutionStatus[];
}

export const AgentStatusTracker: React.FC<AgentStatusTrackerProps> = ({ statuses }) => {
  const getStatusBadge = (status: string) => {
    switch (status.toLowerCase()) {
      case 'completed':
        return (
          <span className="px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[10px] font-bold flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3 text-emerald-600" /> Completed
          </span>
        );
      case 'failed':
        return (
          <span className="px-2 py-0.5 rounded-full bg-red-100 text-red-800 text-[10px] font-bold flex items-center gap-1">
            <XCircle className="w-3 h-3 text-red-600" /> Failed (Recovered)
          </span>
        );
      case 'running':
        return (
          <span className="px-2 py-0.5 rounded-full bg-blue-100 text-blue-800 text-[10px] font-bold flex items-center gap-1">
            <Clock className="w-3 h-3 text-blue-600 animate-spin" /> In Progress
          </span>
        );
      default:
        return (
          <span className="px-2 py-0.5 rounded-full bg-gray-100 text-gray-800 text-[10px] font-bold">
            {status}
          </span>
        );
    }
  };

  return (
    <div className="bg-white p-6 rounded-2xl border border-[#E7E5DF] shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Cpu className="w-5 h-5 text-[#10B981]" />
          <h3 className="text-base font-bold text-[#0F1E28]">
            LangGraph Multi-Agent Execution Telemetry
          </h3>
        </div>
        <span className="text-xs font-semibold text-[#059669] bg-[#10B981]/15 px-2.5 py-1 rounded-lg">
          StateGraph Orchestrated
        </span>
      </div>

      <p className="text-xs text-[#5A6D7C] mb-6 leading-relaxed">
        TRIPORA.AI executes six specialized agents over a shared state graph. Each agent operates with bounded responsibilities, strict Pydantic schema validation, and deterministic fallbacks.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        {statuses.map((agent, i) => (
          <div
            key={i}
            className="p-3.5 rounded-xl border border-[#F1F0EB] bg-[#FAF9F5] flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between gap-2 mb-2">
                <span className="text-xs font-bold text-[#0F1E28] truncate">
                  {agent.agent_name}
                </span>
                {getStatusBadge(agent.status)}
              </div>
              <p className="text-[11px] text-[#475569] leading-relaxed">
                {agent.summary}
              </p>
            </div>

            <div className="mt-3 pt-2 border-t border-[#E7E5DF]/60 flex items-center justify-between text-[10px] text-[#8C9BA5]">
              <span>Duration: {agent.duration_ms} ms</span>
              {agent.error_message && (
                <span className="text-red-500 font-semibold truncate max-w-[120px]">
                  {agent.error_message}
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
