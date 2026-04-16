function LoadingBar({ percent = 0, stage = "idle" }) {
  return (
    <div className="rounded-xl border border-ink/10 bg-white p-4 shadow-soft">
      <div className="mb-2 flex items-center justify-between text-sm text-slate">
        <span>Cleaning progress</span>
        <span>{percent}%</span>
      </div>
      <div className="h-3 overflow-hidden rounded-full bg-mist">
        <div
          className="h-full rounded-full bg-ocean transition-all duration-300"
          style={{ width: `${percent}%` }}
        />
      </div>
      <p className="mt-2 text-xs text-slate">{stage}</p>
    </div>
  );
}

export default LoadingBar;
