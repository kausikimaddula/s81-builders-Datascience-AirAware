import { NavLink } from "react-router-dom";

const tabs = [
  { to: "/", label: "Upload" },
  { to: "/ai-lab", label: "AI Lab" },
  { to: "/dashboard", label: "Dashboard" },
  { to: "/data-table", label: "Data Table" },
];

function NavBar() {
  return (
    <header className="sticky top-0 z-10 border-b border-ink/10 bg-shell/90 backdrop-blur">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-4 md:px-6">
        <div>
          <p className="font-display text-lg font-bold text-ink">NGO Data Cleaning & Analytics</p>
          <p className="text-xs text-slate">Build trust in complaint data quality</p>
        </div>
        <nav className="flex items-center gap-2 rounded-full bg-white p-1 shadow-soft">
          {tabs.map((tab) => (
            <NavLink
              key={tab.to}
              to={tab.to}
              className={({ isActive }) =>
                `rounded-full px-4 py-2 text-sm font-medium transition ${
                  isActive ? "bg-ocean text-white" : "text-slate hover:bg-mist"
                }`
              }
            >
              {tab.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  );
}

export default NavBar;
