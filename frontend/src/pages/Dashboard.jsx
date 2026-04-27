import { useEffect, useState } from "react";
import Card from "../components/Card";
import Loader from "../components/Loader";
import { getHealth, getReports } from "../services/api";

function Dashboard() {
  const [health, setHealth] = useState(null);
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        setLoading(true);
        setError("");
        const [healthRes, reportsRes] = await Promise.all([getHealth(), getReports()]);
        setHealth(healthRes.data?.data?.status || "unknown");
        setReports(reportsRes.data?.data?.reports || []);
      } catch (err) {
        setError(err?.response?.data?.message || err.message || "Failed to load dashboard.");
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, []);

  if (loading) return <Loader text="Loading dashboard..." />;

  return (
    <div className="space-y-5">
      <div>
        <h2 className="text-2xl font-semibold text-white">Dashboard</h2>
        <p className="text-sm text-slate-400">Operational overview of OSINT scanning services.</p>
      </div>

      {error && <p className="rounded-lg border border-red-500/40 bg-red-500/10 p-3 text-sm text-red-300">{error}</p>}

      <div className="grid gap-4 md:grid-cols-3">
        <Card title="System Health">
          <p className={`text-lg font-semibold ${health === "ok" ? "text-green-400" : "text-red-400"}`}>
            {health === "ok" ? "Online" : "Unavailable"}
          </p>
        </Card>
        <Card title="Generated Reports">
          <p className="text-lg font-semibold text-cyan-300">{reports.length}</p>
        </Card>
        <Card title="Quick Actions">
          <div className="text-sm text-slate-300">
            <p>- Run Username scan</p>
            <p>- Run Email scan</p>
            <p>- Run Domain scan</p>
          </div>
        </Card>
      </div>

      <Card title="Recent Reports">
        {reports.length === 0 ? (
          <p className="text-sm text-slate-400">No reports available yet.</p>
        ) : (
          <ul className="space-y-2 text-sm text-slate-200">
            {reports.slice(0, 8).map((report) => (
              <li
                key={report.file_name}
                className="rounded-md border border-cyber-border bg-cyber-panelSoft px-3 py-2"
              >
                <a
                  href={`http://127.0.0.1:5000${report.view_path}`}
                  target="_blank"
                  rel="noreferrer"
                  className="text-cyan-300 hover:underline"
                >
                  {report.file_name}
                </a>
              </li>
            ))}
          </ul>
        )}
      </Card>
    </div>
  );
}

export default Dashboard;
