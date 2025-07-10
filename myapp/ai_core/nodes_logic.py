from typing import Annotated, Sequence, TypedDict, Any
from langchain_core.messages import BaseMessage # The foundational class for all message types in LangGraph
from langchain_core.messages import SystemMessage # Message for providing instructions to the LLM
from langchain_core.messages import AIMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    model: Any
    tools: Any
    session: Any

async def model_node(state:AgentState) -> AgentState:
    system_prompt = SystemMessage(content=
        "You are a helpful AI agent named LightPhantom or Phantom who responds clearly and has Python automation tools at your disposal." \
        "**Only** call a tool if the user clearly asks it to perform that action."
    )
    response = await state["model"].ainvoke([system_prompt] + state["messages"])
    return {
        "messages": state["messages"] + [response],
        "model": state["model"],  
        "tools": state["tools"],
        "session": state["session"]
    }

async def should_continue(state: AgentState) -> str:
    messages = state["messages"]
    last_message = messages[-1]

    if isinstance(last_message, AIMessage) and getattr(last_message, "tool_calls", None):
        return "continue"
    return "end"

