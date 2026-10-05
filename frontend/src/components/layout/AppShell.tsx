import { NavLink, Outlet } from "react-router-dom";
import { Badge } from "../ui";

const navigation = [
  { label: "Dashboard", to: "/dashboard" },
  { label: "Documents", to: "/documents" },
  { label: "Jobs", to: "/jobs" },
  { label: "Settings", to: "/settings" },
];

export function AppShell() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true">S</span>
          <div><strong>SCI-DOC AI</strong><span>Scientific Intelligence</span></div>
        </div>
        <nav aria-label="Primary navigation">
          {navigation.map((item) => (
            <NavLink key={item.to} to={item.to} className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="main-content">
        <header className="topbar"><span>Document Intelligence Platform</span><Badge tone="success">Foundation</Badge></header>
        <section className="page-content"><Outlet /></section>
      </main>
    </div>
  );
}
