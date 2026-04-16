import { useEffect, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  Cell,
} from "recharts";
import StatCard from "../components/StatCard";
import { getStats } from "../services/api";

const PIE_COLORS = ["#0f766e", "#f97360", "#334155", "#16a34a", "#2563eb", "#f59e0b"];

function DashboardPage() {
  const [stats, setStats] = useState({
    total_complaints: 0,
    category_counts: [],
    area_distribution: [],
    time_trends: [],
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await getStats();
        setStats(data);
      } catch {
        setStats({ total_complaints: 0, category_counts: [], area_distribution: [], time_trends: [] });
      }
    };

    fetchStats();
  }, []);

  return (
    <section className="space-y-6">
      <div className="grid gap-4 md:grid-cols-3">
        <StatCard title="Total Complaints" value={stats.total_complaints} />
        <StatCard title="Unique Categories" value={stats.category_counts.length} />
        <StatCard title="Areas Covered" value={stats.area_distribution.length} />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-2xl border border-ink/10 bg-white p-5 shadow-soft">
          <h3 className="font-display text-lg font-semibold text-ink">Category Distribution</h3>
          <div className="mt-4 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats.category_counts}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="category" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#0f766e" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-2xl border border-ink/10 bg-white p-5 shadow-soft">
          <h3 className="font-display text-lg font-semibold text-ink">Area Distribution</h3>
          <div className="mt-4 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={stats.area_distribution}
                  dataKey="count"
                  nameKey="area"
                  outerRadius={110}
                  label
                >
                  {stats.area_distribution.map((entry, index) => (
                    <Cell key={`cell-${entry.area}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="rounded-2xl border border-ink/10 bg-white p-5 shadow-soft">
        <h3 className="font-display text-lg font-semibold text-ink">Time Trend</h3>
        <div className="mt-4 h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={stats.time_trends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="count" stroke="#f97360" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </section>
  );
}

export default DashboardPage;
