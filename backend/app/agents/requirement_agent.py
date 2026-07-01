from app.core.base_agent import BaseAgent

class RequirementAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Requirement Analyzer Agent",
            role="Extract project requirements, features, and constraints.",
            system_prompt=(
                "You are a senior product analyst. Extract functional requirements, "
                "non-functional requirements, user stories, scope, constraints, tech "
                "recommendations, and acceptance criteria."
            ),
        )

    def run(self, user_input, context=None):
        output = self.call_ai(user_input, context)
        return self.standard_response(
            task=user_input,
            output=output,
            data={"requirements_markdown": output},
            next_steps=["Review scope", "Prioritize MVP", "Create architecture"],
        )
