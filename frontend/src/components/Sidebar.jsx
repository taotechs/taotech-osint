import { NavLink } from "react-router-dom";

function Sidebar({ items }) {
  return (
    <aside className="hidden min-h-screen w-64 border-r border-cyber-border bg-cyber-panel lg:block">
      <div className="border-b border-cyber-border p-6">
        <p className="text-xs uppercase tracking-widest text-cyan-400">
          OSINT Control
        </p>
        <h2 className="mt-2 text-xl font-bold text-white">Taotech</h2>
      </div>
      <nav className="space-y-1 p-4">
        {items.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `block rounded-lg px-4 py-2 text-sm transition ${
                isActive
                  ? "bg-cyan-500/20 text-cyan-300 shadow-glow"
                  : "text-slate-300 hover:bg-cyber-panelSoft hover:text-cyan-200"
              }`
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;
