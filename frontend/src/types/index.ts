export interface User {
  id: number;
  email: string;
  full_name?: string;
  preferred_currency: string;
  is_active: boolean;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface ItineraryItem {
  id: string;
  day_number: number;
  activity_name: string;
  description: string;
  location: string;
  latitude?: number | null;
  longitude?: number | null;
  suggested_start_time: string;
  estimated_duration_hours: number;
  estimated_cost: number;
  category: string;
  is_outdoor: boolean;
  data_source: string;
  relevant_notes?: string | null;
}

export interface DayPlan {
  day_number: number;
  date: string;
  theme: string;
  activities: ItineraryItem[];
  day_cost: number;
  day_notes?: string | null;
}

export interface BudgetCategory {
  category: string;
  amount: number;
  percentage: number;
  description: string;
  is_estimate: boolean;
}

export interface BudgetBreakdown {
  total_budget: number;
  total_estimated_cost: number;
  remaining_budget: number;
  budget_deficit: number;
  budget_status: 'Under Budget' | 'Within Budget' | 'Over Budget' | string;
  currency: string;
  cost_per_person: number;
  categories: BudgetCategory[];
  expensive_items: string[];
  cost_saving_recommendations: string[];
  calculation_notes: string;
}

export interface TransportOption {
  id: string;
  mode: string;
  origin: string;
  destination: string;
  distance_km: number;
  duration_hours: number;
  price_range_low: number;
  price_range_high: number;
  estimated_cost: number;
  currency: string;
  is_recommended: boolean;
  recommendation_rationale: string;
  source: string;
  data_timestamp: string;
  booking_advisory: string;
}

export interface HotelOption {
  id: string;
  name: string;
  location: string;
  price_per_night: number;
  total_price: number;
  currency: string;
  rating?: number | null;
  amenities: string[];
  distance_to_center_km: number;
  description: string;
  provider_source: string;
  booking_url?: string | null;
  is_verified: boolean;
  availability_status: string;
  ranking_rationale: string;
}

export interface WeatherForecast {
  date: string;
  day_number: number;
  condition: string;
  temp_high_c: number;
  temp_low_c: number;
  precipitation_chance: number;
  is_rainy: boolean;
  is_outdoor_suitable: boolean;
  risk_assessment: string;
  suggested_alternatives: string[];
  affected_activities: string[];
  data_source: string;
  freshness: string;
}

export interface SafetyFinding {
  id: string;
  title: string;
  category: string;
  severity: 'info' | 'low' | 'medium' | 'high' | string;
  description: string;
  supporting_source: string;
  data_timestamp: string;
  recommended_action: string;
  confidence_notes: string;
}

export interface AgentExecutionStatus {
  agent_name: string;
  status: 'idle' | 'running' | 'completed' | 'failed' | 'skipped' | string;
  duration_ms: number;
  summary: string;
  error_message?: string | null;
}

export interface FullTripPlan {
  trip_id: string;
  title: string;
  origin: string;
  destination: string;
  start_date: string;
  end_date: string;
  duration_days: number;
  travellers: number;
  total_budget: number;
  currency: string;
  travel_style: string;
  itinerary_explanation: string;
  days: DayPlan[];
  budget: BudgetBreakdown;
  transports: TransportOption[];
  hotels: HotelOption[];
  weather_forecasts: WeatherForecast[];
  safety_findings: SafetyFinding[];
  agent_statuses: AgentExecutionStatus[];
  data_source_metadata: Record<string, any>;
  last_replanned_at?: string | null;
}

export interface TripSummary {
  id: string;
  title: string;
  origin: string;
  destination: string;
  start_date: string;
  end_date: string;
  duration_days: number;
  travellers: number;
  total_budget: number;
  currency: string;
  travel_style: string;
  status: string;
  created_at: string;
}

export interface TripResponse extends TripSummary {
  user_id: number;
  interests: string[];
  accommodation_pref: string;
  transport_pref: string;
  full_trip_data?: FullTripPlan;
  updated_at: string;
}

export interface ReplanDiffSummary {
  cost_difference: number;
  previous_total: number;
  new_total: number;
  currency: string;
  changes_summary: string[];
  affected_days: number[];
  notes: string;
}

export interface ReplanResponse {
  trip_id: string;
  diff_summary: ReplanDiffSummary;
  updated_plan: FullTripPlan;
}

export interface ChatMessage {
  id: number;
  role: 'user' | 'assistant' | 'system';
  content: string;
  agent_name: string;
  created_at: string;
}
