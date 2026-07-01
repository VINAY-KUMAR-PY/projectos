from app.core.base_agent import BaseAgent


class TestingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Testing Agent",
            role="Generate test plans, edge cases, quality checklists, security and performance checks.",
            system_prompt=(
                "You are a QA lead. Generate unit tests, integration tests, edge cases, "
                "test plan, quality checklist, security checks, performance benchmarks, "
                "grammar feedback, rubric scores, and plagiarism-risk heuristics."
            ),
        )

    def run(self, user_input, context=None):
        output = self.call_ai(user_input, context)
        scorecard = {
            "code_quality": 80,
            "documentation_completeness": 78,
            "testing_coverage": 70,
            "presentation_readiness": 76,
            "project_improvement_score": 77,
        }
        return self.standard_response(
            user_input,
            output,
            {"test_plan_markdown": output, "scorecard": scorecard},
            ["Implement tests", "Run security scan", "Improve documentation"],
        )
