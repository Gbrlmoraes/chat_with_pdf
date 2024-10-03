from langchain_google_vertexai import ChatVertexAI
from langchain_pinecone import PineconeVectorStore
from langchain_google_vertexai import VertexAIEmbeddings
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

    


if __name__ == "__main__":

    llm = ChatVertexAI(model="gemini-1.5-flash", temperature=0, max_retries=0)

    llm_res = llm.invoke("Olá Gemini!")
    print(llm_res.content)
