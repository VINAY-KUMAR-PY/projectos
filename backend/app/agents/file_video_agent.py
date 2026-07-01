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
        return self.standard_response(user_input, output, {"analysis_markdown": output}, ["Save summary", "Create follow-up tasks"])
