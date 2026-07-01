from app.core.base_agent import BaseAgent


class DeploymentAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Deployment Agent",
            role="Generate deployment instructions for local, Docker, Vercel, Railway/Render, migrations, and monitoring.",
            system_prompt=(
                "You are a DevOps engineer. Produce deployment steps, environment variables, "
                "Docker setup, frontend/backend deployment, database migration, and monitoring guidance."
            ),
        )

    def run(self, user_input, context=None):
        output = self.call_ai(user_input, context)
        return self.standard_response(user_input, output, {"deployment_markdown": output}, ["Create env vars", "Deploy staging"])
