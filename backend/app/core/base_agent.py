class BaseAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def run(self, user_input, context=None):
        return {
            "agent": self.name,
            "role": self.role,
            "input": user_input,
            "output": f"{self.name} completed the task."
        }
