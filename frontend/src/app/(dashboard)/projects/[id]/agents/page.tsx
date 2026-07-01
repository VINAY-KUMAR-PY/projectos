import { AgentPanel } from "@/components/agents/AgentPanel";

export default function AgentsPage({ params }: { params: { id: string } }) {
  return <AgentPanel projectId={Number(params.id)} />;
}
