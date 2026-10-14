import { create } from 'zustand';
import { get as apiGet, post as apiPost, errorMessage } from '../lib/api';
import type { AuthResponse, Profile, RegisterResponse, User } from '../lib/types';

interface AuthState {
  token: string | null;
  user: User | null;
  profile: Profile | null;
  hydrated: boolean;
  setSession: (token: string, user: User) => void;
  hydrate: () => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<RegisterResponse>;
  logout: () => void;
  refreshProfile: () => Promise<void>;
}

function readCachedUser(): { user: User | null; profile: Profile | null } {
  try {
    const rawUser = localStorage.getItem('cp_user');
    const rawProfile = localStorage.getItem('cp_profile');
    return {
      user: rawUser ? (JSON.parse(rawUser) as User) : null,
      profile: rawProfile ? (JSON.parse(rawProfile) as Profile) : null,
    };
  } catch {
    return { user: null, profile: null };
  }
}

function writeCache(user: User | null, profile: Profile | null) {
  try {
    if (user) localStorage.setItem('cp_user', JSON.stringify(user));
    else localStorage.removeItem('cp_user');
    if (profile) localStorage.setItem('cp_profile', JSON.stringify(profile));
    else localStorage.removeItem('cp_profile');
  } catch {
    /* storage full / private mode — ignore, network is source of truth */
  }
}

const initialToken =
  typeof localStorage !== 'undefined' ? localStorage.getItem('cp_token') : null;
const initialCache =
  typeof localStorage !== 'undefined'
    ? readCachedUser()
    : { user: null, profile: null };

export const useAuth = create<AuthState>((set, get) => ({
  token: initialToken,
  // Render cached user instantly so refresh paints UI without waiting for /auth/me.
  user: initialCache.user,
  profile: initialCache.profile,
  hydrated: false,

  setSession: (token, user) => {
    localStorage.setItem('cp_token', token);
    writeCache(user, get().profile);
    set({ token, user });
  },

  hydrate: async () => {
    const token = get().token ?? localStorage.getItem('cp_token');
    if (!token) {
      set({ token: null, hydrated: true });
      return;
    }
    // Fast path: mark hydrated immediately from cache so App renders instantly.
    // Then refresh in background — refresh feels instant even on slow network.
    const cached = readCachedUser();
    set({ token, user: cached.user, profile: cached.profile, hydrated: true });
    try {
      const data = await apiGet<{ user: User; profile: Profile }>('/auth/me');
      writeCache(data.user, data.profile);
      // Only update if token didn't change (logout during fetch).
      if (get().token === token) {
        set({ user: data.user, profile: data.profile });
      }
    } catch {
      // Token invalid — clear session. Don't loop: api interceptor already
      // redirects to /login on 401 for non-auth calls.
      if (get().token === token) {
        localStorage.removeItem('cp_token');
        writeCache(null, null);
        set({ token: null, user: null, profile: null });
      }
    }
  },

  login: async (email, password) => {
    try {
      const data = await apiPost<AuthResponse>('/auth/login', { email, password });
      get().setSession(data.access_token, data.user);
      await get().hydrate();
    } catch (err) {
      throw new Error(errorMessage(err));
    }
  },

  register: async (full_name, email, password) => {
    try {
      const data = await apiPost<RegisterResponse>('/auth/register', { full_name, email, password });
      if (data.access_token && data.user) {
        get().setSession(data.access_token, data.user);
        await get().hydrate();
      }
      return data;
    } catch (err) {
      throw new Error(errorMessage(err));
    }
  },

  logout: () => {
    localStorage.removeItem('cp_token');
    writeCache(null, null);
    set({ token: null, user: null, profile: null });
  },

  refreshProfile: async () => {
    if (!get().token) return;
    try {
      const data = await apiGet<{ user: User; profile: Profile }>('/auth/me');
      writeCache(data.user, data.profile);
      set({ user: data.user, profile: data.profile });
    } catch {
      /* ignore */
    }
  },
}));
