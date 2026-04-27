import { useState } from "react";
import Card from "../components/Card";
import Loader from "../components/Loader";
import { scanUsername } from "../services/api";

function Username() {
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!username.trim()) return setError("Please enter a username.");

    try {
      setLoading(true);
      setError("");
      const response = await scanUsername(username.trim());
      setResult(response.data?.data || null);
    } catch (err) {
      setError(err?.response?.data?.message || err.message || "Username scan failed.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const maigret = result?.results?.maigret;
  const sherlock = result?.results?.sherlock;

  return (
    <div className="space-y-5">
      <h2 className="text-2xl font-semibold text-white">Username Search</h2>

      <Card title="Run Username OSINT">
        <form onSubmit={handleSubmit} className="flex flex-col gap-3 md:flex-row">
          <input
            className="w-full rounded-lg border border-cyber-border bg-cyber-panelSoft px-3 py-2 text-slate-100 outline-none focus:border-cyan-400"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            placeholder="Enter username"
          />
          <button className="rounded-lg bg-cyan-500 px-4 py-2 font-medium text-slate-900 hover:bg-cyan-400">
            Run OSINT Scan
          </button>
        </form>
      </Card>

      {loading && <Loader text="Running username scan..." />}
      {error && <p className="rounded-lg border border-red-500/40 bg-red-500/10 p-3 text-sm text-red-300">{error}</p>}

      {result && (
        <div className="grid gap-4 md:grid-cols-2">
          <Card title="Maigret Results">
            <pre className="overflow-auto whitespace-pre-wrap text-xs text-slate-300">
              {JSON.stringify(maigret, null, 2)}
            </pre>
          </Card>
          <Card title="Sherlock Results">
            <pre className="overflow-auto whitespace-pre-wrap text-xs text-slate-300">
              {JSON.stringify(sherlock, null, 2)}
            </pre>
          </Card>
          <Card title="Platforms And Links">
            <p className="mb-2 text-sm text-slate-300">
              Outputs include platform discovery and profile links from Maigret/Sherlock command results.
            </p>
            <p className="text-xs text-slate-400">Review stdout/stderr in result cards for full extracted links.</p>
          </Card>
          <Card title="Report">
            {result.report_path ? (
              <div className="space-y-2">
                <a
                  href={`http://127.0.0.1:5000${result.report_path}`}
                  target="_blank"
                  rel="noreferrer"
                  className="block text-cyan-300 hover:underline"
                >
                  Open Structured Report
                </a>
                <a
                  href={`http://127.0.0.1:5000${result.report_download_path}`}
                  className="block text-emerald-300 hover:underline"
                >
                  Download Report
                </a>
              </div>
            ) : (
              <p className="text-sm text-slate-400">No report generated for this run.</p>
            )}
          </Card>
        </div>
      )}
    </div>
  );
}

export default Username;
