import Link from "next/link";

export function ProjectCard({ id, title, status }: { id: number; title: string; status: string }) {
  return (
    <Link className="panel block p-4 hover:border-brand" href={`/projects/${id}`}>
      <div className="text-lg font-semibold">{title}</div>
      <div className="mt-2 text-sm text-slate-600">{status}</div>
    </Link>
  );
}
