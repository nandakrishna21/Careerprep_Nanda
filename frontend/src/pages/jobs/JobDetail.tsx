import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import {
  ArrowLeft,
  Bookmark,
  BookmarkCheck,
  Building2,
  CalendarClock,
  CalendarDays,
  ExternalLink,
  MapPin,
  Share2,
  Wallet,
} from 'lucide-react';
import { errorMessage, get, post, del } from '../../lib/api';
import type { Job } from '../../lib/types';
import { Badge, Button, Card, EmptyState, Spinner } from '../../components/ui';
import { postedAgo, titleCase } from '../../components/helpers';
import { useAuth } from '../../stores/auth';

function daysLeft(deadline: string | null): { label: string; tone: string } | null {
  if (!deadline) return null;
  const end = new Date(`${deadline.slice(0, 10)}T23:59:59`);
  const diff = Math.ceil((end.getTime() - Date.now()) / 86400000);
  if (Number.isNaN(diff)) return null;
  if (diff < 0) return { label: 'Closed', tone: 'bg-slate-100 text-slate-500 dark:bg-slate-800 dark:text-slate-400' };
  if (diff <= 3)
    return { label: `${diff}d left`, tone: 'bg-rose-100 text-rose-700 dark:bg-rose-500/15 dark:text-rose-300' };
  if (diff <= 10)
    return { label: `${diff}d left`, tone: 'bg-amber-100 text-amber-700 dark:bg-amber-500/15 dark:text-amber-300' };
  return { label: `${diff}d left`, tone: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-500/15 dark:text-emerald-300' };
}

export default function JobDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { token } = useAuth();
  const [job, setJob] = useState<Job | null>(null);
  const [missing, setMissing] = useState(false);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const data = await get<Job>(`/jobs/${id}`);
        if (alive) setJob(data);
      } catch {
        if (alive) setMissing(true);
      }
    })();
    return () => {
      alive = false;
    };
  }, [id]);

  const toggleSave = async () => {
    if (!job) return;
    if (!token) {
      toast('Sign in to save jobs.');
      navigate(`/login?next=${encodeURIComponent(`/jobs/${job.id}`)}`);
      return;
    }
    setBusy(true);
    try {
      if (job.is_saved) {
        await del(`/jobs/${job.id}/save`);
        setJob({ ...job, is_saved: false, save_status: undefined });
        toast.success('Removed from saved jobs');
      } else {
        await post(`/jobs/${job.id}/save`);
        setJob({ ...job, is_saved: true, save_status: 'saved' });
        toast.success('Job saved');
      }
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setBusy(false);
    }
  };

  const share = async () => {
    try {
      await navigator.clipboard.writeText(job?.share_url || window.location.href);
      toast.success('Link copied - share it anywhere.');
    } catch {
      toast.error('Could not copy the link.');
    }
  };

  if (missing) {
    return (
      <div className="mx-auto max-w-3xl">
        <EmptyState
          title="Job not found"
          description="This posting may have closed or been removed."
          action={<Button onClick={() => navigate('/jobs')}>Browse all jobs</Button>}
        />
      </div>
    );
  }

  if (!job) {
    return (
      <div className="mx-auto max-w-3xl">
        <Spinner />
      </div>
    );
  }

  const days = daysLeft(job.deadline);

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <button
        type="button"
        onClick={() => navigate('/jobs')}
        className="inline-flex items-center gap-1.5 text-sm font-semibold text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-200"
      >
        <ArrowLeft className="h-4 w-4" /> All jobs
      </button>

      <Card className="flex flex-col gap-4">
        <div className="flex items-start justify-between gap-2">
          <div className="min-w-0">
            <h1 className="text-xl font-bold leading-snug text-slate-900 dark:text-white">{job.title}</h1>
            <p className="mt-1 flex items-center gap-1.5 text-sm text-slate-500 dark:text-slate-400">
              <Building2 className="h-4 w-4 shrink-0" />
              {job.company}
            </p>
          </div>
          {days && (
            <span
              className={`shrink-0 inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-bold ${days.tone}`}
            >
              <CalendarClock className="h-3.5 w-3.5" />
              {days.label}
            </span>
          )}
        </div>

        <div className="flex flex-wrap gap-1.5">
          <Badge color={job.type === 'government' ? 'violet' : 'brand'}>
            {job.type === 'government' ? 'Government' : 'IT'}
          </Badge>
          <Badge color="slate">{titleCase(job.category)}</Badge>
          {job.role && <Badge color="brand">{job.role}</Badge>}
          {job.experience && <Badge color="slate">{job.experience}</Badge>}
          {job.is_saved && <Badge color="green">{titleCase(job.save_status ?? 'saved')}</Badge>}
        </div>

        <div className="flex flex-wrap gap-x-5 gap-y-1.5 text-sm text-slate-500 dark:text-slate-400">
          {job.location && (
            <span className="inline-flex items-center gap-1.5">
              <MapPin className="h-4 w-4" /> {job.location}
            </span>
          )}
          {job.posted_at && postedAgo(job.posted_at) && (
            <span className="inline-flex items-center gap-1.5">
              <CalendarDays className="h-4 w-4" /> Posted {postedAgo(job.posted_at)}
            </span>
          )}
          {job.salary && (
            <span className="inline-flex items-center gap-1.5">
              <Wallet className="h-4 w-4" /> {job.salary}
            </span>
          )}
        </div>

        {job.description && (
          <p className="whitespace-pre-line text-sm leading-relaxed text-slate-600 dark:text-slate-300">
            {job.description}
          </p>
        )}

        <div className="flex flex-wrap gap-2 pt-1">
          <a
            href={job.apply_link}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex flex-1 items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-brand-700"
          >
            Apply <ExternalLink className="h-4 w-4" />
          </a>
          <Button variant="outline" onClick={() => void toggleSave()} loading={busy}>
            {job.is_saved ? <BookmarkCheck className="h-4 w-4" /> : <Bookmark className="h-4 w-4" />}
            {job.is_saved ? 'Saved' : 'Save'}
          </Button>
          <Button variant="outline" onClick={() => void share()} aria-label="Copy link to this job">
            <Share2 className="h-4 w-4" /> Share
          </Button>
        </div>

        {!token && (
          <p className="text-center text-xs text-slate-400">
            <Link to={`/login?next=${encodeURIComponent(`/jobs/${job.id}`)}`} className="font-semibold text-brand-600 hover:underline dark:text-brand-400">
              Sign in
            </Link>{' '}
            to save jobs and track applications.
          </p>
        )}
      </Card>
    </div>
  );
}
