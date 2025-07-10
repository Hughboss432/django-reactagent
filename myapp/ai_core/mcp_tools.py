from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_ollama import ChatOllama
from .graph_logic import create_graph_with_tools
import re

async def connect_to_server(user_input,mcp_path='./myapp/mcp/server_local1.py',ollama_model='qwen3'):
    server_params = StdioServerParameters(
        command="python",
        args=[mcp_path],  # Path for MCP local server
    )
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # tools_result = await session.list_tools()
                # print("Available tools:")
                # for tool in tools_result.tools:
                #     print(f"  - {tool.name}: {tool.description}")

                tools = await load_mcp_tools(session)
                model = ChatOllama(model=ollama_model).bind_tools(tools)
                app = create_graph_with_tools(tools)

                inputs = {
                "messages": user_input,
                "model": model,
                "tools": tools,
                "session": session,
                }
                async for state in app.astream(inputs, stream_mode="values"):
                    msgs = state.get("messages", [])
                    if not msgs:
                        continue
                    last = msgs[-1]
                    if getattr(last, "tool_calls", None) or not last.content.strip():
                        #print("🤖 → pediu tool:", last.tool_calls[0]["name"])
                        continue
                    final_result = last.content
            final_result = re.sub(r"<think>.*?</think>", "", final_result, flags=re.DOTALL).strip()
            return final_result
    except Exception as e:
        print(f"Error connecting to MCP: {e}")
        raise