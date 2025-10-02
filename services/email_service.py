"""
Serviço de integração com Google Gemini API
Responsável pela classificação de e-mails e geração de respostas
"""

import google.generativeai as genai
import json
import re
from typing import Dict, Optional
from config.settings import config


class GeminiService:
    """Service Layer para integração com Gemini API"""
    
    def __init__(self):
        """Inicializa o serviço Gemini"""
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)
    
    def classify_email(self, email_content: str) -> Dict[str, Optional[str]]:
        """
        Classifica um e-mail e gera resposta automática se necessário
        
        Args:
            email_content: Conteúdo do e-mail a ser classificado
            
        Returns:
            Dicionário com classificação e resposta sugerida
        """
        try:
            # Formata o prompt com o conteúdo do e-mail
            prompt = config.CLASSIFICATION_PROMPT.format(email_content=email_content)
            
            # Chama a API do Gemini
            response = self.model.generate_content(prompt)
            
            # Extrai e processa a resposta
            result = self._parse_response(response.text)
            
            return result
            
        except Exception as e:
            print(f"Erro ao classificar e-mail: {str(e)}")
            return {
                'classificacao': 'Importante',  # Em caso de erro, marca como importante por segurança
                'resposta_sugerida': None,
                'error': str(e)
            }
    
    def _parse_response(self, response_text: str) -> Dict[str, Optional[str]]:
        """
        Faz parsing da resposta do Gemini
        
        Args:
            response_text: Texto de resposta da API
            
        Returns:
            Dicionário estruturado com classificação e resposta
        """
        try:
            # Tenta extrair JSON da resposta
            # Remove possíveis markdown code blocks
            cleaned_text = re.sub(r'```json\s*|\s*```', '', response_text)
            cleaned_text = cleaned_text.strip()
            
            # Tenta fazer parse do JSON
            result = json.loads(cleaned_text)
            
            # Valida estrutura
            if 'classificacao' not in result:
                raise ValueError("Resposta sem campo 'classificacao'")
            
            # Normaliza a classificação
            classificacao = result['classificacao'].strip()
            if classificacao not in ['Importante', 'Despresível']:
                classificacao = 'Importante'  # Default seguro
            
            return {
                'classificacao': classificacao,
                'resposta_sugerida': result.get('resposta_sugerida')
            }
            
        except json.JSONDecodeError:
            # Fallback: tenta extrair informação usando regex
            return self._fallback_parse(response_text)
    
    def _fallback_parse(self, text: str) -> Dict[str, Optional[str]]:
        """
        Método de fallback para parsing quando JSON falha
        
        Args:
            text: Texto de resposta
            
        Returns:
            Dicionário com melhor interpretação possível
        """
        text_lower = text.lower()
        
        # Tenta identificar classificação
        if 'despresível' in text_lower or 'despresivel' in text_lower:
            classificacao = 'Despresível'
            resposta = None
        else:
            classificacao = 'Importante'
            
            # Tenta extrair resposta sugerida
            match = re.search(r'resposta[:\s]+(.+)', text, re.IGNORECASE | re.DOTALL)
            resposta = match.group(1).strip() if match else None
        
        return {
            'classificacao': classificacao,
            'resposta_sugerida': resposta
        }


class EmailClassificationService:
    """Service Layer principal para classificação de e-mails"""
    
    def __init__(self, nlp_service, gemini_service):
        """
        Inicializa o serviço de classificação
        
        Args:
            nlp_service: Serviço de NLP
            gemini_service: Serviço Gemini
        """
        self.nlp_service = nlp_service
        self.gemini_service = gemini_service
    
    def process_text_input(self, text: str) -> list:
        """
        Processa entrada de texto, lidando com múltiplos e-mails
        
        Args:
            text: Texto contendo um ou mais e-mails
            
        Returns:
            Lista de e-mails classificados
        """
        # Separa múltiplos e-mails
        emails = self.nlp_service.split_emails(text)
        
        # Processa cada e-mail
        results = []
        for email in emails:
            # Pré-processa o e-mail
            processed = self.nlp_service.preprocess_for_analysis(email)
            
            # Classifica usando Gemini (usa texto limpo)
            classification = self.gemini_service.classify_email(processed['cleaned'])
            
            # Extrai palavras-chave
            keywords = self.nlp_service.extract_keywords(processed['cleaned'])
            
            # Monta resultado
            results.append({
                'email_original': email,
                'email_limpo': processed['cleaned'],
                'classificacao': classification['classificacao'],
                'resposta_sugerida': classification['resposta_sugerida'],
                'palavras_chave': keywords,
                'error': classification.get('error')
            })
        
        return results
