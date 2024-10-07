# Use a imagem base do Python 3.12 em Alpine
FROM python:3.12.7-alpine3.20

WORKDIR /app

# Copia o arquivo de requisitos e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do app
COPY . .

EXPOSE 8501

ENV PORT=8501

# Comando para iniciar o app
CMD ["streamlit", "run", "chat_with_pdf.py", "--server.port=8501", "--server.address=0.0.0.0"]