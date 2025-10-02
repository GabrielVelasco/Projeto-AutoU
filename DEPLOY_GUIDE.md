# 🚀 Guia de Deploy no Google Cloud Run

Este guia mostra como fazer deploy da aplicação de classificação de e-mails no Google Cloud Run.

## 📋 Pré-requisitos

1. Conta no Google Cloud Platform (GCP)
2. Projeto criado no GCP
3. Faturamento ativado no projeto
4. Google Cloud SDK (`gcloud`) instalado localmente

### Instalar Google Cloud SDK

**Linux/Mac:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

**Windows:**
- Baixe o instalador: https://cloud.google.com/sdk/docs/install

## 🔧 Passo a Passo

### 1. Configurar Google Cloud CLI

```bash
# Login no Google Cloud
gcloud auth login

# Configurar projeto (substitua PROJECT_ID pelo ID do seu projeto)
gcloud config set project PROJECT_ID

# Verificar projeto atual
gcloud config get-value project

# Habilitar APIs necessárias
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 2. Construir e Fazer Deploy

#### Opção A: Deploy Direto (Recomendado - Mais Fácil)

```bash
# Navegar até o diretório do projeto
cd /home/gabriel-velasco/Documents/ProjetoAutoU2

# Deploy com build automático
gcloud run deploy email-classifier \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10 \
  --port 8080
```

#### Opção B: Build Manual + Deploy (Mais Controle)

```bash
# 1. Definir variáveis
export PROJECT_ID=$(gcloud config get-value project)
export REGION=us-central1
export SERVICE_NAME=email-classifier

# 2. Build da imagem Docker no Cloud Build
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# 3. Deploy no Cloud Run COM variáveis de ambiente
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10 \
  --port 8080 \
  --set-env-vars GEMINI_API_KEY=sua_chave_api_aqui
```

### 3. Configurar Variáveis de Ambiente (IMPORTANTE)

⚠️ **A API key DEVE ser configurada via variável de ambiente!**

```bash
gcloud run services update projeto-autou \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=SUA_CHAVE_API_AQUI
```

📖 Guia completo de configuração: [CONFIG_ENV_VARS.md](CONFIG_ENV_VARS.md)

### 4. Verificar Deploy

Após o deploy, você receberá uma URL como:
```
https://email-classifier-xxxxx-uc.a.run.app
```

Teste a API:
```bash
# Health check
curl https://email-classifier-xxxxx-uc.a.run.app/api/health

# Classificar e-mail
curl -X POST https://email-classifier-xxxxx-uc.a.run.app/api/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Olá, preciso urgentemente do status da minha solicitação #12345"}'
```

## 🔐 Segurança e Produção

### 1. Proteger API com Autenticação

Para exigir autenticação:
```bash
# Deploy com autenticação
gcloud run deploy email-classifier \
  --source . \
  --platform managed \
  --region us-central1 \
  --no-allow-unauthenticated

# Dar permissão a usuários específicos
gcloud run services add-iam-policy-binding email-classifier \
  --region us-central1 \
  --member="user:email@example.com" \
  --role="roles/run.invoker"
```

### 2. Usar Secret Manager para API Keys

```bash
# Criar secret
echo -n "SUA_CHAVE_API_AQUI" | \
  gcloud secrets create gemini-api-key --data-file=-

# Usar no Cloud Run
gcloud run deploy email-classifier \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-secrets GEMINI_API_KEY=gemini-api-key:latest
```

### 3. Configurar CORS para Frontend Específico

Atualizar `app.py`:
```python
CORS(app, origins=["https://seu-frontend.com"])
```

### 4. Adicionar Domínio Customizado

```bash
# Mapear domínio
gcloud run domain-mappings create \
  --service email-classifier \
  --domain api.seudominio.com \
  --region us-central1
```

## 💰 Custos Estimados

Cloud Run cobra por:
- **Requests**: $0.40 por milhão de requests
- **CPU**: $0.00002400 por vCPU-segundo
- **Memória**: $0.00000250 por GiB-segundo
- **Free Tier**: 2 milhões de requests/mês grátis

**Estimativa mensal** (1000 requests/dia):
- ~$0.01 a $0.50/mês (dentro do free tier)

## 📊 Monitoramento

### Ver Logs
```bash
# Logs em tempo real
gcloud run services logs tail email-classifier --region us-central1

# Logs no console
https://console.cloud.google.com/run
```

### Métricas
- Acesse: Cloud Console → Cloud Run → email-classifier → Metrics

## 🔄 Atualizar Deploy

Após fazer alterações no código:
```bash
# Commit das alterações
git add .
git commit -m "Update: nova feature"

# Novo deploy
gcloud run deploy email-classifier --source . --region us-central1
```

## 🐛 Troubleshooting

### Problema: Build falha
**Solução**: Verificar logs do Cloud Build
```bash
gcloud builds list --limit 5
gcloud builds log BUILD_ID
```

### Problema: Container não inicia
**Solução**: Verificar logs do serviço
```bash
gcloud run services logs read email-classifier --region us-central1 --limit 50
```

### Problema: Timeout nas requisições
**Solução**: Aumentar timeout
```bash
gcloud run services update email-classifier \
  --region us-central1 \
  --timeout 600
```

### Problema: Memória insuficiente
**Solução**: Aumentar memória
```bash
gcloud run services update email-classifier \
  --region us-central1 \
  --memory 1Gi
```

## 📱 Conectar Frontend

Após o deploy, atualize o frontend para usar a URL do Cloud Run:

```javascript
// main.js
const API_URL = 'https://email-classifier-xxxxx-uc.a.run.app';

const response = await fetch(`${API_URL}/api/classify`, {
    method: 'POST',
    headers: requestHeaders,
    body: requestBody
});
```

## 🌍 Regiões Disponíveis

Escolha a região mais próxima dos seus usuários:
- `us-central1` (Iowa) - Recomendado para Brasil
- `us-east1` (Carolina do Sul)
- `southamerica-east1` (São Paulo) - Mais próximo do Brasil
- `europe-west1` (Bélgica)
- `asia-northeast1` (Tóquio)

## ✅ Checklist de Deploy

- [ ] Google Cloud SDK instalado e configurado
- [ ] Projeto GCP criado e faturamento ativado
- [ ] APIs habilitadas (Cloud Run, Container Registry, Cloud Build)
- [ ] Dockerfile criado
- [ ] requirements.txt com gunicorn
- [ ] .dockerignore configurado
- [ ] Build e deploy executados com sucesso
- [ ] URL do serviço obtida
- [ ] API testada com curl/Postman
- [ ] Frontend atualizado com nova URL (se aplicável)
- [ ] Monitoramento configurado
- [ ] Logs verificados

## 🎉 Pronto!

Sua aplicação está rodando no Google Cloud Run e pode escalar automaticamente conforme a demanda!

**URL de exemplo**: `https://email-classifier-xxxxx-uc.a.run.app`

**Próximos Passos**:
1. Adicionar domínio customizado
2. Configurar CI/CD com GitHub Actions
3. Implementar cache para melhor performance
4. Adicionar testes automatizados
