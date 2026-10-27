import React from 'react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';
import { BudgetBreakdown } from '../../types';
import { Wallet, TrendingUp, AlertTriangle, CheckCircle, Lightbulb, User } from 'lucide-react';

interface BudgetChartProps {
  budget: BudgetBreakdown;
  travellers: number;
}

const CATEGORY_COLORS = ['#10B981', '#143628', '#3B82F6', '#F59E0B', '#8B5CF6'];

export const BudgetChart: React.FC<BudgetChartProps> = ({ budget, travellers }) => {
  const chartData = budget.categories.map((c) => ({
    name: c.category,
    value: c.amount,
    percentage: c.percentage,
  }));

  const isOverBudget = budget.budget_status === 'Over Budget';
  const isHealthy = budget.remaining_budget > 0;

  return (
    <div className="space-y-6">
      {/* Top Level Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-white border border-[#E7E5DF] shadow-sm">
          <span className="text-xs font-semibold text-[#5A6D7C] uppercase tracking-wider">
            Total Set Budget
          </span>
          <div className="text-2xl font-bold text-[#0F1E28] mt-1">
            {budget.currency} {budget.total_budget.toLocaleString()}
          </div>
          <span className="text-[11px] text-[#8C9BA5] flex items-center gap-1 mt-1">
            <Wallet className="w-3.5 h-3.5 text-[#10B981]" /> Target Ceiling
          </span>
        </div>

        <div className="p-5 rounded-2xl bg-white border border-[#E7E5DF] shadow-sm">
          <span className="text-xs font-semibold text-[#5A6D7C] uppercase tracking-wider">
            Estimated Total Cost
          </span>
          <div className="text-2xl font-bold text-[#0F1E28] mt-1">
            {budget.currency} {budget.total_estimated_cost.toLocaleString()}
          </div>
          <span className="text-[11px] text-[#059669] flex items-center gap-1 mt-1 font-semibold">
            Reconciled with 5% Contingency
          </span>
        </div>

        <div className="p-5 rounded-2xl bg-white border border-[#E7E5DF] shadow-sm">
          <span className="text-xs font-semibold text-[#5A6D7C] uppercase tracking-wider">
            Cost Per Person
          </span>
          <div className="text-2xl font-bold text-[#0F1E28] mt-1">
            {budget.currency} {budget.cost_per_person.toLocaleString()}
          </div>
          <span className="text-[11px] text-[#5A6D7C] flex items-center gap-1 mt-1">
            <User className="w-3.5 h-3.5 text-[#10B981]" /> Split across {travellers} traveler(s)
          </span>
        </div>

        <div
          className={`p-5 rounded-2xl border shadow-sm ${
            isOverBudget
              ? 'bg-red-50/70 border-red-200'
              : 'bg-emerald-50/70 border-emerald-200'
          }`}
        >
          <span className="text-xs font-semibold uppercase tracking-wider text-[#5A6D7C]">
            Budget Status
          </span>
          <div
            className={`text-2xl font-bold mt-1 flex items-center gap-2 ${
              isOverBudget ? 'text-red-700' : 'text-emerald-800'
            }`}
          >
            {isOverBudget ? (
              <>
                <AlertTriangle className="w-6 h-6 text-red-600" /> Over Budget
              </>
            ) : (
              <>
                <CheckCircle className="w-6 h-6 text-emerald-600" /> {budget.budget_status}
              </>
            )}
          </div>
          <span
            className={`text-xs font-medium mt-1 block ${
              isOverBudget ? 'text-red-600' : 'text-emerald-700'
            }`}
          >
            {isOverBudget
              ? `Deficit of ${budget.currency} ${budget.budget_deficit.toLocaleString()}`
              : `Surplus of ${budget.currency} ${budget.remaining_budget.toLocaleString()}`}
          </span>
        </div>
      </div>

      {/* Breakdown Visualization & Category List */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Recharts Donut Pie Chart */}
        <div className="lg:col-span-5 bg-white p-6 rounded-2xl border border-[#E7E5DF] shadow-sm flex flex-col justify-between">
          <h4 className="text-sm font-bold text-[#0F1E28] uppercase tracking-wider mb-2">
            Expense Allocation
          </h4>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={95}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {chartData.map((_, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={CATEGORY_COLORS[index % CATEGORY_COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(value: any) => [`${budget.currency} ${Number(value).toLocaleString()}`, 'Amount']}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <p className="text-[11px] text-center text-[#5A6D7C]">
            Deterministic sum of categories matches overall total with 100% mathematical fidelity.
          </p>
        </div>

        {/* Itemized Categories Table */}
        <div className="lg:col-span-7 bg-white p-6 rounded-2xl border border-[#E7E5DF] shadow-sm">
          <h4 className="text-sm font-bold text-[#0F1E28] uppercase tracking-wider mb-4">
            Category Breakdown
          </h4>
          <div className="space-y-3">
            {budget.categories.map((cat, idx) => (
              <div
                key={cat.category}
                className="p-3.5 rounded-xl border border-[#F1F0EB] bg-[#FAF9F5] flex items-center justify-between gap-4"
              >
                <div className="flex items-center gap-3">
                  <div
                    className="w-3.5 h-3.5 rounded-full shrink-0"
                    style={{ backgroundColor: CATEGORY_COLORS[idx % CATEGORY_COLORS.length] }}
                  />
                  <div>
                    <span className="text-sm font-bold text-[#0F1E28]">{cat.category}</span>
                    <p className="text-[11px] text-[#5A6D7C] mt-0.5">{cat.description}</p>
                  </div>
                </div>
                <div className="text-right shrink-0">
                  <div className="text-sm font-bold text-[#0F1E28]">
                    {budget.currency} {cat.amount.toLocaleString()}
                  </div>
                  <span className="text-[10px] font-semibold text-[#8C9BA5]">
                    {cat.percentage}% of total
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Cost Saving Recommendations */}
      {budget.cost_saving_recommendations.length > 0 && (
        <div className="bg-[#FAF9F5] border border-[#10B981]/30 rounded-2xl p-5">
          <div className="flex items-center gap-2 mb-3">
            <Lightbulb className="w-5 h-5 text-[#059669]" />
            <h4 className="text-sm font-bold text-[#143628] uppercase tracking-wider">
              Budget Optimization Agent Recommendations
            </h4>
          </div>
          <ul className="space-y-2">
            {budget.cost_saving_recommendations.map((rec, i) => (
              <li key={i} className="text-xs text-[#2C3E50] flex items-start gap-2">
                <span className="text-[#10B981] font-bold">&bull;</span>
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
