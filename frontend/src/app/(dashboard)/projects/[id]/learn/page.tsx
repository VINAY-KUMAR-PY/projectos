"use client";

import { useState } from "react";
import { learningApi } from "@/lib/api";

const actions = ["explain_concept", "generate_quiz", "viva_practice", "interview_questions", "explain_my_project"];

export default function LearnPage({ params }: { params: { id: string } }) {
  const projectId = Number(params.id);
  const [action, setAction] = useState(actions[0]);
  const [message, setMessage] = useState("");
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function run() {
    setLoading(true);
    setError("");
    try {
      const response = await learningApi.run(action, projectId, message || "Help me prepare for my project defense.");
      setContent(response.data.content);
    } catch {
      setError("Learning mode could not respond. Check login or plan limits.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="space-y-4">
      <div className="panel p-5">
        <div className="mb-3 flex flex-wrap gap-2">
          <select className="rounded-md border p-2 text-sm" value={action} onChange={(event) => setAction(event.target.value)}>
            {actions.map((item) => <option key={item}>{item}</option>)}
          </select>
          <button className="rounded-md bg-brand px-4 py-2 text-sm text-white disabled:opacity-60" disabled={loading} onClick={run}>
            {loading ? "Thinking..." : "Run Learning Mode"}
          </button>
        </div>
        <textarea className="min-h-28 w-full rounded-md border p-2 text-sm" value={message} onChange={(event) => setMessage(event.target.value)} placeholder="Ask for a concept explanation, quiz, viva practice, or defense script." />
        {error ? <p className="mt-3 text-sm text-red-600">{error}</p> : null}
      </div>
      {content ? <pre className="panel whitespace-pre-wrap p-4 text-sm">{content}</pre> : null}
    </section>
  );
}
