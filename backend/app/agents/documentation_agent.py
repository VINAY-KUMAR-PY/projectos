from app.core.base_agent import BaseAgent


class DocumentationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Documentation Agent",
            role="Generate academic and professional documentation in Markdown.",
            system_prompt=(
                "You write complete project documentation with Abstract, Introduction, "
                "Problem Statement, Literature Review, Methodology, System Design, Testing, "
                "Results, Conclusion, Future Scope, and References."
            ),
        )

    def run(self, user_input, context=None):
        output = self.call_ai(user_input, context)
        return self.standard_response(user_input, output, {"documentation_markdown": output}, ["Export docs", "Review references"])
