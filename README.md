# 🍷 Adega Rádio Tatuapé FM - Sistema de Pedidos

Um sistema completo de pedidos online para adega, desenvolvido com Flask e Bootstrap, integrando pagamento PIX e entrega via WhatsApp.

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Funcionalidades](#-funcionalidades)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Conceitos Educativos](#-conceitos-educativos)
- [API Endpoints](#-api-endpoints)
- [Contribuição](#-contribuição)

## 🎯 Sobre o Projeto

Este projeto é um sistema educativo completo de e-commerce para uma adega, desenvolvido especialmente para estudo. Cada parte do código contém comentários detalhados explicando conceitos de programação web, desde o básico até funcionalidades avançadas.

### Características Principais:
- **100% Educativo**: Código amplamente comentado para aprendizado
- **Responsivo**: Funciona perfeitamente em desktop e mobile
- **Integração WhatsApp**: Pedidos enviados diretamente via WhatsApp
- **Pagamento PIX**: Sistema integrado de pagamento via PIX
- **Interface Moderna**: Design clean e profissional com Bootstrap 5

## 🚀 Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **Flask** - Framework web principal
- **SQLAlchemy** - ORM para banco de dados
- **Flask-Migrate** - Migrações de banco de dados
- **SQLite** - Banco de dados (desenvolvimento)

### Frontend
- **HTML5** - Estrutura das páginas
- **CSS3** - Estilização personalizada
- **Bootstrap 5** - Framework CSS responsivo
- **JavaScript ES6+** - Funcionalidades interativas
- **Font Awesome** - Ícones vetoriais

### Integrações
- **WhatsApp Web API** - Envio de pedidos
- **PIX** - Sistema de pagamento brasileiro

## ✨ Funcionalidades

### 🛍️ Para Clientes
- [x] Catálogo de produtos com filtros por categoria
- [x] Carrinho de compras dinâmico
- [x] Cálculo automático de totais
- [x] Formulário de checkout com validação
- [x] Envio de pedidos via WhatsApp
- [x] Integração com pagamento PIX
- [x] Interface responsiva para mobile

### 👨‍💼 Para Administradores
- [x] Lista de pedidos recebidos
- [x] Controle de estoque
- [x] Gerenciamento de produtos
- [x] Dashboard administrativo

### 🎨 Interface
- [x] Design moderno e profissional
- [x] Animações suaves
- [x] Notificações toast
- [x] Loading indicators
- [x] Breadcrumbs de navegação

## 🔧 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a Passo

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd Adega
```

2. **Crie um ambiente virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados**
```bash
# O banco será criado automaticamente na primeira execução
```

5. **Execute a aplicação**
```bash
python app.py
```

6. **Acesse no navegador**
```
http://localhost:5000
```

## 💡 Como Usar

### Para Clientes

1. **Navegue pelo catálogo** - Veja todos os produtos disponíveis
2. **Filtre por categoria** - Use os filtros para encontrar o que precisa
3. **Adicione ao carrinho** - Clique no botão "+" para adicionar produtos
4. **Revise o carrinho** - Verifique quantidades e valores
5. **Faça o checkout** - Preencha seus dados de entrega
6. **Envie via WhatsApp** - Clique para abrir o WhatsApp com o pedido
7. **Efetue o pagamento** - Use a chave PIX fornecida
8. **Envie o comprovante** - No mesmo chat do WhatsApp

### Para Administradores

1. **Acesse /admin** - Veja lista de pedidos
2. **Gerencie produtos** - Adicione/edite produtos
3. **Controle estoque** - Monitore quantidades disponíveis

## 📁 Estrutura do Projeto

```
Adega/
│
├── app.py                      # Aplicação Flask principal
├── requirements.txt            # Dependências do projeto
├── README.md                   # Esta documentação
│
├── templates/                  # Templates HTML
│   ├── base.html              # Template base
│   ├── index.html             # Página inicial
│   ├── carrinho.html          # Carrinho de compras
│   ├── checkout.html          # Finalização do pedido
│   └── pedido_confirmado.html # Confirmação do pedido
│
├── static/                     # Arquivos estáticos
│   ├── css/
│   │   └── style.css          # Estilos personalizados
│   ├── js/
│   │   └── app.js             # JavaScript principal
│   └── images/                # Imagens dos produtos
│
└── instance/                   # Banco de dados (criado automaticamente)
    └── adega.db
```

## 📚 Conceitos Educativos

Este projeto foi desenvolvido com foco educativo. Aqui estão os principais conceitos abordados:

### 🐍 Python/Flask
- **Arquitetura MVC** - Separação de responsabilidades
- **ORMs** - SQLAlchemy para banco de dados
- **Roteamento** - Definição de URLs e endpoints
- **Templates** - Sistema de templates Jinja2
- **Sessões** - Gerenciamento de sessões de usuário
- **Flash Messages** - Sistema de mensagens temporárias
- **Context Processors** - Dados globais para templates

### 🎨 Frontend
- **HTML Semântico** - Estrutura adequada dos documentos
- **CSS Grid/Flexbox** - Layout responsivo moderno
- **Bootstrap** - Framework CSS profissional
- **JavaScript ES6+** - Programação moderna
- **AJAX/Fetch** - Requisições assíncronas
- **DOM Manipulation** - Interação com elementos da página

### 🗄️ Banco de Dados
- **Relacionamentos** - One-to-Many, Many-to-Many
- **Migrations** - Controle de versão do banco
- **Queries** - Consultas eficientes
- **Constraints** - Integridade dos dados

### 🌐 APIs e Integrações
- **RESTful APIs** - Padrões de API REST
- **WhatsApp Integration** - Integração com WhatsApp Web
- **Payment Integration** - Sistema de pagamento PIX
- **Error Handling** - Tratamento de erros robusto

## 🔗 API Endpoints

### Produtos
- `GET /` - Lista todos os produtos
- `GET /produto/<id>` - Detalhes de um produto específico

### Carrinho
- `POST /adicionar_carrinho` - Adiciona produto ao carrinho
- `GET /carrinho` - Exibe carrinho de compras
- `GET /remover_carrinho/<id>` - Remove produto do carrinho
- `POST /atualizar_quantidade` - Atualiza quantidade no carrinho

### Pedidos
- `GET /checkout` - Página de finalização
- `POST /finalizar_pedido` - Processa o pedido
- `GET /admin` - Dashboard administrativo

## 🛠️ Personalização

### Adicionando Produtos
```python
# No app.py, modifique a função init_db()
produtos_exemplo.append({
    'nome': 'Nome do Produto',
    'descricao': 'Descrição detalhada',
    'preco': 10.50,
    'categoria': 'categoria',
    'estoque': 100,
    'imagem_url': '/static/images/produto.jpg'
})
```

### Modificando Estilos
```css
/* Em static/css/style.css */
:root {
    --adega-primary: #2c5530;    /* Cor principal */
    --adega-secondary: #8b4513;  /* Cor secundária */
    --adega-accent: #daa520;     /* Cor de destaque */
}
```

### Configurando WhatsApp
```python
# Em app.py, modifique:
numero_whatsapp = "5511970603441"  # Seu número
PIX_EMAIL = "seuemail@gmail.com"   # Sua chave PIX
```

## 🚀 Deploy em Produção

### Preparação
1. **Configure variáveis de ambiente**
```bash
export FLASK_ENV=production
export DATABASE_URL=postgresql://user:pass@host:port/db
```

2. **Use um banco mais robusto**
```python
# PostgreSQL recomendado para produção
DATABASE_URI = os.environ.get('DATABASE_URL')
```

3. **Configure um servidor web**
```bash
# Gunicorn recomendado
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Plataformas Recomendadas
- **Heroku** - Deploy fácil e gratuito
- **DigitalOcean** - VPS com mais controle
- **AWS/Azure** - Para aplicações enterprise

## 📱 Recursos Mobile

- ✅ Layout responsivo
- ✅ Touch-friendly buttons
- ✅ Mobile-optimized forms
- ✅ WhatsApp deep linking
- ✅ PWA capabilities (pode ser adicionado)

## 🔒 Segurança

- ✅ CSRF Protection (Flask-WTF)
- ✅ SQL Injection Protection (SQLAlchemy)
- ✅ Input validation
- ✅ Secure sessions
- ⚠️ **Para produção**: Adicione HTTPS, rate limiting, etc.

## 🤝 Contribuição

Este é um projeto educativo! Contribuições são bem-vindas:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Contato

**Adega Rádio Tatuapé FM**
- 📱 WhatsApp: (11) 97060-3441
- 📧 Email: radiotatuapefm@gmail.com
- 📍 Endereço: Vila Regente Feijó - São Paulo/SP

## 📄 Licença

Este projeto é desenvolvido para fins educativos. Sinta-se livre para usar, modificar e distribuir.

---

### 🎓 Para Estudantes

Este projeto é perfeito para quem está aprendendo:

- **Iniciantes**: Foque nos templates HTML e CSS básico
- **Intermediários**: Estude as rotas Flask e JavaScript
- **Avançados**: Analise a arquitetura completa e integrações

Cada arquivo contém comentários detalhados explicando o que cada código faz e por quê. Use como referência para seus próprios projetos!

---

**Desenvolvido com ❤️ para fins educativos**
