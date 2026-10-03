from agent import run_agent


def main():
    print("Self-Learning AI Agent")
    print("Type 'exit' to quit.\n")

    while True:
        task = input("You: ").strip()
        if task.lower() == "exit":
            print("Goodbye!")
            break
        if not task:
            continue
        run_agent(task)


if __name__ == "__main__":
    main()
