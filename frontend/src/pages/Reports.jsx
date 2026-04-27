import { useEffect, useState } from "react";
import Card from "../components/Card";
import Loader from "../components/Loader";
import { getReports } from "../services/api";

function Reports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadReports = async () => {
      try {
        setLoading(true);
        setError("");
        const response = await getReports();
        setReports(response.data?.data?.reports || []);
      } catch (err) {
        setError(err?.response?.data?.message || err.message || "Failed to load reports.");
      } finally {
        setLoading(false);
      }
    };

    loadReports();
  }, []);

  if (loading) return <Loader text="Loading reports..." />;

  return (
    <div className="space-y-5">
      <h2 className="text-2xl font-semibold text-white">Reports</h2>
      {error && <p className="rounded-lg border border-red-500/40 bg-red-500/10 p-3 text-sm text-red-300">{error}</p>}

      <Card title="Generated HTML Reports" rightSlot={<span className="text-xs text-slate-400">{reports.length} files</span>}>
        {reports.length === 0 ? (
          <p className="text-sm text-slate-400">No reports found in the backend reports directory.</p>
        ) : (
          <ul className="space-y-2">
            {reports.map((report) => (
              <li
                key={report}
                className="flex items-center justify-between rounded-md border border-cyber-border bg-cyber-panelSoft px-3 py-2 text-sm"
              >
                <span className="truncate pr-3 text-slate-200">{report.file_name}</span>
                <div className="flex gap-2">
                  <a
                    href={`http://127.0.0.1:5000${report.view_path}`}
                    target="_blank"
                    rel="noreferrer"
                    className="rounded bg-cyan-500/20 px-3 py-1 text-cyan-300 hover:bg-cyan-500/30"
                  >
                    Open
                  </a>
                  <a
                    href={`http://127.0.0.1:5000${report.download_path}`}
                    className="rounded bg-emerald-500/20 px-3 py-1 text-emerald-300 hover:bg-emerald-500/30"
                  >
                    Download
                  </a>
                </div>
              </li>
            ))}
          </ul>
        )}
      </Card>
    </div>
  );
}

export default Reports;
