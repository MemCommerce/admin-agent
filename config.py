from os import getenv

from dotenv import load_dotenv


load_dotenv()

ADMIN_MCP_URL = getenv("ADMIN_MCP_URL", "http://localhost:8000/mcp")