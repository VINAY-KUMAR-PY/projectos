from app.core.base_agent import BaseAgent


class CodingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Coding Agent",
            role="Generate source code, README, setup steps, and code review guidance.",
            system_prompt=(
                "You are a senior coding assistant. Generate practical module-by-module "
                "code plans, file structures, README content, setup instructions, bug fixes, "
                "code explanations, review notes, and multi-file scaffolds. Respect any "
                "language/framework in context and return a clear file tree when code is requested."
            ),
        )

    def run(self, user_input, context=None):
        output = self.call_ai(user_input, context)
        file_tree = [
            {"path": "README.md", "purpose": "Project setup and overview"},
            {"path": "src/main.py", "purpose": "Application entry point"},
            {"path": "tests/test_main.py", "purpose": "Smoke test scaffold"},
        ]
        return self.standard_response(
            user_input,
            output,
            {"code_plan_markdown": output, "file_tree": file_tree},
            ["Generate files", "Review generated code", "Run tests"],
        )
