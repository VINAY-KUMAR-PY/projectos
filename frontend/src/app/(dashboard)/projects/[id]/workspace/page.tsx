"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { collaborationApi, projectsApi } from "@/lib/api";

type Project = { id: number; title: string; description?: string; status: string; progress_score?: number };
type Member = { id: number; email: string; role: string; status: string };
type Comment = { id: number; body: string; entity_type: string; entity_id: number };

const tabs = ["agents", "files", "code", "docs", "diagrams", "ppt", "tasks", "learn"];

export default function ProjectWorkspacePage({ params }: { params: { id: string } }) {
  const projectId = Number(params.id);
  const [project, setProject] = useState<Project | null>(null);
  const [members, setMembers] = useState<Member[]>([]);
  const [comments, setComments] = useState<Comment[]>([]);
  const [email, setEmail] = useState("");
  const [comment, setComment] = useState("");
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    try {
      const [projectResponse, memberResponse, commentResponse] = await Promise.all([
        projectsApi.get(projectId),
        collaborationApi.members(projectId),
        collaborationApi.comments(projectId)
      ]);
      setProject(projectResponse.data);
      setMembers(memberResponse.data.items);
      setComments(commentResponse.data.items);
    } catch {
      setError("Could not load workspace data.");
    }
  }, [projectId]);

  useEffect(() => {
    load();
  }, [load]);

  async function invite() {
    await collaborationApi.invite(projectId, { email, role: "viewer" });
    setEmail("");
    load();
  }

  async function addComment() {
    await collaborationApi.addComment(projectId, { entity_type: "project", entity_id: projectId, body: comment });
    setComment("");
    load();
  }

  return (
    <section className="space-y-4">
      <div className="panel p-5">
        <h1 className="text-xl font-semibold">{project?.title || "Project Workspace"}</h1>
        <p className="mt-2 text-sm text-slate-600">{project?.description || "Loading project context..."}</p>
        {error ? <p className="mt-3 text-sm text-red-600">{error}</p> : null}
        <div className="mt-4 flex flex-wrap gap-2">
          {tabs.map((tab) => (
            <Link className="rounded-md border px-3 py-2 text-sm hover:bg-slate-50" href={`/projects/${projectId}/${tab}`} key={tab}>
              {tab}
            </Link>
          ))}
        </div>
      </div>
      <div className="grid gap-4 lg:grid-cols-2">
        <div className="panel p-5">
          <h2 className="font-semibold">Team</h2>
          <div className="mt-3 flex gap-2">
            <input className="min-w-0 flex-1 rounded-md border p-2 text-sm" placeholder="member@example.com" value={email} onChange={(event) => setEmail(event.target.value)} />
            <button className="rounded-md bg-brand px-4 py-2 text-sm text-white" onClick={invite}>Invite</button>
          </div>
          <ul className="mt-4 space-y-2 text-sm">
            {members.map((member) => <li key={member.id}>{member.email} - {member.role} - {member.status}</li>)}
          </ul>
        </div>
        <div className="panel p-5">
          <h2 className="font-semibold">Comments</h2>
          <textarea className="mt-3 min-h-24 w-full rounded-md border p-2 text-sm" value={comment} onChange={(event) => setComment(event.target.value)} />
          <button className="mt-2 rounded-md bg-brand px-4 py-2 text-sm text-white" onClick={addComment}>Add Comment</button>
          <ul className="mt-4 space-y-2 text-sm">
            {comments.map((item) => <li key={item.id}>{item.body}</li>)}
          </ul>
        </div>
      </div>
    </section>
  );
}
