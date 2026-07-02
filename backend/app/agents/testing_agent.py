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
        scorecard = _score_project(user_input, output, context or {})
        return self.standard_response(
            user_input,
            output,
            {"test_plan_markdown": output, "scorecard": scorecard},
            ["Implement tests", "Run security scan", "Improve documentation"],
        )


def _score_project(user_input: str, output: str, context: dict) -> dict:
    context_text = " ".join(str(value or "") for value in context.values())
    combined = f"{user_input}\n{output}\n{context_text}".lower()
    memory_size = len(str(context.get("memory") or ""))
    description_size = len(str(context.get("description") or ""))
    output_size = len(output)
    risk_penalty = 12 if any(term in combined for term in ["secret", "password =", "api_key", "eval("]) else 0
    test_signal = sum(term in combined for term in ["test", "pytest", "edge case", "integration"])
    docs_signal = sum(term in combined for term in ["documentation", "readme", "report", "setup"])
    presentation_signal = sum(term in combined for term in ["presentation", "demo", "viva", "slide"])
    code_quality = _bounded(48 + min(18, output_size // 120) + min(12, memory_size // 150) - risk_penalty)
    documentation_completeness = _bounded(42 + min(18, description_size // 80) + docs_signal * 7 + min(12, memory_size // 200))
    testing_coverage = _bounded(38 + test_signal * 9 + min(18, output_size // 180))
    presentation_readiness = _bounded(36 + presentation_signal * 10 + min(16, description_size // 100))
    project_improvement_score = _bounded(
        round((code_quality + documentation_completeness + testing_coverage + presentation_readiness) / 4)
    )
    return {
        "code_quality": code_quality,
        "documentation_completeness": documentation_completeness,
        "testing_coverage": testing_coverage,
        "presentation_readiness": presentation_readiness,
        "project_improvement_score": project_improvement_score,
    }


def _bounded(value: int | float) -> int:
    return max(0, min(100, int(round(value))))
