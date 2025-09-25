# api/index.py - Wrapper WSGI para Vercel
import os
import sys

# Adiciona o diretório pai ao path do Python para importar app.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar variável de ambiente para detectar Vercel
os.environ['VERCEL'] = '1'

from app import app, init_db

# Inicializar banco na primeira execução
with app.app_context():
    init_db()

# Export para Vercel - a variável deve se chamar 'app' ou 'application'
application = app

# Para testes locais
if __name__ == "__main__":
    app.run(debug=True)
