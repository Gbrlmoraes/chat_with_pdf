# chat_with_pdf
Converse com documentos em PDF por meio de um Agente de IA

<p align="center">
<img src="http://img.shields.io/static/v1?label=STATUS&message=Em Desenvolvimento&color=YELLOW&style=for-the-badge"/>
</p>

Fontes:
https://cloud.google.com/blog/products/ai-machine-learning/rag-with-bigquery-and-langchain-in-cloud
https://python.langchain.com/docs/integrations/text_embedding/google_vertex_ai_palm/
https://python.langchain.com/docs/integrations/chat/google_vertex_ai_palm/


Deploy:

0:
```bash
set -o allexport
source .env
set +o allexport
```

1:
```bash
git clone https://github.com/Gbrlmoraes/chat_with_pdf.git
```

2:
```bash
docker build -t chat-with-pdf .
docker run -p 8501:8501 chat-with-pdf
```

3:
```bash
gcloud auth login
```

4:
```bash
gcloud config set project $GCP_PROJECT_ID
```

5:
```bash
export IMAGE_NAME=chat-with-pdf
gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/$IMAGE_NAME
```

6:
```bash
export SERVICE_NAME=chat-with-pdf
export GCP_REGION=us-central1
gcloud run deploy $SERVICE_NAME \
--image gcr.io/$GCP_PROJECT_ID/$IMAGE_NAME \
--set-env-vars INDEX_NAME=$INDEX_NAME,PINECONE_API_KEY=$PINECONE_API_KEY,LANGCHAIN_TRACING_V2=$LANGCHAIN_TRACING_V2,LANGCHAIN_API_KEY=$LANGCHAIN_API_KEY,LANGCHAIN_PROJECT=$LANGCHAIN_PROJECT,LANGCHAIN_ENDPOINT=$LANGCHAIN_ENDPOINT \
--platform managed \
--region $GCP_REGION \
--port 8501 \
--allow-unauthenticated
```
