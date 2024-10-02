from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_google_vertexai import VertexAIEmbeddings
import os


def carrega_embeddings(caminho_arquivo: str):
    """
    Função responsável por receber o arquivo em PDF, separar o texto, gerar os embeddings e carregalos para a vector store
    Args:
    - caminho_arquivo: local onde o arquivo se encontra.
    """

    print("Lendo arquivo...")
    loader = PyPDFLoader(file_path=caminho_arquivo)
    documents = loader.load()

    print("Separando texto...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents=documents)
    print(f"- Foram criados {len(docs)} chunks!")

    print("Gerando e carregando embeddings...")
    embeddings = VertexAIEmbeddings(model_name="text-multilingual-embedding-002")
    PineconeVectorStore.from_documents(
        docs, embeddings, index_name=os.environ.get("INDEX_NAME")
    )

    print("Carregamento concluído!")


if __name__ == "__main__":
    carrega_embeddings(
        caminho_arquivo="/home/gbrlmoraes/git_reps/chat_with_pdf/sample_pdfs/regras_pokemon_tcg.pdf"
    )
