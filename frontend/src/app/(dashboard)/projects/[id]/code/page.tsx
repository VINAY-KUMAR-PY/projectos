"use client";

import { useState } from "react";
import { apiBaseUrl, generationApi } from "@/lib/api";

type CodeResult = { content?: string };

export default function CodePage({ params }: { params: { id: string } }) {
  const projectId = Number(params.id);
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState<CodeResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function build(action = "generate") {
    setLoading(true);
    setError("");
    try {
      const response = await generationApi.code(projectId, { action, prompt });
      setResult(response.data);
    } catch {
      setError("Code action failed. Check plan limits or try a smaller prompt.");
    } finally {
      setLoading(false);
    }
  }

  let parsed: { file_tree?: string[]; zip_url?: string; summary?: string } = {};
  try {
    parsed = result?.content ? JSON.parse(result.content) : {};
  } catch {
    parsed = {};
  }

  return (
    <section className="space-y-4">
      <div className="panel p-5">
        <textarea className="mb-3 min-h-28 w-full rounded-md border p-2" placeholder="Describe the scaffold, code to explain, or bug to fix" value={prompt} onChange={(event) => setPrompt(event.target.value)} />
        <div className="flex flex-wrap gap-2">
          {["generate", "explain", "review", "fix_bug"].map((action) => (
            <button className="rounded-md bg-brand px-4 py-2 text-sm text-white disabled:opacity-60" disabled={loading} key={action} onClick={() => build(action)}>
              {loading ? "Working..." : action.replace("_", " ")}
            </button>
          ))}
        </div>
        {error ? <p className="mt-3 text-sm text-red-600">{error}</p> : null}
      </div>
      {parsed.zip_url ? <a className="text-sm font-medium text-brand" href={`${apiBaseUrl}${parsed.zip_url}`}>Download generated code zip</a> : null}
      {parsed.file_tree ? (
        <pre className="panel whitespace-pre-wrap p-4 text-sm">{parsed.file_tree.join("\n")}</pre>
      ) : (
        result?.content ? <pre className="panel whitespace-pre-wrap p-4 text-sm">{result.content}</pre> : null
      )}
    </section>
  );
}
