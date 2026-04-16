function StatCard({ title, value }) {
  return (
    <div className="animate-rise rounded-2xl border border-ink/10 bg-white p-5 shadow-soft">
      <p className="text-sm font-medium text-slate">{title}</p>
      <p className="mt-2 font-display text-3xl font-bold text-ink">{value}</p>
    </div>
  );
}

export default StatCard;
