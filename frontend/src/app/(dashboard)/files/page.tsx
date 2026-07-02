"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { FolderOpen, Loader2 } from "lucide-react";

import { projectsApi } from "@/lib/api";

type ProjectItem = {
  id: number;
  title: string;
  description?: string | null;
};

export default function FilesPage() {
  const [projects, setProjects] = useState<ProjectItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    projectsApi
      .list()
      .then((response) => setProjects(response.data.items || []))
      .catch(() => setError("Could not load projects."))
      .finally(() => setLoading(false));
  }, []);

  return (
    <section className="space-y-5">
      <div>
        <h1 className="text-2xl font-semibold">Files</h1>
        <p className="mt-1 text-sm text-slate-500">Choose a project to upload and analyze files.</p>
      </div>

      {loading && (
        <div className="panel flex items-center gap-2 p-5 text-sm text-slate-600">
          <Loader2 className="h-4 w-4 animate-spin" />
          Loading projects
        </div>
      )}

      {error && <div className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>}

      {!loading && projects.length === 0 && !error && (
        <div className="panel p-5 text-sm text-slate-600">Create a project before uploading files.</div>
      )}

      <div className="grid gap-3 md:grid-cols-2">
        {projects.map((project) => (
          <Link key={project.id} className="panel block p-5 transition hover:border-blue-300" href={`/projects/${project.id}/files`}>
            <div className="flex items-start gap-3">
              <FolderOpen className="mt-1 h-5 w-5 shrink-0 text-blue-600" />
              <div className="min-w-0">
                <h2 className="truncate font-semibold text-slate-900">{project.title}</h2>
                {project.description && <p className="mt-1 line-clamp-2 text-sm text-slate-500">{project.description}</p>}
              </div>
            </div>
          </Link>
        ))}
      </div>
    </section>
  );
}
