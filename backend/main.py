from agents.project_manager_agent import ProjectManagerAgent
from utils.logger import app_logger


def main():
    app_logger.info("ProjectOS Started")

    print("Welcome to ProjectOS AI Agents")
    print("--------------------------------")

    user_input = input("Enter your project idea: ")

    manager = ProjectManagerAgent()

    result = manager.run(user_input)

    app_logger.info("Project created successfully")

    print("\nResult:")
    print(result)


if __name__ == "__main__":
    main()