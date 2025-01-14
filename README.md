# Chat With PDF
_Converse com documentos em PDF por meio de um Agente de IA!_
[Link para o projeto](https://chat-with-pdf-851464781998.us-central1.run.app)

---

## Arquitetura do projeto
---
![arquitetura](https://github.com/user-attachments/assets/dd0ab7fb-b406-4c44-b203-242d39dbec38)

## Estrutura do repositório
```bash
├── .github/workflows            # Diretório com o workflow do projeto
│   └── deploy_gcp.yml           # Workflow que deploy automático para o GCP
├── backend                      # Diretório com scripts em Python das funções
│   ├── __init__.py              # Arquivo de inicialização do pacote
│   ├── ingestao.py              # Arquivo com a função que transforma o PDF em embeddings e carrega para o banco vetorial Pinecone
│   └── llm_chat.py              # Arquivo com a função principal de comunicação com a LLM
├── sample_pdfs                  # Diretório com os arquivos em PDF usados na DEMO
│   └── regras_pokemon_tcg.pdf   # Arquivo com as regras do jogo Pokémon TCG
├── .dockerignore                # Arquivo que ignora pastas carregadas para a imagem Docker
├── .gitignore                   # Arquivo que ignora pastas carregadas para o repositório
├── Dockerfile                   # Arquivo Docker de construção da imagem
├── Pipfile                      # Arquivo com os pacotes Python necessários para o projeto (Pipenv)
├── README.md                    # Arquivo de documentação do repositório
├── chat_with_pdf.py             # Arquivo Python principal do projeto
└── requirements.txt             # Arquivo com os pacotes Python necessários para o projeto (pip)
```
---

## Implantação
_Os passos da instalação foram feitos com um sistema linux em mente, mas é simples alterar os comandos para reproduzir no Windows_

### Requisitos
- Ferramentas e Serviços
  - __Conta na Google Cloud Platform:__ Conta necessária para acessar os serviços da GCP.
  - __Conta no Pinecone:__ Necessário para criação e gerenciamento de índices de embeddings.
  - __(OPCIONAL) Conta no LangSmith:__ Ferramenta opcional para monitoramento e rastreamento de interações em tempo real (usado para tracing e depuração).
    
- Variáveis de Ambiente
<table>
  <thead>
    <tr>
      <th>Variável</th>
      <th>Descrição</th>
      <th>Exemplo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>GCP_JSON_KEY</strong></td>
      <td>Caminho para o arquivo de chave JSON da conta de serviço GCP.</td>
      <td><code>/path/to/key.json</code></td>
    </tr>
    <tr>
      <td><strong>GCP_PROJECT_ID</strong></td>
      <td>ID do projeto dentro do Google Cloud Platform.</td>
      <td><code>my-gcp-project-id</code></td>
    </tr>
    <tr>
      <td><strong>INDEX_NAME</strong></td>
      <td>Nome do índice criado no Pinecone, onde os embeddings serão armazenados.</td>
      <td><code>my-index</code></td>
    </tr>
    <tr>
      <td><strong>PINECONE_API_KEY</strong></td>
      <td>Chave de API para acessar os serviços do Pinecone.</td>
      <td><code>your-pinecone-api-key</code></td>
    </tr>
    <tr>
      <td><strong>LANGCHAIN_API_KEY</strong> (Opcional)</td>
      <td>Chave de API para integrar com o LangSmith (somente se for utilizar tracking).</td>
      <td><code>your-langchain-api-key</code></td>
    </tr>
    <tr>
      <td><strong>LANGCHAIN_ENDPOINT</strong> (Opcional)</td>
      <td>URL do endpoint usado pelo LangSmith para rastreamento.</td>
      <td><code>https://api.langchain.com</code></td>
    </tr>
    <tr>
      <td><strong>LANGCHAIN_PROJECT</strong> (Opcional)</td>
      <td>Nome do projeto dentro do LangSmith, utilizado para organizar os dados rastreados.</td>
      <td><code>my-langchain-project</code></td>
    </tr>
    <tr>
      <td><strong>LANGCHAIN_TRACING_V2</strong> (Opcional)</td>
      <td>Define se o LangSmith será utilizado para acompanhar o projeto. Definir como <code>true</code> se quiser ativar o tracking.</td>
      <td><code>true</code> ou <code>false</code></td>
    </tr>
  </tbody>
</table>

<p><strong>Nota:</strong> As variáveis marcadas como "Opcional" só são necessárias se você planeja utilizar o LangSmith para monitorar a execução do projeto.</p>

### Passo a passo

#### Passo 1: Carregar variáveis de ambiente
Certifique-se de que você tenha suas variáveis de ambiente configuradas no arquivo `.env`. Em seguida, execute:

```bash
set -o allexport
source .env
set +o allexport
```

#### Passo 2: Clonar este repositório
Execute:
```bash
git clone https://github.com/Gbrlmoraes/chat_with_pdf.git
```

#### Passo 3: [Autenticação com a GCP](https://cloud.google.com/docs/authentication/gcloud?hl=pt-br)
Certifique-se de ter a CLI do gcloud instalada. Em seguida, execute:
```bash
gcloud auth login
```

ou, caso deseje usar a chave JSON da conta de serviço, execute:
```bash
gcloud auth login --cred-file=CAMINHO_PARA_A_CHAVE_JSON
```

#### Passo 4: Definir qual projeto será usado na GCP
Execute:
```bash
gcloud config set project $GCP_PROJECT_ID
```

#### Passo 5: Contruir e enviar a imagem Docker para a GCP
Execute:
```bash
export IMAGE_NAME=chat-with-pdf
gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/$IMAGE_NAME
```

#### Passo 6: Fazer o deploy da aplicação do Google Cloud Run
Execute:
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

### Extras:

#### Deploy local com Docker
_Será necessário fazer algumas alterações nos scripts para usar as variáveis de ambiente_
Construa a imagem Docker e execute o projeto localmente com os comandos abaixo, pode ser necessário :
```bash
docker build -t chat-with-pdf .
docker run -p 8501:8501 chat-with-pdf
```

#### Deploy continuo com GitHub Actions
Analise o arquivo deploy_gcp.yml e defina as variáveis correspondentes
