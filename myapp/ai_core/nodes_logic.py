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
        "Você é um agente de IA útil chamado LPhantom que responde em português de forma clara e tem à sua disposição ferramentas de automação em Python." \
        "**Apenas** chame uma ferramenta se o usuário pedir claramente para executar essa ação"
    )
    response = await state["model"].ainvoke([system_prompt] + state["messages"])
    return {
        "messages": state["messages"] + [response],
        "model": state["model"],  # manter os dados no estado
        "tools": state["tools"],
        "session": state["session"]
    }

async def should_continue(state: AgentState) -> str:
    messages = state["messages"]
    last_message = messages[-1]

    if isinstance(last_message, AIMessage) and getattr(last_message, "tool_calls", None):
        return "continue"
    return "end"

