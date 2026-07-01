const plans = [
  ["Free", "0", "2", "10", "10MB"],
  ["Student", "299", "5", "50", "50MB"],
  ["Pro", "499", "20", "200", "200MB"],
  ["Team", "999", "Unlimited", "Unlimited", "1GB"],
  ["Enterprise", "4999", "Unlimited", "Unlimited", "10GB"]
];

export default function SubscriptionPage() {
  return (
    <div className="grid gap-3 md:grid-cols-5">
      {plans.map(([name, price, projects, runs, upload]) => (
        <div className="panel p-4" key={name}>
          <h2 className="font-semibold">{name}</h2>
          <div className="mt-2 text-2xl">INR {price}</div>
          <div className="mt-4 text-sm text-slate-600">Projects: {projects}</div>
          <div className="text-sm text-slate-600">Agent runs: {runs}</div>
          <div className="text-sm text-slate-600">Upload: {upload}</div>
          <button className="mt-4 w-full rounded-md border px-3 py-2">Upgrade</button>
        </div>
      ))}
    </div>
  );
}
