from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from .nodes_logic import model_node, should_continue, AgentState

def create_graph_with_tools(tools):
    graph = StateGraph(AgentState)
    tool_node = ToolNode(tools)
    graph.add_node("our_agent", model_node)
    graph.add_node("tools_node", tool_node)
    
    graph.add_conditional_edges(
        "our_agent",
        should_continue,
        {
            "continue": "tools_node",
            "end": END,
        },
    )

    graph.set_entry_point("our_agent")
    graph.add_edge("tools_node", "our_agent")
    return graph.compile()

