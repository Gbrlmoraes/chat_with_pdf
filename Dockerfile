# Use a imagem base do Python
FROM python:3.12-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo de requisitos e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código do app
COPY . .

# Exponha a porta que o Streamlit vai usar
EXPOSE 8501

ENV PORT 8501

# Comando para iniciar o app
CMD ["streamlit", "run", "chat_with_pdf.py", "--server.port=8501", "--server.address=0.0.0.0"]