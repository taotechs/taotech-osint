function Card({ title, children, rightSlot }) {
  return (
    <section className="rounded-xl border border-cyber-border bg-cyber-panel p-4 shadow">
      <div className="mb-3 flex items-center justify-between">
        <h3 className="text-sm font-semibold uppercase tracking-wide text-cyan-300">
          {title}
        </h3>
        {rightSlot}
      </div>
      <div>{children}</div>
    </section>
  );
}

export default Card;
