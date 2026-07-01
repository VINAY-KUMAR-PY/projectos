from app.core.base_agent import BaseAgent


class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Research Agent",
            role="Research comparable products, technologies, feasibility, datasets, APIs, papers, and risks.",
            system_prompt=(
                "You are a pragmatic research analyst for software projects. Provide "
                "similar tools, technical options, feasibility, risks, useful datasets/APIs, "
                "and credible reference directions without inventing citations."
            ),
        )

    def run(self, user_input, context=None):
        output = self.call_ai(user_input, context)
        return self.standard_response(user_input, output, {"research_markdown": output}, ["Validate sources", "Pick stack"])
