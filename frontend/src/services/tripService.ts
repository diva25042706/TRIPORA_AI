import api from './api';
import { TripSummary, TripResponse, ReplanResponse, ChatMessage } from '../types';

export interface CreateTripPayload {
  title?: string;
  origin: string;
  destination: string;
  start_date: string;
  end_date: string;
  travellers: number;
  total_budget: number;
  currency?: string;
  travel_style?: string;
  interests?: string[];
  accommodation_pref?: string;
  transport_pref?: string;
}

export interface ReplanPayload {
  instruction: string;
  specific_day?: number;
  new_budget?: number;
  new_interests?: string[];
  new_travel_style?: string;
  new_transport_pref?: string;
  new_accommodation_pref?: string;
}

export const tripService = {
  async listTrips(): Promise<TripSummary[]> {
    const res = await api.get<TripSummary[]>('/trips/');
    return res.data;
  },

  async getTrip(tripId: string): Promise<TripResponse> {
    const res = await api.get<TripResponse>(`/trips/${tripId}`);
    return res.data;
  },

  async createTrip(payload: CreateTripPayload): Promise<TripResponse> {
    const res = await api.post<TripResponse>('/trips/', payload);
    return res.data;
  },

  async updateTrip(tripId: string, payload: Partial<CreateTripPayload>): Promise<TripResponse> {
    const res = await api.put<TripResponse>(`/trips/${tripId}`, payload);
    return res.data;
  },

  async deleteTrip(tripId: string): Promise<void> {
    await api.delete(`/trips/${tripId}`);
  },

  async replanTrip(tripId: string, payload: ReplanPayload): Promise<ReplanResponse> {
    const res = await api.post<ReplanResponse>(`/trips/${tripId}/replan`, payload);
    return res.data;
  },

  async sendChatMessage(tripId: string, message: string): Promise<ChatMessage> {
    const res = await api.post<ChatMessage>(`/chat/${tripId}/message`, { message });
    return res.data;
  },

  async getChatHistory(tripId: string): Promise<ChatMessage[]> {
    const res = await api.get<ChatMessage[]>(`/chat/${tripId}/messages`);
    return res.data;
  },
};
