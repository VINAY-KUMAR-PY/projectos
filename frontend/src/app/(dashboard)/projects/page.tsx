import Link from "next/link";
import { ProjectCard } from "@/components/projects/ProjectCard";

export default function ProjectsPage() {
  return (
    <section>
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Projects</h1>
        <Link className="rounded-md bg-brand px-3 py-2 text-white" href="/projects/new">New</Link>
      </div>
      <div className="grid gap-3 md:grid-cols-3">
        <ProjectCard id={1} title="Sample Project" status="draft" />
      </div>
    </section>
  );
}
