"use client";

import { useState } from "react";
import { apiBaseUrl, generationApi } from "@/lib/api";

type Result = { file_url?: string; title?: string; content?: string };

export default function DocsPage({ params }: { params: { id: string } }) {
  const projectId = Number(params.id);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<Result | null>(null);

  async function generate() {
    setLoading(true);
    setError("");
    try {
      const response = await generationApi.document(projectId);
      setResult(response.data);
    } catch (err) {
      setError("Could not generate the document. Check your plan limits or login state.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="space-y-4">
      <div className="panel p-5">
        <div className="mb-3 flex items-center justify-between gap-3">
          <h1 className="text-xl font-semibold">Project Document</h1>
          <button className="rounded-md bg-brand px-4 py-2 text-sm text-white disabled:opacity-60" onClick={generate} disabled={loading}>
            {loading ? "Generating..." : "Download Document"}
          </button>
        </div>
        {error ? <p className="text-sm text-red-600">{error}</p> : null}
        {result?.file_url ? (
          <a className="text-sm font-medium text-brand" href={`${apiBaseUrl}${result.file_url}`}>
            {result.title || "Download generated report"}
          </a>
        ) : (
          <p className="text-sm text-slate-600">Generate a full academic project report from project memory and AI outputs.</p>
        )}
      </div>
      {result?.content ? <pre className="panel whitespace-pre-wrap p-4 text-sm">{result.content}</pre> : null}
    </section>
  );
}
