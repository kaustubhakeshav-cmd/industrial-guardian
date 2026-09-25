import { create } from 'zustand';

interface User {
  username: string;
  role: string;
}

interface AuthState {
  token: string | null;
  user: User | null;
  error: string | null;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('guardian_token'),
  user: null, // In a full app, we would decode the JWT or fetch user details here
  error: null,
  isLoading: false,

  login: async (username, password) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        throw new Error('Invalid operator credentials');
      }

      const data = await response.json();
      localStorage.setItem('guardian_token', data.access_token);
      
      set({ 
        token: data.access_token, 
        user: data.user,
        isLoading: false 
      });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  },

  logout: () => {
    localStorage.removeItem('guardian_token');
    set({ token: null, user: null });
  }
}));