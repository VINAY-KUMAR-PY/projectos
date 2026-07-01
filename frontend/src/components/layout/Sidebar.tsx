import Link from "next/link";

const items = [
  ["Dashboard", "/dashboard"],
  ["Projects", "/projects"],
  ["AI Chat", "/ai-chat"],
  ["Files", "/files"],
  ["Marketplace", "/marketplace"],
  ["Settings", "/settings"],
  ["Subscription", "/settings/subscription"]
];

export function Sidebar() {
  return (
    <aside className="hidden w-64 shrink-0 border-r border-slate-200 bg-white p-4 md:block">
      <div className="mb-6 text-xl font-semibold">ProjectOS</div>
      <nav className="space-y-1">
        {items.map(([label, href]) => (
          <Link className="block rounded-md px-3 py-2 text-sm hover:bg-slate-100" href={href} key={href}>
            {label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
