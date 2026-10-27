import React, { createContext, useContext, useState, useEffect } from 'react';
import { User } from '../types';
import { authService } from '../services/authService';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName?: string, currency?: string) => Promise<void>;
  logout: () => void;
  loginAsDemo: () => Promise<void>;
  updateProfile: (fullName?: string, email?: string, currency?: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('tripora_token'));
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem('tripora_token');
      if (storedToken) {
        try {
          const me = await authService.getMe();
          setUser(me);
        } catch (err) {
          console.error('Session expired or invalid:', err);
          localStorage.removeItem('tripora_token');
          localStorage.removeItem('tripora_user');
          setToken(null);
          setUser(null);
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email: string, password: string) => {
    const res = await authService.login(email, password);
    localStorage.setItem('tripora_token', res.access_token);
    localStorage.setItem('tripora_user', JSON.stringify(res.user));
    setToken(res.access_token);
    setUser(res.user);
  };

  const register = async (email: string, password: string, fullName?: string, currency?: string) => {
    const res = await authService.register(email, password, fullName, currency);
    localStorage.setItem('tripora_token', res.access_token);
    localStorage.setItem('tripora_user', JSON.stringify(res.user));
    setToken(res.access_token);
    setUser(res.user);
  };

  const logout = () => {
    localStorage.removeItem('tripora_token');
    localStorage.removeItem('tripora_user');
    setToken(null);
    setUser(null);
  };

  const loginAsDemo = async () => {
    await login('demo@tripora.ai', 'tripora123');
  };

  const updateProfile = async (fullName?: string, email?: string, currency?: string) => {
    const updated = await authService.updateProfile(fullName, email, currency);
    localStorage.setItem('tripora_user', JSON.stringify(updated));
    setUser(updated);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!token && !!user,
        isLoading,
        login,
        register,
        logout,
        loginAsDemo,
        updateProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
