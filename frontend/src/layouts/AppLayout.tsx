import { Link, NavLink, useLocation, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import {
  Binary,
  Briefcase,
  Building2,
  ChevronDown,
  ExternalLink,
  Flame,
  GraduationCap,
  LayoutDashboard,
  LogOut,
  Map,
  Menu,
  Monitor,
  Search,
  Sparkles,
  Trophy,
  User as UserIcon,
  X,
  Shield,
  Newspaper,
  FileText,
  Youtube,
} from 'lucide-react';
import { useAuth } from '../stores/auth';
import { Avatar, ThemeToggle } from '../components/ui';

const YOUTUBE_CHANNEL = 'https://www.youtube.com/@freejobsinformation';
const DSA_COURSE = 'https://getsdeready.com/courses/dsa/lesson/convert-a-number-to-hexadecimal/?page_tab=overview';
const DSA_YOUTUBE = 'https://www.youtube.com/@CodeHelp';
const DSA_PLAYLIST_TELUGU = 'https://www.youtube.com/playlist?list=PLjzLBp9HHZWiJrhfJzTAEbwdpQIfUXtwP';
const DSA_PLAYLIST_ENGLISH = 'https://www.youtube.com/playlist?list=PLrS21S1jm43igE57Ye_edwds_iL7ZOAG4';

type NavItem = {
  label: string;
  icon: typeof LayoutDashboard;
  to?: string;
  href?: string;
  adminOnly?: boolean;
};

type NavGroup = { label: string; items: NavItem[] };

const nav: NavGroup[] = [
  {
    label: 'Overview',
    items: [
      { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
      { to: '/leaderboard', label: 'Leaderboard', icon: Trophy },
      { to: '/jobs', label: 'Jobs & Opportunities', icon: Briefcase },
    ],
  },
  {
    label: 'Government',
    items: [
      { to: '/gov', label: 'Government Hub', icon: Building2 },
      { to: '/gov/mock', label: 'Mock Tests', icon: FileText },
      { to: '/gov/pyqs', label: 'Previous Year Qs', icon: FileText },
      { to: '/gov/current-affairs', label: 'Current Affairs', icon: Newspaper },
    ],
  },
  {
    label: 'IT Career',
    items: [
      { to: '/it', label: 'IT Career Hub', icon: Monitor },
      { to: '/it/mock', label: 'IT Mock Tests', icon: FileText },
    ],
  },
  {
    label: 'DSA',
    items: [
      { to: '/dsa/prep-way', label: 'DSA Prep Way', icon: Map },
      { href: DSA_COURSE, label: 'DSA Course', icon: Binary },
      { href: DSA_YOUTUBE, label: 'DSA on YouTube', icon: Youtube },
      { href: DSA_PLAYLIST_TELUGU, label: 'DSA Playlist (Telugu)', icon: Youtube },
      { href: DSA_PLAYLIST_ENGLISH, label: 'DSA Playlist (English)', icon: Youtube },
    ],
  },
  {
    label: 'YouTube',
    items: [
      { href: YOUTUBE_CHANNEL, label: 'Free Jobs Information', icon: Youtube },
    ],
  },
  {
    label: 'AI Tools',
    items: [
      { to: '/ai/quiz-generator', label: 'AI Quiz Generator', icon: Sparkles },
      { to: '/ai/interview', label: 'AI Mock Interview', icon: Sparkles },
      { to: '/ai/planner', label: 'AI Study Planner', icon: Sparkles },
      { to: '/ai/resume', label: 'AI Resume Builder', icon: FileText },
      { to: '/ai/resume/analyze', label: 'Resume Analyzer', icon: FileText },
    ],
  },
  {
    label: 'Account',
    items: [
      { to: '/profile', label: 'Profile', icon: UserIcon },
      { to: '/admin', label: 'Admin Panel', icon: Shield, adminOnly: true },
    ],
  },
];

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const { user, profile, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [open, setOpen] = useState(false);
  const [menu, setMenu] = useState(false);

  const close = () => setOpen(false);

  return (
    <div className="flex min-h-screen">
      <aside
        className={`fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-slate-200 bg-white transition-transform dark:border-slate-800 dark:bg-slate-900 lg:translate-x-0 ${
          open ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex h-16 items-center justify-between px-5">
          <Link to="/" className="flex items-center gap-2" onClick={close}>
            <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-violet-600 text-lg font-black text-white">
              C
            </span>
            <span className="text-lg font-extrabold tracking-tight text-slate-900 dark:text-white">
              CareerPrep <span className="text-brand-600 dark:text-brand-400">Hub</span>
            </span>
          </Link>
          <button className="lg:hidden" onClick={close}>
            <X className="h-5 w-5 text-slate-500" />
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto px-3 pb-6">
          {nav.map((group) => {
            const items = group.items.filter((i) => !i.adminOnly || user?.role === 'admin');
            if (!items.length) return null;
            return (
              <div key={group.label} className="mb-5">
                <p className="px-3 pb-1.5 text-[11px] font-bold uppercase tracking-wider text-slate-400">{group.label}</p>
                {items.map((item) => {
                  const classes =
                    'mb-0.5 flex items-center gap-3 rounded-xl px-3 py-2 text-sm font-medium transition';
                  if (item.href) {
                    return (
                      <a
                        key={item.href}
                        href={item.href}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={close}
                        className={`${classes} text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800`}
                      >
                        <item.icon className="h-4 w-4 shrink-0 text-rose-500" />
                        {item.label}
                        <ExternalLink className="ml-auto h-3.5 w-3.5 shrink-0 text-slate-400" />
                      </a>
                    );
                  }
                  return (
                    <NavLink
                      key={item.to}
                      to={item.to ?? '/'}
                      onClick={close}
                      className={({ isActive }) =>
                        `${classes} ${
                          isActive
                            ? 'bg-brand-50 text-brand-700 dark:bg-brand-500/15 dark:text-brand-300'
                            : 'text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800'
                        }`
                      }
                    >
                      <item.icon className="h-4 w-4 shrink-0" />
                      {item.label}
                    </NavLink>
                  );
                })}
              </div>
            );
          })}
        </nav>

        <a
          href={YOUTUBE_CHANNEL}
          target="_blank"
          rel="noopener noreferrer"
          onClick={close}
          className="mx-3 mb-3 flex items-center gap-3 rounded-2xl border border-rose-200 bg-rose-50 p-3 transition hover:border-rose-300 hover:bg-rose-100 dark:border-rose-500/25 dark:bg-rose-500/10 dark:hover:bg-rose-500/20"
        >
          <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-rose-600 text-white">
            <Youtube className="h-5 w-5" />
          </span>
          <span className="min-w-0 flex-1">
            <span className="block text-[10px] font-bold uppercase tracking-wider text-rose-600 dark:text-rose-400">
              Watch on YouTube
            </span>
            <span className="block truncate text-sm font-semibold text-slate-800 dark:text-slate-100">
              Free Jobs Information
            </span>
          </span>
          <ExternalLink className="h-4 w-4 shrink-0 text-rose-500" />
        </a>

        {profile && (
          <div className="border-t border-slate-200 p-4 dark:border-slate-800">
            <div className="mb-1 flex items-center justify-between text-xs">
              <span className="font-semibold text-slate-500">Level {profile.level}</span>
              <span className="flex items-center gap-1 font-semibold text-amber-500">
                <Flame className="h-3.5 w-3.5" /> {profile.streak_days}d
              </span>
            </div>
            <div className="flex items-center gap-1 text-xs font-bold text-brand-600 dark:text-brand-400">
              <GraduationCap className="h-3.5 w-3.5" /> {profile.xp} XP
            </div>
          </div>
        )}
      </aside>

      {open && <div className="fixed inset-0 z-30 bg-black/40 lg:hidden" onClick={close} />}

      <div className="flex min-w-0 flex-1 flex-col lg:pl-64">
        <header className="sticky top-0 z-20 flex h-16 items-center gap-3 border-b border-slate-200 bg-white/80 px-4 backdrop-blur dark:border-slate-800 dark:bg-slate-900/80">
          <button className="rounded-lg p-2 hover:bg-slate-100 dark:hover:bg-slate-800 lg:hidden" onClick={() => setOpen(true)}>
            <Menu className="h-5 w-5" />
          </button>

          <form
            className="relative hidden max-w-md flex-1 sm:block"
            onSubmit={(e) => {
              e.preventDefault();
              const q = new FormData(e.currentTarget).get('q') as string;
              if (q?.trim()) navigate(`/search?q=${encodeURIComponent(q.trim())}`);
            }}
          >
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              name="q"
              placeholder="Search courses, quizzes, jobs..."
              className="input pl-9"
            />
          </form>

          <div className="ml-auto flex items-center gap-2">
            <ThemeToggle />
            <div className="relative">
              <button
                className="flex items-center gap-2 rounded-xl p-1.5 hover:bg-slate-100 dark:hover:bg-slate-800"
                onClick={() => setMenu((v) => !v)}
              >
                <Avatar name={user?.full_name ?? 'U'} color={profile?.avatar_color} />
                <ChevronDown className="h-4 w-4 text-slate-400" />
              </button>
              {menu && (
                <>
                  <div className="fixed inset-0 z-30" onClick={() => setMenu(false)} />
                  <div className="absolute right-0 z-40 mt-2 w-52 overflow-hidden rounded-xl border border-slate-200 bg-white py-1 shadow-lg dark:border-slate-700 dark:bg-slate-900">
                    <div className="border-b border-slate-100 px-4 py-2 dark:border-slate-800">
                      <p className="truncate text-sm font-semibold">{user?.full_name}</p>
                      <p className="truncate text-xs text-slate-400">{user?.email}</p>
                    </div>
                    <Link
                      to="/profile"
                      onClick={() => setMenu(false)}
                      className="block px-4 py-2 text-sm hover:bg-slate-50 dark:hover:bg-slate-800"
                    >
                      Profile
                    </Link>
                    <button
                      className="flex w-full items-center gap-2 px-4 py-2 text-sm text-rose-600 hover:bg-slate-50 dark:hover:bg-slate-800"
                      onClick={() => {
                        logout();
                        navigate('/');
                      }}
                    >
                      <LogOut className="h-4 w-4" /> Logout
                    </button>
                  </div>
                </>
              )}
            </div>
          </div>
        </header>

        <main className="flex-1 p-4 sm:p-6 lg:p-8">{children}</main>
      </div>
    </div>
  );
}
