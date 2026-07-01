from app.core.base_agent import BaseAgent


class DeploymentAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Deployment Agent",
            role="Generate deployment instructions for local, Docker, Vercel, Railway/Render, migrations, and monitoring.",
            system_prompt=(
                "You are a DevOps engineer. Produce deployment steps, environment variables, "
                "Docker setup, frontend/backend deployment, database migration, monitoring guidance, "
                "and ready-to-use config files for Vercel, Netlify, Render, Railway, AWS, Docker, and GitHub Pages."
            ),
        )

    def run(self, user_input, context=None):
        output = self.call_ai(user_input, context)
        configs = {
            "vercel.json": '{"buildCommand":"npm run build"}',
            "render.yaml": "services:\n  - type: web\n    env: python",
            "railway.json": '{"deploy":{"startCommand":"uvicorn app.api.server:app"}}',
        }
        return self.standard_response(
            user_input,
            output,
            {"deployment_markdown": output, "configs": configs},
            ["Create env vars", "Commit deploy configs", "Deploy staging"],
        )
