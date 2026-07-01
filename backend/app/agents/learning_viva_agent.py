from app.core.base_agent import BaseAgent


class LearningVivaAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Learning and Viva Agent",
            role="Generate viva questions, answers, quizzes, interview prep, and project explanation scripts.",
            system_prompt=(
                "You are an academic mentor. Generate likely viva questions with ideal answers, "
                "concept explanations, quiz questions, interview questions, and a 5-minute explanation script."
            ),
        )

    def run(self, user_input, context=None):
        output = self.call_ai(user_input, context)
        return self.standard_response(user_input, output, {"learning_markdown": output}, ["Practice Q&A", "Refine explanation"])
