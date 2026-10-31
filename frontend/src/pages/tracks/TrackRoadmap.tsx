import { Link, useParams } from 'react-router-dom';
import {
  ArrowRight,
  BookOpen,
  CheckCircle2,
  Clock,
  Cloud,
  Code2,
  Database,
  ExternalLink,
  GraduationCap,
  Layers,
  Map,
  MessagesSquare,
  Signal,
  Trophy,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { Badge, Card, EmptyState } from '../../components/ui';
import { PageHeader, SectionHeader } from '../../components/SectionHeader';
import { CAREER_TRACKS, type TrackLevel } from '../../lib/careerTracks';

const STAGE_ICONS: LucideIcon[] = [
  Code2,
  Signal,
  Database,
  Cloud,
  Layers,
  MessagesSquare,
  Trophy,
];

const LEVEL_COLOR: Record<TrackLevel, 'green' | 'amber' | 'rose'> = {
  Beginner: 'green',
  Intermediate: 'amber',
  Advanced: 'rose',
};

export default function TrackRoadmap() {
  const { slug = '' } = useParams();
  const track = CAREER_TRACKS[slug];

  if (!track) {
    return (
      <div className="mx-auto max-w-3xl pt-10">
        <EmptyState
          title="Unknown track"
          description="This learning track does not exist yet. Pick one from the left panel."
          action={
            <Link
              to="/dashboard"
              className="rounded-xl bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700"
            >
              Back to dashboard
            </Link>
          }
        />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-6xl space-y-6">
      <PageHeader
        title={`${track.title} Roadmap`}
        subtitle={track.tagline}
        actions={
          <Link
            to={`/tracks/${track.slug}/resources`}
            className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-brand-700"
          >
            Free resources <ArrowRight className="h-4 w-4" />
          </Link>
        }
      />

      <Card className="flex items-start gap-3 border-brand-200 bg-brand-50/60 p-4 dark:border-brand-500/30 dark:bg-brand-500/10">
        <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-brand-100 text-brand-700 dark:bg-brand-500/20 dark:text-brand-300">
          <GraduationCap className="h-4 w-4" />
        </span>
        <div className="text-sm text-brand-800 dark:text-brand-200">
          <b>What it is:</b> {track.about}
        </div>
      </Card>

      <div className="flex flex-wrap gap-2">
        {track.skills.map((skill) => (
          <span
            key={skill}
            className="rounded-lg bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600 dark:bg-slate-800 dark:text-slate-300"
          >
            {skill}
          </span>
        ))}
      </div>

      <SectionHeader
        title="Roadmap — scratch to advance"
        subtitle={`${track.stages.length} stages. Finish them in order; each stage lists what to learn and the time it usually takes.`}
      />

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {track.stages.map((stage, index) => {
          const StageIcon = STAGE_ICONS[index % STAGE_ICONS.length];
          return (
          <Card key={stage.title} className="flex flex-col gap-3">
            <div className="flex items-center gap-3">
              <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-300">
                <StageIcon className="h-5 w-5" />
              </span>
              <div className="min-w-0">
                <p className="text-xs font-bold text-brand-600 dark:text-brand-400">
                  STAGE {index + 1}
                </p>
                <h2 className="truncate font-bold text-slate-900 dark:text-white">
                  {stage.title}
                </h2>
              </div>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              <Badge color={LEVEL_COLOR[stage.level]}>{stage.level}</Badge>
              <span className="inline-flex items-center gap-1 text-xs font-medium text-slate-500 dark:text-slate-400">
                <Clock className="h-3.5 w-3.5" /> {stage.duration}
              </span>
            </div>
            <p className="text-sm font-medium text-slate-700 dark:text-slate-300">
              {stage.goal}
            </p>
            <ul className="space-y-1.5 text-sm text-slate-500 dark:text-slate-400">
              {stage.topics.map((topic) => (
                <li key={topic} className="flex items-start gap-2">
                  <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-500" />
                  {topic}
                </li>
              ))}
            </ul>
          </Card>
          );
        })}
      </div>

      <SectionHeader
        title="Free resources for this track"
        subtitle={`${track.resources.length} hand-picked links — every one usable at no cost.`}
      />

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {track.resources.slice(0, 6).map((resource) => (
          <a
            key={resource.url}
            href={resource.url}
            target="_blank"
            rel="noopener noreferrer"
            className="group"
          >
            <Card className="flex h-full flex-col gap-2.5 transition group-hover:-translate-y-0.5 group-hover:border-brand-300 dark:group-hover:border-brand-500/40">
              <div className="flex items-start justify-between gap-2">
                <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-300">
                  <BookOpen className="h-5 w-5" />
                </span>
                <Badge color={resource.level === 'Beginner' ? 'green' : resource.level === 'Intermediate' ? 'amber' : 'rose'}>
                  {resource.level}
                </Badge>
              </div>
              <h3 className="flex items-center gap-1.5 font-bold text-slate-900 dark:text-white">
                {resource.name}
                <ExternalLink className="h-3.5 w-3.5 shrink-0 text-slate-400 transition group-hover:text-brand-500" />
              </h3>
              <p className="text-sm leading-relaxed text-slate-500 dark:text-slate-400">
                {resource.description}
              </p>
            </Card>
          </a>
        ))}
      </div>

      <div className="flex justify-center">
        <Link
          to={`/tracks/${track.slug}/resources`}
          className="inline-flex items-center gap-2 rounded-xl border border-slate-300 bg-white px-5 py-2.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:bg-slate-800"
        >
          View all {track.resources.length} free resources{' '}
          <ArrowRight className="h-4 w-4" />
        </Link>
      </div>

      <Card className="flex flex-col items-start gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="font-bold text-slate-900 dark:text-white">
            Related job roles
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            {track.roles.join(' · ')}
          </p>
        </div>
        <Link
          to="/jobs"
          className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-brand-700"
        >
          <Map className="h-4 w-4" /> Browse jobs
        </Link>
      </Card>
    </div>
  );
}
