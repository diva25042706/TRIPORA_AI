import api from './api';

export interface PlaceItem {
  id: string;
  name: string;
  category: string;
  area_zone: 'chennai_city' | 'greater_chennai' | 'day_trips' | string;
  area_label: string;
  locality: string;
  city: string;
  district: string;
  address: string;
  lat: number;
  lng: number;
  desc: string;
  opening_hours: string;
  closed_days: string;
  ticket_price_inr: number;
  visit_duration_hours: number;
  is_outdoor: boolean;
  accessibility_notes?: string;
  official_website?: string;
  image_url?: string;
  source_attribution?: string;
  last_updated?: string;
  distance_km?: number;
  travel_time_min?: number;
}

export interface CategoryCount {
  category: string;
  count: number;
}

export interface AreaZoneCount {
  zone: string;
  label: string;
  count: number;
}

export interface PlaceSearchResponse {
  total: number;
  page: number;
  limit: number;
  total_pages: number;
  has_more: boolean;
  results: PlaceItem[];
  available_categories: CategoryCount[];
  available_zones: AreaZoneCount[];
}

export interface PlaceSearchParams {
  query?: string;
  category?: string;
  area_zone?: string;
  sort_by?: string;
  page?: number;
  limit?: number;
}

export const placesService = {
  searchPlaces: async (params: PlaceSearchParams = {}): Promise<PlaceSearchResponse> => {
    const response = await api.get<PlaceSearchResponse>('/places/search', { params });
    return response.data;
  },

  getCategories: async (): Promise<CategoryCount[]> => {
    const response = await api.get<CategoryCount[]>('/places/categories');
    return response.data;
  },

  getZones: async (): Promise<AreaZoneCount[]> => {
    const response = await api.get<AreaZoneCount[]>('/places/zones');
    return response.data;
  },

  getPlaceById: async (id: string): Promise<PlaceItem> => {
    const response = await api.get<PlaceItem>(`/places/${id}`);
    return response.data;
  },
};
