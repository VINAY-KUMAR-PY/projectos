"use client";

import { useState } from "react";
import { projectsApi } from "@/lib/api";

export function ProjectForm() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  async function submit() {
    const response = await projectsApi.create({ title, description });
    window.location.href = `/projects/${response.data.id}`;
  }

  return (
    <div className="panel max-w-xl p-5">
      <input className="mb-3 w-full rounded-md border p-2" placeholder="Project title" value={title} onChange={(event) => setTitle(event.target.value)} />
      <textarea className="mb-4 min-h-32 w-full rounded-md border p-2" placeholder="Project description" value={description} onChange={(event) => setDescription(event.target.value)} />
      <button className="rounded-md bg-brand px-4 py-2 text-white" onClick={submit}>Create project</button>
    </div>
  );
}
