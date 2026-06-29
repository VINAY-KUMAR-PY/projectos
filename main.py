from agents.project_manager_agent import ProjectManagerAgent

def main():
    print("Welcome to ProjectOS AI Agents")
    print("--------------------------------")

    user_input = input("Enter your project idea: ")

    manager = ProjectManagerAgent()
    result = manager.run(user_input)

    print("\nResult:")
    print(result)

if __name__ == "__main__":
    main()