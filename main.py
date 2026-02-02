from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from pathlib import Path
import os

# BASE_DIR = Path(__file__).resolve().parent
# load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)
load_dotenv(".env")
from agent import build_agent

print("OPENAI_API_KEY exists:", bool(os.getenv("OPENAI_API_KEY")))



def main():
    executor, first_message = build_agent()

    chat_history = []

    # agente fala primeiro
    print(first_message)
    chat_history.append(AIMessage(content=first_message))

    while True:
        user_input = input("> ")

        if user_input.lower() in ("exit", "quit"):
            break

        result = executor.invoke(
            {"messages": chat_history + [HumanMessage(content=user_input)]}
        )

        last = result["messages"][-1]
        print(last.content)

        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(last)


if __name__ == "__main__":
    main()
