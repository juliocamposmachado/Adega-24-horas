# app.py - Aplicação Principal da Adega
# Este é o arquivo principal do nosso projeto Flask
# Aqui configuramos a aplicação, rotas e funcionalidades principais

# IMPORTAÇÕES NECESSÁRIAS
# =====================================================
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timezone
import os
import json
import urllib.parse
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# CONFIGURAÇÃO DA APLICAÇÃO FLASK
# =====================================================
app = Flask(__name__)

# Configuração da chave secreta (necessária para sessões e formulários)
# Em produção, use uma chave mais segura e nunca coloque no código
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui-mude-em-producao'

# Configuração do banco de dados SQLite
# SQLite é um banco de dados simples, ideal para desenvolvimento
# O arquivo será criado na pasta instance/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adega.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INICIALIZAÇÃO DAS EXTENSÕES
# =====================================================
# SQLAlchemy - ORM (Object Relational Mapping) para trabalhar com banco de dados
db = SQLAlchemy(app)

# Migrate - Para criar e gerenciar migrações do banco de dados
migrate = Migrate(app, db)

# MODELOS DO BANCO DE DADOS
# =====================================================
# Modelo para representar um produto na adega
class Produto(db.Model):
    """
    Modelo Produto - Representa cada item disponível na adega
    
    Conceitos importantes:
    - db.Model: Classe base para todos os modelos do SQLAlchemy
    - db.Column: Define uma coluna na tabela do banco de dados
    - primary_key: Chave primária (identificador único)
    - nullable: Se o campo pode ser nulo/vazio
    """
    
    # ID único para cada produto (chave primária)
    id = db.Column(db.Integer, primary_key=True)
    
    # Nome do produto (até 100 caracteres, obrigatório)
    nome = db.Column(db.String(100), nullable=False)
    
    # Descrição detalhada do produto (texto longo)
    descricao = db.Column(db.Text, nullable=True)
    
    # Preço do produto (número decimal com até 2 casas decimais)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Categoria do produto (cerveja, vinho, destilados, etc.)
    categoria = db.Column(db.String(50), nullable=False)
    
    # URL da imagem do produto
    imagem_url = db.Column(db.String(200), nullable=True)
    
    # Estoque disponível
    estoque = db.Column(db.Integer, default=0)
    
    # Se o produto está ativo/disponível
    ativo = db.Column(db.Boolean, default=True)
    
    # Data de criação do produto
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        """
        Método especial que define como o objeto é representado quando impresso
        Útil para debugging
        """
        return f'<Produto {self.nome}>'
    
    def to_dict(self):
        """
        Método personalizado para converter o produto em dicionário
        Útil para APIs e JSON
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': float(self.preco),
            'categoria': self.categoria,
            'imagem_url': self.imagem_url,
            'estoque': self.estoque,
            'ativo': self.ativo
        }

# Modelo para representar um pedido
class Pedido(db.Model):
    """
    Modelo Pedido - Representa um pedido feito por um cliente
    """
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Informações do cliente
    nome_cliente = db.Column(db.String(100), nullable=False)
    telefone_cliente = db.Column(db.String(20), nullable=False)
    endereco_cliente = db.Column(db.Text, nullable=False)
    
    # Valor total do pedido
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Status do pedido (pendente, confirmado, entregue, cancelado)
    status = db.Column(db.String(20), default='pendente')
    
    # Data e hora do pedido
    data_pedido = db.Column(db.DateTime, default=datetime.now)
    
    # Observações adicionais
    observacoes = db.Column(db.Text, nullable=True)
    
    # Relacionamento com os itens do pedido
    # backref cria automaticamente uma propriedade 'pedido' em ItemPedido
    itens = db.relationship('ItemPedido', backref='pedido', lazy=True)
    
    def __repr__(self):
        return f'<Pedido {self.id} - {self.nome_cliente}>'

# Modelo para representar itens individuais de um pedido
class ItemPedido(db.Model):
    """
    Modelo ItemPedido - Representa cada item dentro de um pedido
    
    Conceito de relacionamento:
    - Um pedido pode ter vários itens
    - Cada item pertence a um pedido específico
    - Usamos chave estrangeira (ForeignKey) para conectar as tabelas
    """
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Chave estrangeira para o pedido (relacionamento)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    
    # Chave estrangeira para o produto
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    
    # Quantidade do produto neste item
    quantidade = db.Column(db.Integer, nullable=False)
    
    # Preço unitário no momento do pedido (pode ser diferente do preço atual)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Relacionamento com produto
    produto = db.relationship('Produto', backref='itens_pedido')
    
    @property
    def subtotal(self):
        """
        Property que calcula o subtotal do item (quantidade × preço unitário)
        Property é um método que se comporta como atributo
        """
        return self.quantidade * self.preco_unitario
    
    def __repr__(self):
        return f'<ItemPedido {self.produto.nome} x{self.quantidade}>'

# FUNÇÕES AUXILIARES
# =====================================================
def obter_carrinho():
    """
    Função para obter o carrinho da sessão
    
    Conceitos importantes:
    - session: Armazena dados do usuário durante a navegação
    - get(): Método seguro para obter valor, retorna None se não existir
    - list(): Converte para lista (caso não seja)
    """
    return session.get('carrinho', [])

def salvar_carrinho(carrinho):
    """
    Função para salvar o carrinho na sessão
    """
    session['carrinho'] = carrinho

def calcular_total_carrinho(carrinho):
    """
    Função para calcular o valor total do carrinho
    
    Conceitos:
    - sum(): Função built-in do Python para somar elementos
    - Generator expression: (item['subtotal'] for item in carrinho)
    - É mais eficiente que list comprehension para somas
    """
    return sum(item['subtotal'] for item in carrinho)

def gerar_mensagem_whatsapp(pedido_dados, carrinho):
    """
    Função para gerar mensagem formatada para WhatsApp
    
    Args:
        pedido_dados: Dicionário com dados do cliente
        carrinho: Lista com itens do carrinho
    
    Returns:
        String com mensagem formatada
    """
    
    # Cabeçalho da mensagem
    mensagem = "🍷 *PEDIDO ADEGA RÁDIO TATUAPÉ FM* 🍷\n\n"
    
    # Informações do cliente
    mensagem += f"👤 *Cliente:* {pedido_dados['nome']}\n"
    mensagem += f"📞 *Telefone:* {pedido_dados['telefone']}\n"
    mensagem += f"📍 *Endereço:* {pedido_dados['endereco']}\n"
    mensagem += f"🕐 *Data/Hora:* {datetime.now().strftime('%d/%m/%Y às %H:%M')}\n\n"
    
    # Itens do pedido
    mensagem += "🛒 *ITENS DO PEDIDO:*\n"
    mensagem += "-" * 30 + "\n"
    
    total = 0
    for item in carrinho:
        subtotal = item['quantidade'] * item['preco']
        total += subtotal
        mensagem += f"• {item['nome']}\n"
        mensagem += f"  Qtd: {item['quantidade']} x R$ {item['preco']:.2f}\n"
        mensagem += f"  Subtotal: R$ {subtotal:.2f}\n\n"
    
    mensagem += "-" * 30 + "\n"
    mensagem += f"💰 *TOTAL: R$ {total:.2f}*\n\n"
    
    # Instruções de pagamento
    mensagem += "💳 *PAGAMENTO:*\n"
    mensagem += "PIX: radiotatuapefm@gmail.com\n\n"
    mensagem += "⚠️ *IMPORTANTE:*\n"
    mensagem += "• Efetue o pagamento via PIX\n"
    mensagem += "• Envie o comprovante para este número\n"
    mensagem += "• A entrega será liberada após confirmação\n\n"
    mensagem += "Obrigado pela preferência! 🙏"
    
    return mensagem

# ROTAS DA APLICAÇÃO
# =====================================================

@app.route('/')
def index():
    """
    Rota principal - Página inicial com catálogo de produtos
    
    Conceitos:
    - @app.route(): Decorador que define uma rota URL
    - render_template(): Função que renderiza um template HTML
    - Query do banco: Produto.query.filter_by().all()
    """
    
    # Busca todos os produtos ativos no banco de dados
    produtos = Produto.query.filter_by(ativo=True).all()
    
    # Obter carrinho atual
    carrinho = obter_carrinho()
    total_itens = sum(item['quantidade'] for item in carrinho)
    
    # Renderiza o template passando os produtos
    return render_template('index.html', 
                         produtos=produtos, 
                         total_itens=total_itens)

@app.route('/produto/<int:produto_id>')
def detalhes_produto(produto_id):
    """
    Rota para exibir detalhes de um produto específico
    
    Conceitos:
    - <int:produto_id>: Parâmetro da URL que é convertido para inteiro
    - get_or_404(): Busca o produto ou retorna erro 404 se não encontrar
    """
    
    produto = Produto.query.get_or_404(produto_id)
    carrinho = obter_carrinho()
    total_itens = sum(item['quantidade'] for item in carrinho)
    
    return render_template('produto_detalhes.html', 
                         produto=produto,
                         total_itens=total_itens)

@app.route('/adicionar_carrinho', methods=['POST'])
def adicionar_carrinho():
    """
    Rota para adicionar produtos ao carrinho
    
    Conceitos:
    - methods=['POST']: Aceita apenas requisições POST
    - request.form: Dados enviados via formulário POST
    - request.is_json: Verifica se é requisição JSON (AJAX)
    - jsonify(): Converte dicionário Python para JSON
    """
    
    try:
        # Verifica se é uma requisição JSON (AJAX)
        if request.is_json:
            dados = request.get_json()
            produto_id = dados.get('produto_id')
            quantidade = dados.get('quantidade', 1)
        else:
            # Dados de formulário tradicional
            produto_id = int(request.form.get('produto_id'))
            quantidade = int(request.form.get('quantidade', 1))
        
        # Busca o produto no banco
        produto = Produto.query.get_or_404(produto_id)
        
        # Verifica se há estoque suficiente
        if produto.estoque < quantidade:
            if request.is_json:
                return jsonify({'error': 'Estoque insuficiente'}), 400
            flash('Estoque insuficiente!', 'error')
            return redirect(url_for('index'))
        
        # Obter carrinho atual
        carrinho = obter_carrinho()
        
        # Verifica se o produto já está no carrinho
        produto_no_carrinho = None
        for item in carrinho:
            if item['produto_id'] == produto_id:
                produto_no_carrinho = item
                break
        
        if produto_no_carrinho:
            # Atualiza quantidade se produto já existe
            produto_no_carrinho['quantidade'] += quantidade
            produto_no_carrinho['subtotal'] = produto_no_carrinho['quantidade'] * produto_no_carrinho['preco']
        else:
            # Adiciona novo produto ao carrinho
            carrinho.append({
                'produto_id': produto_id,
                'nome': produto.nome,
                'preco': float(produto.preco),
                'quantidade': quantidade,
                'subtotal': quantidade * float(produto.preco),
                'imagem_url': produto.imagem_url
            })
        
        # Salva carrinho na sessão
        salvar_carrinho(carrinho)
        
        # Resposta baseada no tipo de requisição
        if request.is_json:
            total_itens = sum(item['quantidade'] for item in carrinho)
            return jsonify({
                'success': True,
                'message': 'Produto adicionado ao carrinho!',
                'total_itens': total_itens
            })
        else:
            flash('Produto adicionado ao carrinho!', 'success')
            return redirect(url_for('index'))
            
    except Exception as e:
        # Tratamento de erros
        if request.is_json:
            return jsonify({'error': str(e)}), 500
        flash(f'Erro ao adicionar produto: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/carrinho')
def carrinho():
    """
    Rota para exibir o carrinho de compras
    """
    carrinho = obter_carrinho()
    total = calcular_total_carrinho(carrinho)
    
    return render_template('carrinho.html', 
                         carrinho=carrinho, 
                         total=total)

@app.route('/remover_carrinho/<int:produto_id>')
def remover_carrinho(produto_id):
    """
    Rota para remover um produto do carrinho
    """
    carrinho = obter_carrinho()
    
    # Remove o produto do carrinho
    carrinho = [item for item in carrinho if item['produto_id'] != produto_id]
    
    salvar_carrinho(carrinho)
    flash('Produto removido do carrinho!', 'info')
    
    return redirect(url_for('carrinho'))

@app.route('/atualizar_quantidade', methods=['POST'])
def atualizar_quantidade():
    """
    Rota para atualizar quantidade de um produto no carrinho via AJAX
    """
    try:
        dados = request.get_json()
        produto_id = dados.get('produto_id')
        nova_quantidade = dados.get('quantidade')
        
        if nova_quantidade <= 0:
            return jsonify({'error': 'Quantidade deve ser maior que zero'}), 400
        
        carrinho = obter_carrinho()
        
        # Encontra e atualiza o produto
        for item in carrinho:
            if item['produto_id'] == produto_id:
                # Verifica estoque
                produto = Produto.query.get(produto_id)
                if produto.estoque < nova_quantidade:
                    return jsonify({'error': 'Estoque insuficiente'}), 400
                
                item['quantidade'] = nova_quantidade
                item['subtotal'] = nova_quantidade * item['preco']
                break
        
        salvar_carrinho(carrinho)
        total = calcular_total_carrinho(carrinho)
        
        return jsonify({
            'success': True,
            'novo_total': total
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/checkout')
def checkout():
    """
    Rota para página de checkout/finalização do pedido
    """
    carrinho = obter_carrinho()
    
    if not carrinho:
        flash('Carrinho vazio!', 'warning')
        return redirect(url_for('index'))
    
    total = calcular_total_carrinho(carrinho)
    
    return render_template('checkout.html', 
                         carrinho=carrinho, 
                         total=total)

@app.route('/finalizar_pedido', methods=['POST'])
def finalizar_pedido():
    """
    Rota para finalizar o pedido e enviar para WhatsApp
    """
    try:
        carrinho = obter_carrinho()
        
        if not carrinho:
            flash('Carrinho vazio!', 'warning')
            return redirect(url_for('index'))
        
        # Coleta dados do formulário
        pedido_dados = {
            'nome': request.form.get('nome'),
            'telefone': request.form.get('telefone'),
            'endereco': request.form.get('endereco'),
            'observacoes': request.form.get('observacoes', '')
        }
        
        # Validação básica
        if not all([pedido_dados['nome'], pedido_dados['telefone'], pedido_dados['endereco']]):
            flash('Todos os campos são obrigatórios!', 'error')
            return redirect(url_for('checkout'))
        
        # Gera mensagem para WhatsApp
        mensagem = gerar_mensagem_whatsapp(pedido_dados, carrinho)
        
        # Número do WhatsApp (com código do país)
        numero_whatsapp = "5511970603441"  # +55 11 970603441
        
        # Encode da mensagem para URL
        mensagem_encoded = urllib.parse.quote(mensagem)
        
        # URL do WhatsApp
        whatsapp_url = f"https://wa.me/{numero_whatsapp}?text={mensagem_encoded}"
        
        # Salva o pedido no banco de dados (opcional)
        valor_total = calcular_total_carrinho(carrinho)
        
        novo_pedido = Pedido(
            nome_cliente=pedido_dados['nome'],
            telefone_cliente=pedido_dados['telefone'],
            endereco_cliente=pedido_dados['endereco'],
            valor_total=valor_total,
            observacoes=pedido_dados['observacoes']
        )
        
        db.session.add(novo_pedido)
        db.session.commit()
        
        # Adiciona os itens do pedido
        for item in carrinho:
            item_pedido = ItemPedido(
                pedido_id=novo_pedido.id,
                produto_id=item['produto_id'],
                quantidade=item['quantidade'],
                preco_unitario=item['preco']
            )
            db.session.add(item_pedido)
        
        db.session.commit()
        
        # Limpa o carrinho
        session.pop('carrinho', None)
        
        # Renderiza página de confirmação com link do WhatsApp
        return render_template('pedido_confirmado.html', 
                             whatsapp_url=whatsapp_url,
                             pedido=novo_pedido)
        
    except Exception as e:
        flash(f'Erro ao processar pedido: {str(e)}', 'error')
        return redirect(url_for('checkout'))

@app.route('/admin')
def admin():
    """
    Rota para área administrativa (lista de pedidos)
    """
    pedidos = Pedido.query.order_by(Pedido.data_pedido.desc()).all()
    return render_template('admin.html', pedidos=pedidos)

# CONTEXT PROCESSORS
# =====================================================
@app.context_processor
def inject_carrinho_info():
    """
    Context processor - disponibiliza informações do carrinho em todos os templates
    
    Conceito: Context processors são funções que executam antes de renderizar
    qualquer template, permitindo adicionar variáveis globais
    """
    carrinho = obter_carrinho()
    return {
        'carrinho_total_itens': sum(item['quantidade'] for item in carrinho)
    }

# FILTROS PERSONALIZADOS PARA TEMPLATES
# =====================================================
@app.template_filter('currency')
def currency_filter(value):
    """
    Filtro personalizado para formatar valores como moeda brasileira
    
    Uso no template: {{ produto.preco|currency }}
    """
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# FUNÇÃO PARA INICIALIZAR O BANCO DE DADOS
# =====================================================
def init_db():
    """
    Função para inicializar o banco de dados com dados de exemplo
    """
    # Cria as tabelas
    db.create_all()
    
    # Verifica se já existem produtos
    if Produto.query.count() == 0:
        # Dados de exemplo baseados na sua adega
        produtos_exemplo = [
            # Cervejas
            {
                'nome': 'Cerveja Skol Lata 350ml',
                'descricao': 'Cerveja pilsen gelada, ideal para relaxar',
                'preco': 3.50,
                'categoria': 'cerveja',
                'estoque': 100,
                'imagem_url': '/static/images/skol.jpg'
            },
            {
                'nome': 'Cerveja Brahma Duplo Malte 350ml',
                'descricao': 'Cerveja encorpada com duplo malte',
                'preco': 4.20,
                'categoria': 'cerveja',
                'estoque': 80,
                'imagem_url': '/static/images/brahma.jpg'
            },
            {
                'nome': 'Cerveja Heineken Long Neck 330ml',
                'descricao': 'Cerveja premium importada holandesa',
                'preco': 6.90,
                'categoria': 'cerveja',
                'estoque': 60,
                'imagem_url': '/static/images/heineken.jpg'
            },
            # Vinhos
            {
                'nome': 'Vinho Tinto Seco 750ml',
                'descricao': 'Vinho tinto nacional seco, harmoniza com carnes',
                'preco': 25.90,
                'categoria': 'vinho',
                'estoque': 30,
                'imagem_url': '/static/images/vinho_tinto.jpg'
            },
            {
                'nome': 'Vinho Branco Suave 750ml',
                'descricao': 'Vinho branco suave, perfeito para peixes',
                'preco': 28.50,
                'categoria': 'vinho',
                'estoque': 25,
                'imagem_url': '/static/images/vinho_branco.jpg'
            },
            # Destilados
            {
                'nome': 'Cachaça Artesanal 670ml',
                'descricao': 'Cachaça artesanal premium envelhecida',
                'preco': 35.00,
                'categoria': 'destilados',
                'estoque': 20,
                'imagem_url': '/static/images/cachaca.jpg'
            },
            {
                'nome': 'Vodka Premium 1L',
                'descricao': 'Vodka premium importada, pura e suave',
                'preco': 45.90,
                'categoria': 'destilados',
                'estoque': 15,
                'imagem_url': '/static/images/vodka.jpg'
            },
            # Refrigerantes e Água
            {
                'nome': 'Coca-Cola Lata 350ml',
                'descricao': 'Refrigerante de cola gelado',
                'preco': 4.00,
                'categoria': 'refrigerante',
                'estoque': 120,
                'imagem_url': '/static/images/coca.jpg'
            },
            {
                'nome': 'Água Mineral 500ml',
                'descricao': 'Água mineral natural sem gás',
                'preco': 2.50,
                'categoria': 'agua',
                'estoque': 150,
                'imagem_url': '/static/images/agua.jpg'
            }
        ]
        
        # Adiciona produtos ao banco
        for produto_data in produtos_exemplo:
            produto = Produto(**produto_data)
            db.session.add(produto)
        
        # Salva no banco
        db.session.commit()
        print("Banco de dados inicializado com produtos de exemplo!")

# PONTO DE ENTRADA DA APLICAÇÃO
# =====================================================
if __name__ == '__main__':
    # Cria contexto da aplicação para operações de banco
    with app.app_context():
        init_db()
    
    # Inicia o servidor de desenvolvimento
    # debug=True: Recarrega automaticamente quando há mudanças no código
    # host='0.0.0.0': Permite acesso de outros dispositivos na rede
    # port=5000: Porta onde a aplicação vai rodar
    app.run(debug=True, host='0.0.0.0', port=5000)
