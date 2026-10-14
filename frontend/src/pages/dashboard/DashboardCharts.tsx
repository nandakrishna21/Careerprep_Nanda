import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { Card } from '../../components/ui';
import type { DashboardData } from '../../lib/types';

const BRAND = '#6366f1';

function Badgeish({ children }: { children: React.ReactNode }) {
  return (
    <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-500 dark:bg-slate-800 dark:text-slate-400">
      {children}
    </span>
  );
}

export default function DashboardCharts({
  data,
  theme,
}: {
  data: DashboardData;
  theme: string;
}) {
  const tickColor = theme === 'dark' ? '#94a3b8' : '#64748b';
  const gridColor = theme === 'dark' ? '#1e293b' : '#e2e8f0';
  const tooltipStyle = {
    background: theme === 'dark' ? '#0f172a' : '#ffffff',
    border: `1px solid ${theme === 'dark' ? '#334155' : '#e2e8f0'}`,
    borderRadius: 12,
    color: theme === 'dark' ? '#e2e8f0' : '#0f172a',
    fontSize: 12,
  } as const;

  return (
    <section className="grid gap-4 lg:grid-cols-2 xl:grid-cols-3">
      <Card className="xl:col-span-3 lg:col-span-2">
        <div className="mb-4 flex items-center justify-between gap-2">
          <div>
            <h2 className="text-base font-bold text-slate-900 dark:text-white">Performance trend</h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">Score per quiz over time</p>
          </div>
          <Badgeish>{data.performance_trend.length} entries</Badgeish>
        </div>
        {data.performance_trend.length ? (
          <div className="h-56 text-slate-500 dark:text-slate-400">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data.performance_trend} margin={{ top: 4, right: 8, left: -18, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={gridColor} vertical={false} />
                <XAxis
                  dataKey="date"
                  tick={{ fill: tickColor, fontSize: 11 }}
                  tickLine={false}
                  axisLine={{ stroke: gridColor }}
                  tickFormatter={(v: string) => String(v).slice(5)}
                  minTickGap={24}
                />
                <YAxis
                  tick={{ fill: tickColor, fontSize: 11 }}
                  tickLine={false}
                  axisLine={false}
                  width={44}
                />
                <Tooltip contentStyle={tooltipStyle} labelStyle={{ color: tickColor }} />
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke={BRAND}
                  strokeWidth={2.5}
                  dot={{ r: 3, fill: BRAND, strokeWidth: 0 }}
                  activeDot={{ r: 5 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <p className="py-10 text-center text-sm text-slate-400">No quiz attempts yet.</p>
        )}
      </Card>

      <Card>
        <div className="mb-4">
          <h2 className="text-base font-bold text-slate-900 dark:text-white">Daily activity</h2>
          <p className="text-xs text-slate-500 dark:text-slate-400">Study hours per day</p>
        </div>
        {data.daily_activity.length ? (
          <div className="h-48 text-slate-500 dark:text-slate-400">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.daily_activity} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={gridColor} vertical={false} />
                <XAxis
                  dataKey="date"
                  tick={{ fill: tickColor, fontSize: 11 }}
                  tickLine={false}
                  axisLine={{ stroke: gridColor }}
                  tickFormatter={(v: string) => String(v).slice(5)}
                  minTickGap={20}
                />
                <YAxis tick={{ fill: tickColor, fontSize: 11 }} tickLine={false} axisLine={false} width={40} />
                <Tooltip contentStyle={tooltipStyle} labelStyle={{ color: tickColor }} cursor={{ fill: theme === 'dark' ? '#1e293b44' : '#eef2ff' }} />
                <Bar dataKey="hours" fill={BRAND} radius={[6, 6, 0, 0]} maxBarSize={28} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <p className="py-10 text-center text-sm text-slate-400">No activity logged yet.</p>
        )}
      </Card>

      <Card>
        <div className="mb-4">
          <h2 className="text-base font-bold text-slate-900 dark:text-white">Mock test performance</h2>
          <p className="text-xs text-slate-500 dark:text-slate-400">Accuracy per mock test</p>
        </div>
        {data.mock_performance.length ? (
          <div className="h-48 text-slate-500 dark:text-slate-400">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.mock_performance} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={gridColor} vertical={false} />
                <XAxis
                  dataKey="title"
                  tick={{ fill: tickColor, fontSize: 10 }}
                  tickLine={false}
                  axisLine={{ stroke: gridColor }}
                  interval={0}
                  tickFormatter={(v: string) => (v.length > 10 ? `${v.slice(0, 9)}…` : v)}
                />
                <YAxis tick={{ fill: tickColor, fontSize: 11 }} tickLine={false} axisLine={false} width={40} />
                <Tooltip contentStyle={tooltipStyle} labelStyle={{ color: tickColor }} cursor={{ fill: theme === 'dark' ? '#1e293b44' : '#eef2ff' }} />
                <Bar dataKey="accuracy" fill={BRAND} radius={[6, 6, 0, 0]} maxBarSize={34} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <p className="py-10 text-center text-sm text-slate-400">No mock tests taken yet.</p>
        )}
      </Card>
    </section>
  );
}
