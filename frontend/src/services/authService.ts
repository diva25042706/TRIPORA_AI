import api from './api';
import { AuthResponse, User } from '../types';

export const authService = {
  async register(email: string, password: string, fullName?: string, preferredCurrency = 'INR'): Promise<AuthResponse> {
    const res = await api.post<AuthResponse>('/auth/register', {
      email,
      password,
      full_name: fullName,
      preferred_currency: preferredCurrency,
    });
    return res.data;
  },

  async login(email: string, password: string): Promise<AuthResponse> {
    const res = await api.post<AuthResponse>('/auth/login', {
      email,
      password,
    });
    return res.data;
  },

  async getMe(): Promise<User> {
    const res = await api.get<User>('/auth/me');
    return res.data;
  },

  async updateProfile(fullName?: string, email?: string, preferredCurrency?: string): Promise<User> {
    const res = await api.put<User>('/auth/me', {
      full_name: fullName,
      email: email,
      preferred_currency: preferredCurrency,
    });
    return res.data;
  },
};
