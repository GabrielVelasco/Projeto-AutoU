# Use uma imagem Python oficial
FROM python:3.12-slim

# Define variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia arquivos de dependências
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Baixa recursos do NLTK
RUN python -c "import nltk; nltk.download('stopwords', quiet=True); nltk.download('punkt', quiet=True); nltk.download('rslp', quiet=True)"

# Copia o código da aplicação
COPY . .

# Cria diretório de uploads
RUN mkdir -p uploads

# Expõe a porta que o Cloud Run usa
EXPOSE 8080

# Comando para executar a aplicação com Gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
