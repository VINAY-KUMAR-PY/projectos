export default function TasksPage() {
  return <div className="grid gap-3 md:grid-cols-3">{["todo", "doing", "done"].map((col) => <div className="panel min-h-64 p-4 capitalize" key={col}>{col}</div>)}</div>;
}
