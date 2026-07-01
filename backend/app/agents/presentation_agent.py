from app.core.base_agent import BaseAgent


class PresentationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Presentation Agent",
            role="Generate slide outlines, speaker notes, visuals, and demo scripts.",
            system_prompt=(
                "You create professional PPT outlines: Title, Problem, Solution, Features, "
                "Architecture, Demo, Tech Stack, Results, Conclusion, and Q&A with speaker notes."
            ),
        )

    def run(self, user_input, context=None):
        output = self.call_ai(user_input, context)
        return self.standard_response(user_input, output, {"presentation_markdown": output}, ["Create slides", "Practice demo"])
