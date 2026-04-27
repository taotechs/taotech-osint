import { useState } from "react";
import Card from "../components/Card";
import Loader from "../components/Loader";
import { scanDomain } from "../services/api";

function Domain() {
  const [domain, setDomain] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const summary = result?.summary;

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!domain.trim()) return setError("Please enter a domain.");

    try {
      setLoading(true);
      setError("");
      const response = await scanDomain(domain.trim());
      setResult(response.data?.data || null);
    } catch (err) {
      setError(err?.response?.data?.message || err.message || "Domain scan failed.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-5">
      <h2 className="text-2xl font-semibold text-white">Domain Search</h2>

      <Card title="Run Domain OSINT">
        <form onSubmit={handleSubmit} className="flex flex-col gap-3 md:flex-row">
          <input
            className="w-full rounded-lg border border-cyber-border bg-cyber-panelSoft px-3 py-2 text-slate-100 outline-none focus:border-cyan-400"
            value={domain}
            onChange={(event) => setDomain(event.target.value)}
            placeholder="Enter domain (example.com)"
          />
          <button className="rounded-lg bg-cyan-500 px-4 py-2 font-medium text-slate-900 hover:bg-cyan-400">
            Run OSINT Scan
          </button>
        </form>
      </Card>

      {loading && <Loader text="Running domain scan..." />}
      {error && <p className="rounded-lg border border-red-500/40 bg-red-500/10 p-3 text-sm text-red-300">{error}</p>}

      {result && (
        <div className="grid gap-4 md:grid-cols-2">
          <Card title="Domain Intelligence">
            <p className="mb-2 text-sm text-slate-300">
              Platforms found: {summary?.platforms_found ?? 0} | Links found: {summary?.links_found ?? 0}
            </p>
            <details>
              <summary className="cursor-pointer text-sm text-slate-300">Show raw output</summary>
              <pre className="mt-2 overflow-auto whitespace-pre-wrap text-xs text-slate-300">
                {JSON.stringify(result.results, null, 2)}
              </pre>
            </details>
          </Card>
          <Card title="Report">
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
              className="mt-2 block text-emerald-300 hover:underline"
            >
              Download Report
            </a>
          </Card>
        </div>
      )}
    </div>
  );
}

export default Domain;
