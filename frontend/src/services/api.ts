import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Attach JWT access token to every request if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('tripora_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Intercept 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token invalid or expired
      localStorage.removeItem('tripora_token');
      localStorage.removeItem('tripora_user');
    }
    return Promise.reject(error);
  }
);

export default api;
