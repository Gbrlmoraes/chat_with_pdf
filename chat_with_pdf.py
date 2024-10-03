from backend.llm_chat import llm_chat
import streamlit as st

st.header("Conversando com um PDF! 📃")

# Define variáveis que receberão o histórico de mensagens do chat
if (
    "historico_prompts_usuario" not in st.session_state
    and "historico_respostas_llm" not in st.session_state
    and "historico_chat" not in st.session_state
):
    st.session_state["historico_prompts_usuario"] = []
    st.session_state["historico_respostas_llm"] = []
    st.session_state["historico_chat"] = []

# Mostra as mensagens existentes
for participante, mensagem in st.session_state["historico_chat"]:
    with st.chat_message(participante):
        st.markdown(mensagem)

# Interação usuário-llm
if prompt := st.chat_input("Faça uma pergunta"):

    # Mostra a pergunta do usuário
    with st.chat_message("human"):
        st.markdown(prompt)

    # Gera a resposta utilizando langchain
    resposta_llm = llm_chat(
        prompt_usuario=prompt, historico_chat=st.session_state["historico_chat"]
    )

    # resposta_llm = {"answer": f"O usuário disse {prompt}"}

    # Monstra a resposta no chat
    with st.chat_message("ai"):
        st.markdown(resposta_llm["answer"])

    # Guarda as variáveis da seção
    st.session_state["historico_prompts_usuario"].append(prompt)
    st.session_state["historico_respostas_llm"].append(resposta_llm["answer"])

    st.session_state["historico_chat"].append(("human", prompt))
    st.session_state["historico_chat"].append(("ai", resposta_llm["answer"]))
