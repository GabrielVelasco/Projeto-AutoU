# 📧 Sistema de Classificação Automática de E-mails

Sistema inteligente para classificação e geração de respostas automáticas para e-mails corporativos do setor financeiro, utilizando IA generativa.

## 🎯 Objetivo

Automatizar o processo de triagem de e-mails em empresas financeiras, identificando mensagens que requerem atenção imediata e gerando respostas automáticas quando apropriado.

## 🚀 Tecnologias Utilizadas

- **Backend**: Python 3.12 + Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **IA**: Google Gemini API (gemini-2.0-flash-exp)
- **NLP**: NLTK (Natural Language Toolkit)
- **Bibliotecas**: PyPDF2, Flask-CORS

## ✨ Funcionalidades

### Interface do Usuário
- ✅ Upload de arquivos (PDF, TXT) ou inserção direta de texto
- ✅ Suporte a múltiplos e-mails separados por delimitador (`##### EMAIL #####`)
- ✅ Interface drag-and-drop para upload de arquivos
- ✅ Design responsivo e moderno

### Processamento
- ✅ Classificação automática: "Importante" ou "Despresível"
- ✅ Geração de respostas automáticas para e-mails importantes
- ✅ Pré-processamento NLP (remoção de stopwords, stemming)
- ✅ Extração de palavras-chave

### Armazenamento
- ✅ Persistência local usando LocalStorage do navegador
- ✅ Histórico de e-mails analisados
- ✅ Estatísticas de classificação

## 🔧 Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório** (ou navegue até o diretório)
```bash
cd /home/gabriel-velasco/Documents/ProjetoAutoU2
```

2. **Crie e ative um ambiente virtual** (recomendado)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure recursos do NLTK**
```bash
python setup_nltk.py
```

5. **Execute a aplicação**
```bash
python app.py
# ou use o script de conveniência:
./run.sh
```

6. **Acesse no navegador**
```
http://localhost:5000
```

## 📝 Como Usar

### Análise de E-mail Único
1. Acesse a aplicação no navegador
2. Na aba "Texto", cole o conteúdo do e-mail
3. Clique em "Classificar E-mails"
4. Visualize o resultado com classificação e resposta sugerida

### Análise de Múltiplos E-mails
1. Separe cada e-mail com o delimitador: `##### EMAIL #####`
2. Cole todo o texto na aba "Texto"
3. Clique em "Classificar E-mails"
4. Todos os e-mails serão processados individualmente

### Upload de Arquivo
1. Vá para a aba "Upload"
2. Arraste um arquivo PDF ou TXT, ou clique para selecionar
3. Clique em "Classificar E-mails"
4. Visualize os resultados

### Gerenciar Resultados
- **Expandir e-mail**: Clique no card para ver detalhes completos
- **Limpar histórico**: Clique em "Limpar Tudo"
- **Persistência**: Os resultados são salvos automaticamente no navegador

## 🌐 Deploy em Produção

### Google Cloud Run (Recomendado)

O projeto está pronto para deploy no Google Cloud Run. Siga o guia completo em [`DEPLOY_GUIDE.md`](DEPLOY_GUIDE.md).

**Deploy rápido:**
```bash
# 1. Instalar Google Cloud SDK
curl https://sdk.cloud.google.com | bash

# 2. Configurar projeto
gcloud config set project SEU_PROJECT_ID

# 3. Fazer deploy
./deploy.sh
```

Ou manualmente:
```bash
gcloud run deploy email-classifier \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Custos**: ~$0.01 a $0.50/mês (dentro do free tier do GCP)

### Outras Opções de Deploy
- **Heroku**: `heroku create && git push heroku main`
- **Railway**: Conectar repositório GitHub
- **Render**: Deploy automático via Git
- **AWS Elastic Beanstalk**: Deploy com Docker
- **Azure App Service**: Deploy com Container

📖 Guia completo: [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)

## 📂 Estrutura do Projeto

```
ProjetoAutoU2/
├── app.py                    # Aplicação Flask principal (Controller)
├── requirements.txt          # Dependências Python
├── setup_nltk.py            # Script de configuração NLTK
├── run.sh                   # Script de inicialização
├── exemplo_emails.txt       # Exemplos de e-mails para teste
│
├── config/
│   ├── __init__.py
│   └── settings.py          # Configurações (Singleton Pattern)
│
├── services/
│   ├── __init__.py
│   ├── nlp_service.py       # Service Layer - NLP
│   └── email_service.py     # Service Layer - Gemini API
│
├── utils/
│   ├── __init__.py
│   └── file_handler.py      # Utilitários de manipulação de arquivos
│
├── static/
│   ├── css/
│   │   └── style.css        # Estilos da aplicação
│   └── js/
│       └── main.js          # Lógica frontend
│
└── templates/
    └── index.html           # Template HTML principal
```

## 🏗️ Arquitetura e Padrões

### Arquitetura
- **MVC Adaptado**: Model-View-Controller adaptado para Flask
- **Service Layer**: Separação da lógica de negócio
- **Dependency Injection**: Injeção de dependências nos serviços

### Padrões de Projeto
- **Singleton**: Configurações centralizadas (`Config`)
- **Service Layer**: Camada de serviços (`NLPService`, `GeminiService`)
- **Factory Method**: Criação de handlers de arquivo
- **Strategy Pattern**: Diferentes estratégias de processamento NLP

### Clean Code
- ✅ Nomes descritivos e significativos
- ✅ Funções pequenas e focadas (SRP - Single Responsibility Principle)
- ✅ Separação de responsabilidades
- ✅ Comentários e docstrings
- ✅ Tratamento de erros consistente

## 🔐 Configuração da API

A chave da API do Gemini está configurada em `config/settings.py`:

```python
GEMINI_API_KEY = "AIzaSyAzlQnmePYFIXnKuj3gy011Tfj4a_0uiOo"
GEMINI_MODEL = "gemini-2.0-flash-exp"
```

> ⚠️ **Nota de Segurança**: Em produção, use variáveis de ambiente para armazenar chaves sensíveis.

## 🧪 Testes

Um arquivo de exemplo está disponível em `exemplo_emails.txt` com diferentes tipos de e-mails para testar o sistema.

## 🎨 Interface

A interface foi desenvolvida com foco em:
- **Usabilidade**: Intuitiva, sem necessidade de manual
- **Clareza**: Propósito evidente desde o primeiro contato
- **Organização Visual**: Design limpo e sem distrações
- **Responsividade**: Funciona em diferentes tamanhos de tela
- **Feedback Visual**: Animações e notificações claras

## 🚀 Melhorias Futuras

- [ ] Integração com APIs de e-mail (Gmail, Outlook)
- [ ] Dashboard de analytics
- [ ] Exportação de relatórios
- [ ] Suporte a mais idiomas
- [ ] Treinamento de modelo customizado
- [ ] Sistema de autenticação
- [ ] Banco de dados para persistência

## 📄 Licença

MIT License - Sinta-se livre para usar este projeto!

## 👨‍💻 Desenvolvedor

Desenvolvido com ❤️ usando Flask + Gemini AI para automação inteligente de e-mails corporativos.
