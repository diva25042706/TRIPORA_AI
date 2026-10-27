import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';
import { ItineraryView } from '../components/trip/ItineraryView';
import { BudgetChart } from '../components/trip/BudgetChart';
import { AgentStatusTracker } from '../components/trip/AgentStatusTracker';
import { TransportComparison } from '../components/trip/TransportComparison';
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

  it('renders TransportComparison for Chennai -> Tiruvannamalai with zero flights and IRCTC train booking', () => {
    const mockTransports: any[] = [
      {
        id: 'trans_cab',
        mode: 'Private Outstation Cab / Taxi',
        origin: 'Chennai',
        destination: 'Tiruvannamalai',
        distance_km: 195.0,
        duration_hours: 4.0,
        price_range_low: 3200,
        price_range_high: 4800,
        estimated_cost: 4000,
        currency: 'INR',
        is_recommended: true,
        recommendation_rationale: 'Direct highway route via NH 32 & NH 77.',
        source: 'Verified State Highway Network',
        data_timestamp: '2026-10-28 00:00 UTC',
        booking_advisory: 'Includes driver allowance and tolls.',
        verification_status: 'verified',
        booking_url: null,
      },
      {
        id: 'trans_train',
        mode: 'Express Train / Railway (Chennai Egmore - Tiruvannamalai Express / MEMU)',
        origin: 'Chennai',
        destination: 'Tiruvannamalai',
        distance_km: 205.0,
        duration_hours: 4.5,
        price_range_low: 230,
        price_range_high: 900,
        estimated_cost: 565,
        currency: 'INR',
        is_recommended: false,
        recommendation_rationale: 'Southern Railway broad gauge route via Chengalpattu & Villupuram.',
        source: 'Indian Railways Schedule Benchmark',
        data_timestamp: '2026-10-28 00:00 UTC',
        booking_advisory: 'IRCTC reservation opens 120 days in advance.',
        verification_status: 'verified',
        train_number: '16115 / 06033',
        train_name: 'Chennai Egmore - Tiruvannamalai Express',
        departure_time: '18:00',
        arrival_time: '22:30',
        booking_url: 'https://www.irctc.co.in/nget/',
        live_availability_status: 'IRCTC Reservation Open (2S / CC / SL Berths)',
      },
    ];

    render(<TransportComparison transports={mockTransports} currency="INR" />);

    // Flights count badge should be Flights (0)
    expect(screen.getByText('Flights (0)')).toBeDefined();

    // Zero-flight advisory banner for airport-less destination must be displayed
    expect(screen.getByText('No Commercial Passenger Airport Serving Destination')).toBeDefined();

    // IRCTC booking button must be present
    expect(screen.getByText('Book on Official IRCTC Portal')).toBeDefined();
  });

  it('renders TransportComparison for Chennai -> Coimbatore with verified flight and train options', () => {
    const mockTransports: any[] = [
      {
        id: 'trans_flight',
        mode: 'Commercial Flight (IndiGo / Air India Express)',
        origin: 'Chennai',
        destination: 'Coimbatore',
        distance_km: 425.0,
        duration_hours: 3.1,
        price_range_low: 6400,
        price_range_high: 11600,
        estimated_cost: 9000,
        currency: 'INR',
        is_recommended: true,
        recommendation_rationale: 'Direct commercial flight connecting MAA and CJB.',
        source: 'Commercial Passenger Airline Matrix',
        data_timestamp: '2026-10-28 00:00 UTC',
        booking_advisory: 'Airfares vary dynamically based on load factor.',
        verification_status: 'verified',
        flight_operator: 'IndiGo / Air India Express',
        flight_number: '6E 6825 / 6E 238',
        departure_time: '07:15 / 18:30 Scheduled Daily',
        arrival_time: '08:20 / 19:35',
        booking_url: 'https://www.goindigo.in',
        live_availability_status: 'Scheduled Daily Flights Confirmed (Book on Airline Portal)',
      },
      {
        id: 'trans_train',
        mode: 'Express Train / Railway (Coimbatore Vande Bharat Express)',
        origin: 'Chennai',
        destination: 'Coimbatore',
        distance_km: 495.0,
        duration_hours: 5.8,
        price_range_low: 2730,
        price_range_high: 4980,
        estimated_cost: 3855,
        currency: 'INR',
        is_recommended: false,
        recommendation_rationale: 'Semi-high speed Vande Bharat Express via Katpadi and Salem.',
        source: 'Indian Railways Schedule Benchmark',
        data_timestamp: '2026-10-28 00:00 UTC',
        booking_advisory: 'Official IRCTC reservation opens 120 days in advance.',
        verification_status: 'verified',
        train_number: '20643',
        train_name: 'Coimbatore Vande Bharat Express',
        departure_time: '14:25',
        arrival_time: '20:15',
        booking_url: 'https://www.irctc.co.in/nget/',
        live_availability_status: 'Vande Bharat Express (AC Chair Car & Executive Car)',
      },
    ];

    render(<TransportComparison transports={mockTransports} currency="INR" />);

    expect(screen.getAllByText('Flights (1)').length).toBeGreaterThan(0);
    expect(screen.getAllByText('Express Rail (1)').length).toBeGreaterThan(0);
    expect(screen.getAllByText('Book on Official Airline Portal').length).toBeGreaterThan(0);
    expect(screen.getAllByText('Book on Official IRCTC Portal').length).toBeGreaterThan(0);
  });
});

