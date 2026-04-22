import os
from langchain.agents import create_agent
from src.tools import (
    code_analysis_tool,
    pattern_detection_tool,
    pattern_recommendation_tool,
    code_generation_tool,
    evaluation_tool
)
from typing import cast
from langchain_core.language_models.chat_models import BaseChatModel
from dotenv import load_dotenv

from src.llm import get_llm

load_dotenv()


class Orchestrator:
    def __init__(self):
        self.tools = [
            code_analysis_tool,
            pattern_detection_tool,
            pattern_recommendation_tool,
            code_generation_tool,
            evaluation_tool
        ]

        prompt_path = os.path.join(
            os.path.dirname(__file__), "system_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            system_instruction = f.read()

        self.model = get_llm()

        self.agent = create_agent(
            model=cast(BaseChatModel, self.model), tools=self.tools, system_prompt=system_instruction)

    def invoke(self, user_prompt: str) -> tuple[str, str]:
        result = self.agent.invoke(
            {"messages": [
                {"role": "user", "content": user_prompt}
            ]}
        )
        last_message = result["messages"][-1]
        model_name = last_message.response_metadata.get(
            "model_name", "unknown")
        return last_message.content, model_name
