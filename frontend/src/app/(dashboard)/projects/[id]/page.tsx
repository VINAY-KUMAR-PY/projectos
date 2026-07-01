import Link from "next/link";

const tabs = ["workspace", "agents", "files", "code", "docs", "diagrams", "ppt", "tasks", "settings"];

export default function ProjectOverview({ params }: { params: { id: string } }) {
  return (
    <section className="space-y-4">
      <div className="panel p-5">
        <h1 className="text-2xl font-semibold">Project #{params.id}</h1>
        <div className="mt-3 h-2 rounded bg-slate-100"><div className="h-2 w-1/3 rounded bg-brand" /></div>
      </div>
      <div className="grid gap-2 md:grid-cols-3">
        {tabs.map((tab) => (
          <Link className="panel p-3 capitalize" href={`/projects/${params.id}/${tab}`} key={tab}>{tab}</Link>
        ))}
      </div>
    </section>
  );
}
