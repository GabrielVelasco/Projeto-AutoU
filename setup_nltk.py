"""
Script de inicialização para baixar recursos NLTK necessários
"""

import nltk

def setup_nltk():
    """Baixa recursos necessários do NLTK"""
    resources = [
        'stopwords',
        'punkt',
        'rslp'  # Stemmer para português
    ]
    
    print("Baixando recursos NLTK...")
    for resource in resources:
        try:
            nltk.download(resource, quiet=False)
            print(f"✓ {resource} baixado com sucesso")
        except Exception as e:
            print(f"✗ Erro ao baixar {resource}: {e}")
    
    print("\nRecursos NLTK configurados!")

if __name__ == "__main__":
    setup_nltk()
