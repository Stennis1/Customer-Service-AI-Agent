import os
from typing import List

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from api_tools import APITools
from knowledge_base import KnowledgeBase

load_dotenv()


class CustomerServiceAgent:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL", "openai:gpt-4o-mini")
        self.history_window = int(os.getenv("MAX_HISTORY_MESSAGES", "20"))

        self.knowledge_base = self._init_knowledge_base()
        self.api_tools = self._init_api_tools()

        self.agent = create_agent(
            model=self.model,
            tools=self._create_tools(),
            system_prompt=self._get_system_prompt(),
        )
        self.chat_history: List[BaseMessage] = []

    def _create_tools(self):
        """Define tools available to the agent."""
        return [
            self.search_knowledge_base,
            self.escalate_to_human,
            self.check_order_status,
        ]

    def _init_knowledge_base(self):
        """Initialize the vector knowledge base with safe fallback."""
        try:
            return KnowledgeBase(data_path="./knowledge", persist_directory="./chromadb")
        except Exception:
            return None

    def _init_api_tools(self):
        """Initialize API tools if required env vars are provided."""
        base_url = os.getenv("CUSTOMER_API_BASE_URL", "").strip()
        api_key = os.getenv("CUSTOMER_API_KEY", "").strip()

        if not base_url or not api_key:
            return None

        return APITools(base_url=base_url, api_key=api_key)

    def _get_system_prompt(self) -> str:
        return """You are a helpful customer service agent for Adillis Edu.
Your role is to assist customers professionally and efficiently.

Guidelines:
- Always be polite and empathetic
- Use available tools to find accurate information
- If you cannot resolve an issue, escalate to a human agent
- Keep responses concise but informative
- Ask clarifying questions when needed
"""

    def _extract_assistant_text(self, messages: List[BaseMessage]) -> str:
        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                content = msg.content
                if isinstance(content, str):
                    return content
                if isinstance(content, list):
                    parts = []
                    for item in content:
                        if isinstance(item, dict) and item.get("type") == "text":
                            parts.append(item.get("text", ""))
                    if parts:
                        return "\n".join(parts).strip()
        return "I am sorry, I could not generate a response."

    def _trim_history(self, messages: List[BaseMessage]) -> List[BaseMessage]:
        if len(messages) <= self.history_window:
            return messages
        return messages[-self.history_window :]

    def search_knowledge_base(self, query: str) -> str:
        """Search the company knowledge base for information relevant to the customer question."""
        if self.knowledge_base is None:
            return (
                "Knowledge base is unavailable right now. "
                "Please verify OPENAI_API_KEY and local knowledge files."
            )
        return self.knowledge_base.search(query=query, k=3)

    def escalate_to_human(self, reason: str) -> str:
        """Escalate complex issues to a human support agent when automation is insufficient."""
        return (
            "I'm transferring you to a human agent who can better assist with: "
            f"{reason}. Please hold while I connect you."
        )

    def check_order_status(self, order_id: str) -> str:
        """Check the status of a customer order by order ID."""
        if self.api_tools is not None:
            return self.api_tools.check_order_status(order_id)

        if order_id.startswith("ORD"):
            return (
                f"Order {order_id} is currently being processed and will ship "
                "within 2 business days."
            )
        return "Please provide a valid order ID starting with 'ORD'."

    def chat(self, message: str) -> str:
        """Process a user message and return the agent response."""
        try:
            incoming = [*self.chat_history, HumanMessage(content=message)]
            result = self.agent.invoke({"messages": incoming})
            output_messages = result.get("messages", incoming)
            self.chat_history = self._trim_history(output_messages)
            return self._extract_assistant_text(output_messages)
        except Exception as exc:
            return (
                "I'm sorry, I encountered an error: "
                f"{str(exc)}. Let me escalate this to a human agent."
            )


if __name__ == "__main__":
    agent = CustomerServiceAgent()

    print("Customer Service Agent initialized!")
    print("Type 'quit' to exit\n")

    while True:
        user_input = input("Customer: ")
        if user_input.lower() == "quit":
            break

        response = agent.chat(user_input)
        print(f"Agent: {response}\n")
