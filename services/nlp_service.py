"""
Serviço de Processamento de Linguagem Natural (NLP)
Responsável por pré-processar e limpar texto de e-mails
"""

import re
import nltk
from typing import List
from config.settings import config


class NLPService:
    """Service Layer para processamento de linguagem natural"""
    
    def __init__(self):
        """Inicializa o serviço NLP e baixa recursos necessários"""
        self._ensure_nltk_resources()
        self.stopwords = set(nltk.corpus.stopwords.words(config.STOPWORDS_LANGUAGE))
        self.stemmer = nltk.stem.RSLPStemmer()  # Stemmer para português
    
    def _ensure_nltk_resources(self):
        """Garante que os recursos NLTK necessários estão disponíveis"""
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
        
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
    
    def split_emails(self, text: str) -> List[str]:
        """
        Separa múltiplos e-mails com base no separador configurado
        
        Args:
            text: Texto contendo um ou mais e-mails
            
        Returns:
            Lista de e-mails individuais
        """
        if config.EMAIL_SEPARATOR in text:
            emails = text.split(config.EMAIL_SEPARATOR)
            return [email.strip() for email in emails if email.strip()]
        return [text.strip()]
    
    def clean_text(self, text: str) -> str:
        """
        Limpa e normaliza o texto
        
        Args:
            text: Texto bruto do e-mail
            
        Returns:
            Texto limpo e normalizado
        """
        # Remove caracteres especiais excessivos
        text = re.sub(r'[^\w\s\.\,\!\?\-\:\;\(\)]', ' ', text)
        
        # Remove espaços múltiplos
        text = re.sub(r'\s+', ' ', text)
        
        # Remove espaços no início e fim
        text = text.strip()
        
        return text
    
    def remove_stopwords(self, text: str) -> str:
        """
        Remove stopwords do texto (opcional - usado para análise)
        
        Args:
            text: Texto a processar
            
        Returns:
            Texto sem stopwords
        """
        words = text.lower().split()
        filtered_words = [word for word in words if word not in self.stopwords]
        return ' '.join(filtered_words)
    
    def apply_stemming(self, text: str) -> str:
        """
        Aplica stemming/lematização ao texto
        
        Args:
            text: Texto a processar
            
        Returns:
            Texto com stemming aplicado
        """
        words = text.lower().split()
        stemmed_words = [self.stemmer.stem(word) for word in words]
        return ' '.join(stemmed_words)
    
    def preprocess_for_analysis(self, text: str) -> dict:
        """
        Pré-processa texto completo para análise (mantém original + versões processadas)
        
        Args:
            text: Texto original do e-mail
            
        Returns:
            Dicionário com versões do texto (original e processadas)
        """
        cleaned = self.clean_text(text)
        
        return {
            'original': text,
            'cleaned': cleaned,
            'without_stopwords': self.remove_stopwords(cleaned),
            'stemmed': self.apply_stemming(cleaned)
        }
    
    def extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        """
        Extrai palavras-chave principais do texto
        
        Args:
            text: Texto a analisar
            top_n: Número de palavras-chave a retornar
            
        Returns:
            Lista de palavras-chave
        """
        # Remove stopwords e aplica stemming
        processed = self.apply_stemming(self.remove_stopwords(text))
        words = processed.split()
        
        # Conta frequência
        from collections import Counter
        word_freq = Counter(words)
        
        # Retorna top N palavras mais frequentes
        return [word for word, _ in word_freq.most_common(top_n)]
