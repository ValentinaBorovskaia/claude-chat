from .client import ClaudeClient
from .models import ChatHistory

def main():
    client = ClaudeClient()
    history = ChatHistory()
    system_prompt = "You are a helpful assistant. Answer concisely."

    print("🤖 Claude Chat")
    print("Commands: 'exit' — quit, 'clear' — reset history")
    print("-" * 40)

    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue
        if user_input.lower() == "exit":
            print("Bye!")
            break
        if user_input.lower() == "clear":
            history = ChatHistory()
            print("History cleared.")
            continue

        history.add("user", user_input)

        print("\nClaude: ", end="")
        response = client.send_streaming(history, system_prompt)

        history.add("assistant", response)

if __name__ == "__main__":
    main()