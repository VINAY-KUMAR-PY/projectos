"use client";

import { useCallback, useEffect, useState } from "react";
import { marketplaceApi } from "@/lib/api";

type Item = { id: number; title: string; description?: string; item_type: string; price_inr: number };

export default function MarketplacePage() {
  const [items, setItems] = useState<Item[]>([]);
  const [search, setSearch] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    try {
      const response = await marketplaceApi.list(search);
      setItems(response.data.items);
    } catch {
      setError("Could not load marketplace items.");
    }
  }, [search]);

  useEffect(() => {
    load();
  }, [load]);

  async function handleUseItem(id: number) {
    try {
      const response = await marketplaceApi.use(id);
      setMessage(`Created project ${response.data.project_id}`);
    } catch {
      setError("Could not use this item. Check project limits or login state.");
    }
  }

  return (
    <section className="space-y-4">
      <div className="panel p-5">
        <div className="flex gap-2">
          <input className="min-w-0 flex-1 rounded-md border p-2 text-sm" placeholder="Search templates, prompts, workflows" value={search} onChange={(event) => setSearch(event.target.value)} />
          <button className="rounded-md bg-brand px-4 py-2 text-sm text-white" onClick={load}>Search</button>
        </div>
        {message ? <p className="mt-3 text-sm text-green-700">{message}</p> : null}
        {error ? <p className="mt-3 text-sm text-red-600">{error}</p> : null}
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {items.map((item) => (
          <article className="panel p-4" key={item.id}>
            <p className="text-xs uppercase text-slate-500">{item.item_type}</p>
            <h2 className="mt-1 font-semibold">{item.title}</h2>
            <p className="mt-2 min-h-12 text-sm text-slate-600">{item.description || "No description"}</p>
            <div className="mt-4 flex items-center justify-between">
              <span className="text-sm font-medium">INR {item.price_inr}</span>
              <button className="rounded-md border px-3 py-2 text-sm" onClick={() => handleUseItem(item.id)}>Use</button>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
