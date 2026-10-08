import { create } from 'zustand';

type Theme = 'light' | 'dark';

function apply(theme: Theme) {
  document.documentElement.classList.toggle('dark', theme === 'dark');
  localStorage.setItem('cp_theme', theme);
}

const initial = (localStorage.getItem('cp_theme') as Theme) || 'light';
apply(initial);

interface ThemeState {
  theme: Theme;
  toggle: () => void;
}

export const useTheme = create<ThemeState>((set, get) => ({
  theme: initial,
  toggle: () => {
    const next: Theme = get().theme === 'light' ? 'dark' : 'light';
    apply(next);
    set({ theme: next });
  },
}));
