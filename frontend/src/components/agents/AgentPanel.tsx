"use client";

import { useState } from "react";
import { agentsApi } from "@/lib/api";

export function AgentPanel({ projectId }: { projectId: number }) {
  const [agent, setAgent] = useState("requirements");
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");

  async function run() {
    const response = await agentsApi.run(projectId, agent, input);
    setOutput(JSON.stringify(response.data.result, null, 2));
  }

  return (
    <div className="grid gap-4 lg:grid-cols-[360px_1fr]">
      <div className="panel p-4">
        <select className="mb-3 w-full rounded-md border p-2" value={agent} onChange={(event) => setAgent(event.target.value)}>
          {["requirements", "research", "architecture", "coding", "documentation", "diagrams", "presentation", "testing", "deployment", "learning", "file_analysis"].map((item) => (
            <option key={item}>{item}</option>
          ))}
        </select>
        <textarea className="mb-3 min-h-40 w-full rounded-md border p-2" value={input} onChange={(event) => setInput(event.target.value)} />
        <button className="rounded-md bg-brand px-4 py-2 text-white" onClick={run}>Run Agent</button>
      </div>
      <pre className="panel overflow-auto p-4 text-sm">{output || "Agent output appears here."}</pre>
    </div>
  );
}
