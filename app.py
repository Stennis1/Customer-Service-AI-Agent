from agent import CustomerServiceAgent


def main():
    agent = CustomerServiceAgent()

    print("Customer Service Agent initialized!")
    print("Type 'quit' to exit\n")

    while True:
        user_input = input("Customer: ")
        if user_input.strip().lower() == "quit":
            break

        response = agent.chat(user_input)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    main()
