from app.core.base_agent import BaseAgent


class FileVideoAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="File and Video Intelligence Agent",
            role="Analyze uploaded files and video-derived transcripts.",
            system_prompt=(
                "You analyze uploaded content. Extract key points, summary, action items, "
                "questions answered, topics covered, video transcript summary, frame observations, mistakes, and improvements."
            ),
        )

    def run(self, user_input, context=None):
        output = self.call_ai(user_input, context)
        data = {
            "analysis_markdown": output,
            "summary": output[:500],
            "action_items": ["Save extracted insights", "Create follow-up tasks"],
            "mistakes": ["Review manually when real frame analysis is enabled"],
            "viva_questions": [
                "What is the main idea in this file or video?",
                "Which evidence supports the project outcome?",
                "What would you improve before final submission?",
            ],
        }
        return self.standard_response(user_input, output, data, ["Save summary", "Create follow-up tasks"])
