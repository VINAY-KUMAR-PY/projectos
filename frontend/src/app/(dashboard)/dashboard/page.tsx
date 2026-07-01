import Link from "next/link";
import { ProjectStats } from "@/components/projects/ProjectStats";

export default function DashboardPage() {
  return (
    <section className="space-y-5">
      <ProjectStats />
      <div className="grid gap-4 lg:grid-cols-[2fr_1fr]">
        <div className="panel p-5">
          <h1 className="text-xl font-semibold">Recent Projects</h1>
          <div className="mt-4 grid gap-3 md:grid-cols-2">
            <div className="rounded-md border p-4">No projects yet</div>
          </div>
        </div>
        <div className="panel p-5">
          <h2 className="font-semibold">Quick Actions</h2>
          <div className="mt-4 grid gap-2">
            <Link className="rounded-md bg-brand px-3 py-2 text-center text-white" href="/projects/new">New Project</Link>
            <Link className="rounded-md border px-3 py-2 text-center" href="/files">Upload File</Link>
            <Link className="rounded-md border px-3 py-2 text-center" href="/ai-chat">Open AI Chat</Link>
          </div>
        </div>
      </div>
    </section>
  );
}
