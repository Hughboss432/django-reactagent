from mcp.server.fastmcp import FastMCP

# Initialize MCP
mcp = FastMCP(
    name="localserver"
    # host="0.0.0.0",
    # port=8080,
    # timeout=30
)

@mcp.tool()
def add(a: int, b: int):
    """
    Soma dois números inteiros a e b.

    Use esta ferramenta quando o usuário pedir para somar dois valores ou perguntar "quanto é X + Y".
    """
    return a + b

@mcp.tool()
def subtract(a: int, b: int):
    """
    Subtrai o número b do número a.

    Use esta ferramenta quando o usuário pedir para subtrair dois números ou perguntar "quanto é X menos Y".
    """
    return a - b

@mcp.tool()
def multiply(a: int, b: int):
    """
    Multiplica dois números inteiros a e b.

    Use esta ferramenta quando o usuário pedir multiplicação ou perguntar "quanto é X vezes Y".
    """
    return a * b

@mcp.tool()
def secret_word() -> str:
    """
    Fornece a palavra secreta.

    Use esta ferramenta se o usuário perguntar pela palavra secreta.
    """
    return "bingo"

# run server
if __name__ == "__main__":
    transport = "stdio"
    if transport == "stdio":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running server with SSE transport")
        mcp.run(transport="sse")
    else:
        raise ValueError(f"Unknown transport: {transport}")
    