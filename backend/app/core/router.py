class AgentRouter:
    """
    Routes tasks to the correct agent based on task type.
    """

    def __init__(self):
        self.routes = {}

    def register(self, task_type, agent):
        self.routes[task_type] = agent

    def route(self, task_type, user_input, context=None):
        agent = self.routes.get(task_type)

        if not agent:
            return {
                "status": "error",
                "message": f"No agent found for task type: {task_type}"
            }

        return agent.run(user_input, context)
