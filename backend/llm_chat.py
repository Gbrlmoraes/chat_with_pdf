from langchain_google_vertexai import ChatVertexAI
from langchain_pinecone import PineconeVectorStore
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from typing import List, Dict, Any
from dotenv import load_dotenv
import os

load_dotenv()


def llm_chat(prompt_usuario: str, historico_chat: List[Dict[str, Any]] = []):

    # Definindo o sistema de embeddings, a vector store e qual llm usaremos
    embeddings = VertexAIEmbeddings(model_name="text-multilingual-embedding-002")
    vectorstore = PineconeVectorStore(
        index_name=os.environ.get("INDEX_NAME"), embedding=embeddings
    )
    llm = ChatVertexAI(model="gemini-1.5-flash", temperature=0, max_retries=0)

    # Prompt que adicionará o contexto dos documentos
    TEMPLATE_PROMPT_DOC = """
    Responda qualquer pergunta do usuário utilizando APENAS o contexto abaixo:

    <context>
    {context}
    </context>

    Usuário:
    {input}
    """
    prompt_doc = PromptTemplate(
        template=TEMPLATE_PROMPT_DOC, input_variables=["context", "input"]
    )

    # Criando chain de contexto de documentos
    chain_documentos = create_stuff_documents_chain(llm=llm, prompt=prompt_doc)

    # Prompt que recebe o contexto do histórico do chat
    TEMPLATE_PROMPT_HISTORICO = """
    Tendo como base a seguinte conversa e a nova pergunta, reformule a nova pergunta para ser uma pergunta independente.

    Histórico do Chat:
    {chat_history}
    Nova Pergunta: {input}
    Pergunta Inpendente:
    """
    prompt_historico = PromptTemplate(
        template=TEMPLATE_PROMPT_HISTORICO, input_variables=["chat_history", "input"]
    )

    # Retriever ciente do histórico do chat
    retriever_historico = create_history_aware_retriever(
        llm=llm, retriever=vectorstore.as_retriever(), prompt=prompt_historico
    )

    # Criando chain final de perguntas e respostas, ciente do histórico de chat e do contexto dos documentos
    chain_final = create_retrieval_chain(
        retriever=retriever_historico, combine_docs_chain=chain_documentos
    )

    result = chain_final.invoke(
        input={"input": prompt_usuario, "chat_history": historico_chat}
    )
    return result


if __name__ == "__main__":

    llm_res = llm_chat("Quais os tipos de energia existentes?")
    print(llm_res["answer"])
