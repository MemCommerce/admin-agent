from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from agents import gen_trace_id, trace
from agents.mcp import MCPServerStreamableHttp

from schemas import ChatRequest, ChatResponse
from admin_agent import process_message

app = FastAPI()


@app.post("/chat", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def post_chat_message(chat_req: ChatRequest):
    async with MCPServerStreamableHttp(
        name="Streamable MCP Admin server",
        params={
            "url": "http://localhost:8000/mcp",
        },
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="Admin Agent workflow", trace_id=trace_id):
            print(
                f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n"
            )
            resp = await process_message(server, chat_req)
            return resp


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
