"""
Aplicação Flask principal
Segue padrão MVC adaptado para Flask
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

from config.settings import config
from services.nlp_service import NLPService
from services.email_service import GeminiService, EmailClassificationService
from utils.file_handler import FileHandler


# Inicializa a aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

# Habilita CORS
CORS(app)

# Cria pasta de uploads se não existir
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)

# Inicializa serviços (Dependency Injection)
nlp_service = NLPService()
gemini_service = GeminiService()
email_service = EmailClassificationService(nlp_service, gemini_service)
file_handler = FileHandler()


@app.route('/')
def index():
    """Rota principal - renderiza a página inicial"""
    return render_template('index.html')


@app.route('/api/classify', methods=['POST'])
def classify_emails():
    """
    API endpoint para classificação de e-mails
    Aceita texto direto (JSON) ou arquivo (FormData)
    """
    try:
        text_content = None
        
        # Verifica se é upload de arquivo
        if 'file' in request.files:
            file = request.files['file']
            
            if file and file.filename and file_handler.allowed_file(file.filename):
                # Salva arquivo temporariamente
                filename = secure_filename(file.filename)
                file_path = os.path.join(config.UPLOAD_FOLDER, filename)
                file.save(file_path)
                
                # Extrai texto do arquivo
                text_content = file_handler.extract_text_from_file(file_path, filename)
                
                # Remove arquivo temporário
                os.remove(file_path)
                
                if not text_content:
                    return jsonify({
                        'success': False,
                        'error': 'Não foi possível extrair texto do arquivo'
                    }), 400
        
        # Verifica se é texto direto via JSON
        elif request.is_json and 'text' in request.json:
            text_content = request.json['text']
        
        # Fallback: verifica se é texto via FormData
        elif 'text' in request.form:
            text_content = request.form['text']
        
        # Valida entrada
        if not text_content or not text_content.strip():
            return jsonify({
                'success': False,
                'error': 'Nenhum conteúdo fornecido'
            }), 400
        
        # Processa e classifica e-mails
        results = email_service.process_text_input(text_content)
        
        return jsonify({
            'success': True,
            'emails': results,
            'total': len(results)
        })
    
    except Exception as e:
        print(f"Erro no endpoint /api/classify: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erro ao processar: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Email Classification API'
    })


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handler para arquivos muito grandes"""
    return jsonify({
        'success': False,
        'error': 'Arquivo muito grande. Tamanho máximo: 16MB'
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handler para rotas não encontradas"""
    return jsonify({
        'success': False,
        'error': 'Rota não encontrada'
    }), 404


if __name__ == '__main__':
    # Porta configurável para Cloud Run
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
