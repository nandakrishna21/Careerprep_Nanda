import { Link, useNavigate } from 'react-router-dom';
import { LogOut, Search } from 'lucide-react';
import { useAuth } from '../stores/auth';
import { Avatar, Button, ThemeToggle } from '../components/ui';

export default function PublicLayout({ children }: { children: React.ReactNode }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/80 backdrop-blur dark:border-slate-800 dark:bg-slate-950/80">
        <div className="mx-auto flex h-16 max-w-7xl items-center gap-4 px-4 sm:px-6">
          <Link to="/" className="flex items-center gap-2">
            <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-violet-600 text-lg font-black text-white">
              C
            </span>
            <span className="text-lg font-extrabold tracking-tight text-slate-900 dark:text-white">
              CareerPrep <span className="text-brand-600 dark:text-brand-400">Hub</span>
            </span>
          </Link>

          <div className="relative ml-auto hidden max-w-sm flex-1 md:block">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <form
              onSubmit={(e) => {
                e.preventDefault();
                const q = new FormData(e.currentTarget).get('q') as string;
                if (q?.trim()) navigate(`/search?q=${encodeURIComponent(q.trim())}`);
              }}
            >
              <input name="q" placeholder="Search anything..." className="input pl-9" />
            </form>
          </div>

          <div className="ml-auto flex items-center gap-2 md:ml-0">
            <ThemeToggle />
            {user ? (
              <>
                <Link to="/dashboard">
                  <Avatar name={user.full_name} />
                </Link>
                <Button variant="ghost" onClick={() => { logout(); navigate('/'); }}>
                  <LogOut className="h-4 w-4" /> Logout
                </Button>
              </>
            ) : (
              <>
                <Link to="/login">
                  <Button variant="ghost">Login</Button>
                </Link>
                <Link to="/register">
                  <Button>Register</Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </header>
      {children}
    </div>
  );
}
