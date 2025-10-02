# 📧 Sistema de Classificação Automática de E-mails

Sistema inteligente para classificação e geração de respostas automáticas para e-mails corporativos do setor financeiro, utilizando IA generativa.

Acesse aqui: https://projeto-autou-16087676324.europe-west1.run.app/

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
- **Dependency Injection**: Injeção de dependências nos serviços (req.txt)

### Padrões de Projeto
- **Singleton**: Configs centralizadas (`Config` que guarda configs base da Gemini API)
- **Service Layer**: Camada de serviços (`NLPService`, `GeminiService`)
- **Factory Method**: Criação de handlers de arquivo
- **Strategy Pattern**: Diferentes estratégias de processamento NLP

### Clean Code
- ✅ Nomes descritivos e significativos
- ✅ Funções pequenas e focadas (SRP - Single Responsibility Principle)
- ✅ Separação de responsabilidades
- ✅ Comentários e docstrings
- ✅ Tratamento de erros consistente

## 🧪 Testes

Um arquivo de exemplo está disponível em `exemplo_emails.txt` com diferentes tipos de e-mails para testar o sistema.

## �🚀 Melhorias Futuras

- [ ] Integração com APIs de e-mail (Gmail, Outlook)
- [ ] Banco de dados para persistência...

## 👨‍💻 Desenvolvedor

Desenvolvido sem ❤️ usando Flask + Gemini AI para automação inteligente de e-mails corporativos (a IA vai roubar meu emprego).
