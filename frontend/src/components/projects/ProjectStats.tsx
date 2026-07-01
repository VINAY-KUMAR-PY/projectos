export function ProjectStats() {
  const stats = [
    ["Total Projects", "0"],
    ["Agent Runs Today", "0"],
    ["Files Uploaded", "0"],
    ["Tasks Completed", "0"]
  ];
  return (
    <div className="grid gap-3 md:grid-cols-4">
      {stats.map(([label, value]) => (
        <div className="panel p-4" key={label}>
          <div className="text-sm text-slate-500">{label}</div>
          <div className="mt-2 text-2xl font-semibold">{value}</div>
        </div>
      ))}
    </div>
  );
}
