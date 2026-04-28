from src.orchestrator import Orchestrator
import os
import sys
import time
import uuid
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool

# Ensure 'src' is in PYTHONPATH for cross-module imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


app = FastAPI()
orchestrator = None


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str | None = None
    messages: list[ChatMessage] = Field(default_factory=list)
    temperature: float | None = None
    stream: bool = False


@app.post("/v1/chat/completions")
async def chat_completions(payload: ChatCompletionRequest) -> dict[str, Any]:
    global orchestrator
    if orchestrator is None:
        orchestrator = Orchestrator()
    prompt = _build_prompt(payload.messages)
    final_output, used_model = await run_in_threadpool(orchestrator.invoke, prompt)

    return {
        "id": f"chatcmpl-{uuid.uuid4().hex}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": used_model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": final_output,
                },
                "finish_reason": "stop",
            }
        ],
    }


@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "custom-agent",
                "object": "model",
                "owned_by": "you"
            }
        ]
    }


def _build_prompt(messages: list[ChatMessage]) -> str:
    if not messages:
        return ""

    parts: list[str] = []
    for message in messages:
        parts.append(f"{message.role.upper()}: {message.content}")
    return "\n\n".join(parts)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False)
