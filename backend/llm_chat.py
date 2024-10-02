from langchain_google_vertexai import ChatVertexAI
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    
    llm = ChatVertexAI(
        model='gemini-1.5-flash',
        temperature=0,
        max_retries=0
    )

    llm_res = llm.invoke('Olá Gemini!')
    print(llm_res.content)