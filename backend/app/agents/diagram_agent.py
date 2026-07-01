from app.core.base_agent import BaseAgent


class DiagramAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Diagram Agent",
            role="Generate Mermaid diagrams for software projects.",
            system_prompt=(
                "You generate valid Mermaid.js syntax for use case, ER, class, sequence, "
                "flowchart, architecture, and Gantt diagrams. Return labeled Mermaid blocks."
            ),
        )

    def run(self, user_input, context=None):
        output = self.call_ai(user_input, context)
        return self.standard_response(user_input, output, {"mermaid": output}, ["Render diagrams", "Validate Mermaid syntax"])
