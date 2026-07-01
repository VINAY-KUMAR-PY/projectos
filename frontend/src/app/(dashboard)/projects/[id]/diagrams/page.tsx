"use client";

import mermaid from "mermaid";
import { useEffect, useState } from "react";
import { generationApi } from "@/lib/api";

const types = ["usecase", "er", "class", "sequence", "flowchart", "architecture", "schema", "gantt"];

export default function DiagramsPage({ params }: { params: { id: string } }) {
  const projectId = Number(params.id);
  const [diagramType, setDiagramType] = useState("architecture");
  const [content, setContent] = useState("");
  const [svg, setSvg] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    mermaid.initialize({ startOnLoad: false, securityLevel: "strict" });
  }, []);

  async function generate() {
    setLoading(true);
    setError("");
    try {
      const response = await generationApi.diagram(projectId, diagramType);
      const source = response.data.content as string;
      setContent(source);
      const rendered = await mermaid.render(`diagram-${Date.now()}`, source);
      setSvg(rendered.svg);
    } catch {
      setError("Could not generate or render diagram.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="space-y-4">
      <div className="panel p-5">
        <div className="mb-3 flex flex-wrap items-center gap-3">
          <select className="rounded-md border p-2 text-sm" value={diagramType} onChange={(event) => setDiagramType(event.target.value)}>
            {types.map((item) => <option key={item}>{item}</option>)}
          </select>
          <button className="rounded-md bg-brand px-4 py-2 text-sm text-white disabled:opacity-60" onClick={generate} disabled={loading}>
            {loading ? "Generating..." : "Generate Diagram"}
          </button>
        </div>
        {error ? <p className="text-sm text-red-600">{error}</p> : null}
      </div>
      {svg ? <div className="panel overflow-auto p-4" dangerouslySetInnerHTML={{ __html: svg }} /> : null}
      {content ? <pre className="panel whitespace-pre-wrap p-4 text-sm">{content}</pre> : null}
    </section>
  );
}
