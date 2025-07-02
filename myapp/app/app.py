import streamlit as st
import asyncio
from mcp_tools import connect_to_server
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(page_title="Agente com MCP", layout="centered")
st.title("🤖 LPhantom")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Digite algo...")

if user_input:
    async def run():
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        result = await connect_to_server(user_input)
        return result

    result = asyncio.run(run())

    # Atualiza histórico de chat
    st.session_state.chat_history.append(AIMessage(content=result))

    # salvando em txt o chat
    if user_input == "exit":
        with open("logging.txt", "w") as file:
            file.write("Your Conversation Log:\n")

            for message in st.session_state.chat_history:
                if isinstance(message, HumanMessage):
                    file.write(f"You: {message.content}\n")
                elif isinstance(message, AIMessage):
                    file.write(f"AI: {message.content}\n\n")
            file.write("End of Conversation")

for msg in st.session_state.chat_history:
    if hasattr(msg, "tool_calls") and msg.tool_calls:
        continue  # Ignora mensagens que chamam ferramentas
    else:
        st.chat_message(msg.type).write(msg.content)