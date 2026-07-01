"use client";

import { useState } from "react";
import { apiBaseUrl, generationApi } from "@/lib/api";

type Slide = { title: string; bullets?: string[] };
type Result = { file_url?: string; content?: string; metadata?: { slides?: Slide[] } };

export default function PptPage({ params }: { params: { id: string } }) {
  const projectId = Number(params.id);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<Result | null>(null);

  async function generate() {
    setLoading(true);
    setError("");
    try {
      const response = await generationApi.ppt(projectId);
      setResult(response.data);
    } catch {
      setError("Could not generate presentation. Check plan limits or try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="space-y-4">
      <div className="panel p-5">
        <div className="mb-3 flex items-center justify-between gap-3">
          <h1 className="text-xl font-semibold">Presentation</h1>
          <button className="rounded-md bg-brand px-4 py-2 text-sm text-white disabled:opacity-60" onClick={generate} disabled={loading}>
            {loading ? "Generating..." : "Generate PPT"}
          </button>
        </div>
        {error ? <p className="text-sm text-red-600">{error}</p> : null}
        {result?.file_url ? <a className="text-sm font-medium text-brand" href={`${apiBaseUrl}${result.file_url}`}>Download presentation</a> : null}
      </div>
      {result?.metadata?.slides ? (
        <div className="grid gap-3 md:grid-cols-2">
          {result.metadata.slides.map((slide) => (
            <div className="panel p-4" key={slide.title}>
              <h2 className="font-semibold">{slide.title}</h2>
              <ul className="mt-2 list-disc pl-5 text-sm text-slate-600">
                {(slide.bullets || []).map((item) => <li key={item}>{item}</li>)}
              </ul>
            </div>
          ))}
        </div>
      ) : null}
      {result?.content ? <pre className="panel whitespace-pre-wrap p-4 text-sm">{result.content}</pre> : null}
    </section>
  );
}
