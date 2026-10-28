import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor, fireEvent, cleanup } from '@testing-library/react';
import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { DiscoverPlacesPage } from '../pages/DiscoverPlacesPage';
import { placesService } from '../services/placesService';

// Mock placesService
vi.mock('../services/placesService', () => ({
  placesService: {
    searchPlaces: vi.fn(),
    getCategories: vi.fn(),
    getZones: vi.fn(),
    getDistricts: vi.fn(),
    resolveDestination: vi.fn(),
    getPlaceById: vi.fn(),
  },
}));

const mockPlaces = [
  {
    id: 'chn_beach_marina',
    name: 'Marina Beach & Promenade',
    category: 'Beaches & Waterfronts',
    area_zone: 'chennai_city',
    area_label: 'Chennai City',
    locality: 'Triplicane',
    city: 'Chennai',
    district: 'Chennai',
    address: 'Kamarajar Salai, Triplicane, Chennai 600005',
    lat: 13.0500,
    lng: 80.2824,
    desc: 'World second longest urban natural sand beach.',
    opening_hours: 'Open 24 hours',
    closed_days: 'None',
    ticket_price_inr: 0,
    visit_duration_hours: 2.5,
    is_outdoor: true,
    accessibility_notes: 'Wheelchair ramp available.',
    source_attribution: 'TTDC',
    last_updated: '2026-10-28',
  },
  {
    id: 'chn_temple_kapaleeshwarar',
    name: 'Kapaleeshwarar Temple',
    category: 'Temples & Religious Sites',
    area_zone: 'chennai_city',
    area_label: 'Chennai City',
    locality: 'Mylapore',
    city: 'Chennai',
    district: 'Chennai',
    address: 'Vadakku Mada Veethi, Mylapore, Chennai 600004',
    lat: 13.0334,
    lng: 80.2699,
    desc: '7th-century Dravidian Shiva temple.',
    opening_hours: '05:30 AM - 12:00 PM',
    closed_days: 'None',
    ticket_price_inr: 0,
    visit_duration_hours: 1.5,
    is_outdoor: false,
    source_attribution: 'HR&CE / TTDC',
    last_updated: '2026-10-28',
  },
  {
    id: 'chn_museum_government',
    name: 'Government Museum Egmore',
    category: 'Museums, Art & Libraries',
    area_zone: 'chennai_city',
    area_label: 'Chennai City',
    locality: 'Egmore',
    city: 'Chennai',
    district: 'Chennai',
    address: 'Pantheon Road, Egmore, Chennai 600008',
    lat: 13.0788,
    lng: 80.2585,
    desc: 'Second oldest museum in India housing Chola bronzes.',
    opening_hours: '09:30 AM - 05:00 PM',
    closed_days: 'Fridays',
    ticket_price_inr: 100,
    visit_duration_hours: 2.5,
    is_outdoor: false,
    source_attribution: 'Department of Museums',
    last_updated: '2026-10-28',
  },
  {
    id: 'chn_daytrip_mahabalipuram',
    name: 'Group of Monuments at Mahabalipuram',
    category: 'Nearby Day Trips (Outside Chennai)',
    area_zone: 'day_trips',
    area_label: 'Nearby Day Trips',
    locality: 'Mahabalipuram',
    city: 'Mahabalipuram',
    district: 'Chengalpattu',
    address: 'East Coast Road, Mahabalipuram 603104',
    lat: 12.6269,
    lng: 80.1927,
    desc: '7th-century UNESCO World Heritage monolithic rock-cut sanctuaries.',
    opening_hours: '06:00 AM - 06:00 PM',
    closed_days: 'None',
    ticket_price_inr: 40,
    visit_duration_hours: 4.5,
    is_outdoor: true,
    source_attribution: 'Archaeological Survey of India (ASI)',
    last_updated: '2026-10-28',
  },
];

describe('DiscoverPlacesPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    (placesService.getDistricts as any).mockResolvedValue([
      { district: 'Chennai', district_key: 'chennai', city: 'Chennai', lat: 13.08, lng: 80.27, attraction_count: 54, popular_attractions: ['Marina Beach'] },
      { district: 'Madurai', district_key: 'madurai', city: 'Madurai', lat: 9.92, lng: 78.12, attraction_count: 6, popular_attractions: ['Meenakshi Amman Temple'] }
    ]);
    (placesService.searchPlaces as any).mockResolvedValue({
      total: 54,
      page: 1,
      limit: 12,
      total_pages: 5,
      has_more: true,
      results: mockPlaces,
      available_categories: [
        { category: 'Beaches & Waterfronts', count: 5 },
        { category: 'Temples & Religious Sites', count: 6 },
        { category: 'Museums, Art & Libraries', count: 6 },
        { category: 'Nearby Day Trips (Outside Chennai)', count: 5 },
      ],
      available_zones: [
        { zone: 'chennai_city', label: 'Chennai City', count: 40 },
        { zone: 'greater_chennai', label: 'Greater Chennai Suburbs', count: 9 },
        { zone: 'day_trips', label: 'Nearby Day Trips (Outside Chennai)', count: 5 },
      ],
    });
  });

  afterEach(() => {
    cleanup();
  });

  it('renders the Discover page with header and verified badges', async () => {
    render(
      <BrowserRouter>
        <DiscoverPlacesPage />
      </BrowserRouter>
    );

    expect(screen.getByText(/Discover All 38 Districts of Tamil Nadu/i)).toBeDefined();
    expect(screen.getAllByPlaceholderText(/Search places/i).length).toBeGreaterThan(0);

    await waitFor(() => {
      expect(screen.getByText('Marina Beach & Promenade')).toBeDefined();
      expect(screen.getByText('Kapaleeshwarar Temple')).toBeDefined();
      expect(screen.getByText('Government Museum Egmore')).toBeDefined();
      expect(screen.getByText('Group of Monuments at Mahabalipuram')).toBeDefined();
    });

    // Verifies more than 3 places are rendered seamlessly without arbitrary limits
    expect(screen.getAllByText(/Plan Trip/i).length).toBe(4);
  });

  it('opens details modal when Details & Map is clicked', async () => {
    render(
      <BrowserRouter>
        <DiscoverPlacesPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Marina Beach & Promenade')).toBeDefined();
    });

    const detailsButtons = screen.getAllByText(/Details & Map/i);
    fireEvent.click(detailsButtons[0]);

    await waitFor(() => {
      expect(screen.getByText(/Full Address & Coordinates/i)).toBeDefined();
      expect(screen.getByText(/Kamarajar Salai, Triplicane, Chennai 600005/i)).toBeDefined();
      expect(screen.getByText(/Open in Google Maps/i)).toBeDefined();
    });
  });

  it('triggers search when input query is typed', async () => {
    render(
      <BrowserRouter>
        <DiscoverPlacesPage />
      </BrowserRouter>
    );

    const searchInputs = screen.getAllByPlaceholderText(/Search places/i);
    fireEvent.change(searchInputs[0], { target: { value: 'Mylapore' } });

    await waitFor(() => {
      expect(placesService.searchPlaces).toHaveBeenCalledWith(
        expect.objectContaining({ query: 'Mylapore' })
      );
    });
  });
});
