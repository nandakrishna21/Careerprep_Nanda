// Hover-prefetch for left-panel routes: downloading the next route's chunk
// while the cursor travels there removes the lazy-load spinner on click.
// Vite dedupes these dynamic imports with App.tsx's React.lazy chunks,
// so no extra bytes are ever shipped.

const loaders: Record<string, () => Promise<unknown>> = {
  '/dashboard': () => import('../pages/dashboard/Dashboard'),
  '/leaderboard': () => import('../pages/Leaderboard'),
  '/search': () => import('../pages/Search'),
  '/profile': () => import('../pages/Profile'),
  '/jobs': () => import('../pages/jobs/Jobs'),
  '/my-jobs': () => import('../pages/jobs/MyJobsList'),
  '/gov': () => import('../pages/gov/GovDashboard'),
  '/gov/mock': () => import('../pages/gov/MockTests'),
  '/gov/pyqs': () => import('../pages/gov/Pyqs'),
  '/gov/current-affairs': () => import('../pages/gov/CurrentAffairs'),
  '/gov/videos': () => import('../pages/gov/VideoTutorials'),
  '/it': () => import('../pages/it/ItDashboard'),
  '/it/mock': () => import('../pages/it/ItMockTests'),
  '/dsa/prep-way': () => import('../pages/dsa/DsaPrepWay'),
  '/ai/quiz-generator': () => import('../pages/ai/AiQuizGenerator'),
  '/ai/interview': () => import('../pages/ai/AiInterview'),
  '/ai/planner': () => import('../pages/ai/AiPlanner'),
  '/ai/resume': () => import('../pages/ai/AiResume'),
  '/ai/resume/analyze': () => import('../pages/ai/AiResumeAnalyze'),
  '/ai/chat': () => import('../pages/ai/GeminiChat'),
  '/admin': () => import('../pages/admin/Admin'),
};

const done = new Set<string>();

export function prefetchPage(to: string): void {
  if (done.has(to)) return;
  const load = loaders[to];
  if (!load) return;
  done.add(to);
  load().catch(() => {
    // Chunk not needed yet / offline — the click will load it normally.
    done.delete(to);
  });
}
