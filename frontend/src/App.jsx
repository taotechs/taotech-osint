import { NavLink, Route, Routes } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Username from "./pages/Username";
import Email from "./pages/Email";
import Domain from "./pages/Domain";
import Reports from "./pages/Reports";

const navItems = [
  { label: "Dashboard", path: "/" },
  { label: "Username Search", path: "/username" },
  { label: "Email Search", path: "/email" },
  { label: "Domain Search", path: "/domain" },
  { label: "Reports", path: "/reports" },
];

function App() {
  return (
    <div className="min-h-screen bg-cyber-bg text-slate-100">
      <div className="flex">
        <Sidebar items={navItems} />

        <div className="flex min-h-screen flex-1 flex-col">
          <header className="sticky top-0 z-20 border-b border-cyber-border bg-cyber-panel/90 backdrop-blur">
            <div className="flex items-center justify-between px-6 py-4">
              <div>
                <h1 className="text-lg font-semibold text-cyan-300">
                  Taotech OSINT Toolkit
                </h1>
                <p className="text-xs text-slate-400">
                  Cyber Intelligence Dashboard
                </p>
              </div>
              <nav className="hidden gap-3 md:flex">
                {navItems.map((item) => (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    className={({ isActive }) =>
                      `rounded-md px-3 py-1 text-sm ${
                        isActive
                          ? "bg-cyan-500/20 text-cyan-300"
                          : "text-slate-300 hover:bg-slate-800"
                      }`
                    }
                  >
                    {item.label}
                  </NavLink>
                ))}
              </nav>
            </div>
          </header>

          <main className="flex-1 p-6">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/username" element={<Username />} />
              <Route path="/email" element={<Email />} />
              <Route path="/domain" element={<Domain />} />
              <Route path="/reports" element={<Reports />} />
            </Routes>
          </main>
        </div>
      </div>
    </div>
  );
}

export default App;
