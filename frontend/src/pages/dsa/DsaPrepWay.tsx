import { Link } from 'react-router-dom';
import {
  ArrowRight,
  Binary,
  BookOpen,
  CheckCircle2,
  Code2,
  ExternalLink,
  Layers,
  Map,
  Rocket,
  Target,
  Trophy,
  Youtube,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { Card } from '../../components/ui';

const DSA_COURSE = 'https://getsdeready.com/courses/dsa/lesson/convert-a-number-to-hexadecimal/?page_tab=overview';
const DSA_YOUTUBE = 'https://www.youtube.com/@CodeHelp';
const DSA_PLAYLIST_TELUGU = 'https://www.youtube.com/playlist?list=PLjzLBp9HHZWiJrhfJzTAEbwdpQIfUXtwP';
const DSA_PLAYLIST_ENGLISH = 'https://www.youtube.com/playlist?list=PLrS21S1jm43igE57Ye_edwds_iL7ZOAG4';

type Stage = { title: string; icon: LucideIcon; points: string[] };

const STAGES: Stage[] = [
  {
    title: 'Pick one language',
    icon: Code2,
    points: [
      'Choose Python, Java or C++ — each works for interviews.',
      'Learn input/output, loops, arrays, strings and hash maps.',
      'Stick with it for the whole journey; do not switch midway.',
    ],
  },
  {
    title: 'Learn complexity analysis',
    icon: Target,
    points: [
      'Understand Big-O time and space complexity.',
      'Recognise O(n), O(n log n), O(n²) patterns on the fly.',
      'Always estimate complexity before writing code.',
    ],
  },
  {
    title: 'Master core data structures',
    icon: Layers,
    points: [
      'Arrays, strings and hashing first.',
      'Then linked lists, stacks, queues, trees, heaps and tries.',
      'Practice each until you can code it blind-folded.',
    ],
  },
  {
    title: 'Learn the essential algorithms',
    icon: Binary,
    points: [
      'Recursion and backtracking.',
      'Two pointers, sliding window and binary search.',
      'Sorting (merge, quick), DFS and BFS on trees and graphs.',
    ],
  },
  {
    title: 'Level up with DP + greedy',
    icon: Rocket,
    points: [
      'Start with 1D then 2D dynamic programming.',
      'Learn the classic subsets — knapsack, LIS, grid paths.',
      'Re-solve every DP you learn after 2–3 days.',
    ],
  },
  {
    title: 'Solve daily, track your sheet',
    icon: CheckCircle2,
    points: [
      'Target 2–3 problems every day without fail.',
      'Use a structured sheet (Striver A2Z, Grind 75, NeetCode 150).',
      'Re-attempt skipped problems within a week.',
    ],
  },
  {
    title: 'Time yourself like an interview',
    icon: Trophy,
    points: [
      'Set a 25-minute timer per problem, coding included.',
      'Verbalise your approach out loud, then type it.',
      'Fix perf worst cases — no brute-force-only solutions.',
    ],
  },
];

const RESOURCES = [
  {
    icon: Binary,
    title: 'DSA Course — GetSReady',
    blurb: 'Free guided DSA lessons with theory, examples and practice (conversion, arrays, recursion and more).',
    href: DSA_COURSE,
  },
  {
    icon: Youtube,
    title: 'DSA on YouTube — CodeHelp',
    blurb: 'Love Babbar’s free, complete DSA series in Hindi (C++ and Java) — playlists make it easy to follow along.',
    href: DSA_YOUTUBE,
  },
  {
    icon: Youtube,
    title: 'Python + DSA (Telugu)',
    blurb: 'Complete free Python + DSA course in Telugu — ideal if you prefer Telugu explanations with English code.',
    href: DSA_PLAYLIST_TELUGU,
  },
  {
    icon: Youtube,
    title: 'DSA English Course',
    blurb: 'Free Algorithms & Data Structures course in English for beginners — theory plus solved examples.',
    href: DSA_PLAYLIST_ENGLISH,
  },
  {
    icon: BookOpen,
    title: 'Daily practice platforms',
    blurb: 'Level up on LeetCode, GeeksforGeeks and takeuforward.org — the exact problem sheets most companies reuse.',
    href: 'https://leetcode.com',
  },
];

export default function DsaPrepWay() {
  return (
    <div className="mx-auto max-w-5xl space-y-8">
      <div>
        <span className="inline-flex items-center gap-1.5 rounded-full bg-brand-100 px-3 py-1 text-xs font-bold text-brand-700 dark:bg-brand-500/15 dark:text-brand-300">
          <Map className="h-3.5 w-3.5" /> DSA
        </span>
        <h1 className="mt-3 text-2xl font-bold text-slate-900 dark:text-white">DSA Preparation Way</h1>
        <p className="mt-1 max-w-2xl text-sm text-slate-500 dark:text-slate-400">
          A step-by-step route to crack coding interviews — learn the fundamentals free, then grind daily. Finish
          every stage in order and keep a streak going.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {STAGES.map((stage, index) => (
          <Card key={stage.title} className="flex flex-col gap-3">
            <div className="flex items-center gap-3">
              <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-300">
                <stage.icon className="h-5 w-5" />
              </span>
              <div className="min-w-0">
                <p className="text-xs font-bold text-brand-600 dark:text-brand-400">STAGE {index + 1}</p>
                <h2 className="truncate font-bold text-slate-900 dark:text-white">{stage.title}</h2>
              </div>
            </div>
            <ul className="space-y-1.5 text-sm text-slate-500 dark:text-slate-400">
              {stage.points.map((point) => (
                <li key={point} className="flex items-start gap-2">
                  <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-500" />
                  {point}
                </li>
              ))}
            </ul>
          </Card>
        ))}
      </div>

      <div>
        <h2 className="mb-3 text-lg font-bold text-slate-900 dark:text-white">Free resources</h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {RESOURCES.map((resource) => (
            <a
              key={resource.title}
              href={resource.href}
              target="_blank"
              rel="noopener noreferrer"
              className="card group flex flex-col gap-3 p-5 transition hover:-translate-y-0.5 hover:border-brand-300 dark:hover:border-brand-500/40"
            >
              <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-300">
                <resource.icon className="h-5 w-5" />
              </span>
              <span className="flex items-center gap-1.5 font-bold text-slate-900 dark:text-white">
                {resource.title}
                <ExternalLink className="h-3.5 w-3.5 text-slate-400 transition group-hover:text-brand-500" />
              </span>
              <span className="text-sm text-slate-500 dark:text-slate-400">{resource.blurb}</span>
            </a>
          ))}
        </div>
      </div>

      <Card className="flex flex-col items-start gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="font-bold text-slate-900 dark:text-white">Ready to start?</h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Jump into the DSA course, or open a practice sheet and solve your first problem today.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <a
            href={DSA_COURSE}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-brand-700"
          >
            Start the course <ArrowRight className="h-4 w-4" />
          </a>
          <Link
            to="/it"
            className="inline-flex items-center gap-2 rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:bg-slate-800"
          >
            Explore IT career paths
          </Link>
        </div>
      </Card>
    </div>
  );
}