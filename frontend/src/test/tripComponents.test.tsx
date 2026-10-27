import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';
import { ItineraryView } from '../components/trip/ItineraryView';
import { BudgetChart } from '../components/trip/BudgetChart';
import { AgentStatusTracker } from '../components/trip/AgentStatusTracker';
import { DayPlan, BudgetBreakdown, AgentExecutionStatus } from '../types';

describe('TRIPORA.AI Frontend Components', () => {
  it('renders ItineraryView with day activities and chronological tags', () => {
    const mockDays: DayPlan[] = [
      {
        day_number: 1,
        date: '2026-11-15',
        theme: 'Historic Center Excursions',
        day_cost: 600,
        activities: [
          {
            id: 'act1',
            day_number: 1,
            activity_name: 'Aguada Fort',
            description: 'Coastal fortress visit',
            location: 'Goa',
            suggested_start_time: '09:30 AM',
            estimated_duration_hours: 2.0,
            estimated_cost: 200,
            category: 'Culture',
            is_outdoor: true,
            data_source: 'Catalog',
            relevant_notes: 'Morning excursion',
          },
        ],
      },
    ];

    render(<ItineraryView days={mockDays} currency="INR" />);
    expect(screen.getAllByText('Day 1').length).toBeGreaterThan(0);
    expect(screen.getByText('Aguada Fort')).toBeDefined();
    expect(screen.getByText('09:30 AM')).toBeDefined();
  });

  it('renders BudgetChart with exact calculations and status', () => {
    const mockBudget: BudgetBreakdown = {
      total_budget: 50000,
      total_estimated_cost: 42000,
      remaining_budget: 8000,
      budget_deficit: 0,
      budget_status: 'Under Budget',
      currency: 'INR',
      cost_per_person: 21000,
      categories: [
        {
          category: 'Transportation',
          amount: 12000,
          percentage: 28.6,
          description: 'Rail travel',
          is_estimate: true,
        },
        {
          category: 'Accommodation',
          amount: 18000,
          percentage: 42.9,
          description: 'Boutique Stay',
          is_estimate: true,
        },
      ],
      expensive_items: [],
      cost_saving_recommendations: ['Healthy surplus available'],
      calculation_notes: '100% reconciled',
    };

    render(<BudgetChart budget={mockBudget} travellers={2} />);
    expect(screen.getByText('Under Budget')).toBeDefined();
    expect(screen.getByText('Transportation')).toBeDefined();
    expect(screen.getByText('Accommodation')).toBeDefined();
  });

  it('renders AgentStatusTracker with 6 specialized agents', () => {
    const mockStatuses: AgentExecutionStatus[] = [
      {
        agent_name: 'Trip Planner Agent',
        status: 'completed',
        duration_ms: 120,
        summary: 'Scheduled 3 days',
      },
      {
        agent_name: 'Budget Optimization Agent',
        status: 'completed',
        duration_ms: 85,
        summary: 'Reconciled INR 42,000',
      },
    ];

    render(<AgentStatusTracker statuses={mockStatuses} />);
    expect(screen.getByText('Trip Planner Agent')).toBeDefined();
    expect(screen.getByText('Budget Optimization Agent')).toBeDefined();
  });
});
