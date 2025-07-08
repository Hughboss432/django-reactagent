from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_ollama import ChatOllama
from .graph_logic import create_graph_with_tools


async def connect_to_server(user_input):
    server_params = StdioServerParameters(
        command="python",
        args=["./myapp/mcp/server_local.py"],  # Caminho para servidor MCP
    )
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # teste das ferramentas na sessão
                # tools_result = await session.list_tools()
                # print("Available tools:")
                # for tool in tools_result.tools:
                #     print(f"  - {tool.name}: {tool.description}")

                tools = await load_mcp_tools(session)
                model = ChatOllama(model="qwen3").bind_tools(tools)
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
            return final_result
    except Exception as e:
        print(f"Erro ao conectar com MCP: {e}")
        raise