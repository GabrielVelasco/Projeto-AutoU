"""
Utilitários para manipulação de arquivos
"""

import PyPDF2
from typing import Optional
from werkzeug.utils import secure_filename
from config.settings import config


class FileHandler:
    """Classe para manipulação de arquivos"""
    
    @staticmethod
    def allowed_file(filename: str) -> bool:
        """
        Verifica se a extensão do arquivo é permitida
        
        Args:
            filename: Nome do arquivo
            
        Returns:
            True se permitido, False caso contrário
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> Optional[str]:
        """
        Extrai texto de arquivo PDF
        
        Args:
            file_path: Caminho do arquivo PDF
            
        Returns:
            Texto extraído ou None se falhar
        """
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"Erro ao extrair texto do PDF: {str(e)}")
            return None
    
    @staticmethod
    def extract_text_from_txt(file_path: str) -> Optional[str]:
        """
        Extrai texto de arquivo TXT
        
        Args:
            file_path: Caminho do arquivo TXT
            
        Returns:
            Texto extraído ou None se falhar
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            print(f"Erro ao ler arquivo TXT: {str(e)}")
            return None
    
    @staticmethod
    def extract_text_from_file(file_path: str, filename: str) -> Optional[str]:
        """
        Extrai texto de arquivo baseado na extensão
        
        Args:
            file_path: Caminho do arquivo
            filename: Nome do arquivo
            
        Returns:
            Texto extraído ou None se falhar
        """
        extension = filename.rsplit('.', 1)[1].lower()
        
        if extension == 'pdf':
            return FileHandler.extract_text_from_pdf(file_path)
        elif extension == 'txt':
            return FileHandler.extract_text_from_txt(file_path)
        else:
            return None
