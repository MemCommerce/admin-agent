from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from agents import gen_trace_id, trace
from agents.mcp import MCPServerStreamableHttp

from schemas import ChatRequest, ChatResponse, DescriptionReq
from admin_agent import process_message
from create_description import create_ai_description
from config import ADMIN_MCP_URL

app = FastAPI()


@app.post("/chat", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def post_chat_message(chat_req: ChatRequest):
    async with MCPServerStreamableHttp(
        name="Streamable MCP Admin server",
        params={
            "url": ADMIN_MCP_URL,
        },
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="Admin Agent workflow", trace_id=trace_id):
            print(
                f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n"
            )
            resp = await process_message(server, chat_req)
            return resp


@app.post(
    "/product-description", response_model=str, status_code=status.HTTP_201_CREATED
)
async def post_product_description(product_details: DescriptionReq):
    new_description = await create_ai_description(product_details)
    return new_description


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
