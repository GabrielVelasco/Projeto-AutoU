"""
Configurações da aplicação
Singleton Pattern para gerenciar configurações centralizadas
"""

import os


class Config:
    """Classe de configuração usando Singleton Pattern"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Inicializa as configurações"""
        # API Configuration
        self.GEMINI_API_KEY = "AIzaSyAzlQnmePYFIXnKuj3gy011Tfj4a_0uiOo"
        self.GEMINI_MODEL = "gemini-2.0-flash-exp"
        
        # Flask Configuration
        self.SECRET_KEY = os.urandom(24)
        self.MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
        
        # Upload Configuration
        self.ALLOWED_EXTENSIONS = {'txt', 'pdf'}
        self.UPLOAD_FOLDER = 'uploads'
        
        # NLP Configuration
        self.STOPWORDS_LANGUAGE = 'portuguese'
        self.EMAIL_SEPARATOR = '##### EMAIL #####'
        
        # Prompt Template
        self.CLASSIFICATION_PROMPT = """Trabalho em uma empresa do ramo financeiro (tipo banco/fintech), recebo muitos emails diários e preciso classificar o que é importante e o que não é. Me ajude a analisar o teor da mensagem e classificar o email como Importante ou Despresível. Tome o tempo que for necessário para pesquisar sobre do que se trata as empresas do setor e com quais problemas elas geralmente lidam, para que você tenha mais embasamento na hora de fazer a classificação.

São importantes emails com o seguinte teor: 
Solicitações de suporte técnico, atualização sobre casos em aberto, requisições importantes, dúvidas sobre o sistema e etc.

Email com o seguinte teor podem ser considerados despresíveis: 
Mensagem de feliz natal, congratulações e agradecimentos, ou perguntas não relevantes dado o contexto de atuação da empresa. Esses não precisam de sugestão de resposta.

Segue a mensagem (entre $ $) a ser classificada como 'Importante' ou 'Despresível' (caso haja dúvida, favoreça a classificação como 'Importante').

IMPORTANTE: Retorne APENAS um JSON válido no seguinte formato, sem qualquer texto adicional antes ou depois:
{{"classificacao": "Importante" ou "Despresível", "resposta_sugerida": "texto da resposta ou null se despresível"}}

$ 
{email_content}
$
"""


# Instância global
config = Config()
