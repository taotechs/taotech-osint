function Loader({ text = "Loading..." }) {
  return (
    <div className="flex items-center gap-3 rounded-lg border border-cyber-border bg-cyber-panelSoft p-3">
      <span className="h-5 w-5 animate-spin rounded-full border-2 border-cyan-400 border-t-transparent" />
      <span className="text-sm text-slate-300">{text}</span>
    </div>
  );
}

export default Loader;
