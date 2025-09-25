# 🧪 Como Testar o Sistema da Adega

Este guia te ajudará a testar todas as funcionalidades do sistema passo a passo.

## 🚀 Iniciando o Sistema

### 1. Instalar Dependências
```bash
# Abrir terminal no diretório C:\Adega
cd C:\Adega

# Instalar as dependências
pip install -r requirements.txt
```

### 2. Executar a Aplicação
```bash
python app.py
```

### 3. Acessar o Sistema
- Abra seu navegador
- Acesse: `http://localhost:5000`
- Você deve ver a página inicial da adega

## 🧪 Roteiro de Testes

### Teste 1: Página Inicial
**Objetivo:** Verificar se a página carrega corretamente

✅ **Verificar:**
- [ ] Página carrega sem erros
- [ ] Logo "Adega Rádio Tatuapé FM" aparece
- [ ] Menu de navegação está funcionando
- [ ] Produtos são exibidos em cards
- [ ] Filtros de categoria funcionam
- [ ] Badge do carrinho mostra "0"

### Teste 2: Adicionar Produtos ao Carrinho
**Objetivo:** Testar funcionalidade do carrinho

✅ **Passos:**
1. Escolha um produto (ex: Cerveja Skol)
2. Altere a quantidade para 2
3. Clique no botão "+" (adicionar ao carrinho)
4. Observe:
   - [ ] Notificação de sucesso aparece
   - [ ] Badge do carrinho atualiza para "2"
   - [ ] Produto é adicionado

**Repita com outros produtos para testar o carrinho com múltiplos itens**

### Teste 3: Página do Carrinho
**Objetivo:** Verificar funcionalidades do carrinho

✅ **Passos:**
1. Clique no ícone do carrinho no menu
2. Verificar:
   - [ ] Produtos adicionados estão listados
   - [ ] Quantidades estão corretas
   - [ ] Preços calculados corretamente
   - [ ] Total está correto
   - [ ] Botões +/- alteram quantidades
   - [ ] Botão remover funciona

### Teste 4: Página de Checkout
**Objetivo:** Testar formulário de finalização

✅ **Passos:**
1. No carrinho, clique em "Finalizar Pedido"
2. Preencher formulário:
   - **Nome:** João Silva
   - **Telefone:** (11) 99999-9999
   - **Endereço:** Rua das Flores, 123, Centro, São Paulo
   - **Observações:** Entregar após 18h
3. Marcar "Aceito os termos"
4. Clicar em "Enviar Pedido via WhatsApp"

✅ **Verificar:**
- [ ] Validações do formulário funcionam
- [ ] Campos obrigatórios são validados
- [ ] Máscara do telefone funciona
- [ ] Resumo do pedido está correto
- [ ] Chave PIX pode ser copiada

### Teste 5: Confirmação do Pedido
**Objetivo:** Verificar página de sucesso

✅ **Verificar:**
- [ ] Página de confirmação aparece
- [ ] Dados do pedido estão corretos
- [ ] Link do WhatsApp está funcionando
- [ ] Chave PIX pode ser copiada
- [ ] Instruções de pagamento estão claras

### Teste 6: Integração WhatsApp
**Objetivo:** Testar envio para WhatsApp

✅ **Passos:**
1. Na página de confirmação, clique em "Abrir WhatsApp"
2. Verificar:
   - [ ] WhatsApp abre (ou WhatsApp Web)
   - [ ] Número correto: +55 11 970603441
   - [ ] Mensagem está formatada corretamente
   - [ ] Contém todos os dados do pedido
   - [ ] Instruções de pagamento incluídas

### Teste 7: Painel Administrativo
**Objetivo:** Verificar área administrativa

✅ **Passos:**
1. Acesse: `http://localhost:5000/admin`
2. Verificar:
   - [ ] Lista de pedidos aparece
   - [ ] Pedidos recentes estão listados
   - [ ] Informações dos pedidos estão completas

## 📱 Testes Mobile

### Responsividade
**Objetivo:** Verificar funcionamento em mobile

✅ **Passos:**
1. Redimensionar janela do navegador (ou usar F12 → Device Mode)
2. Testar todas as funcionalidades acima em diferentes tamanhos
3. Verificar:
   - [ ] Layout adapta-se à tela pequena
   - [ ] Botões são tocáveis
   - [ ] Formulários são usáveis
   - [ ] Tabelas são scrolláveis horizontalmente

## 🐛 Possíveis Problemas e Soluções

### Erro: "ModuleNotFoundError"
**Solução:**
```bash
pip install -r requirements.txt
```

### Erro: "Port already in use"
**Solução:**
- Matar processo na porta 5000 ou
- Alterar porta no `app.py`: `app.run(port=5001)`

### WhatsApp não abre
**Possíveis causas:**
- WhatsApp não instalado no PC
- Usar WhatsApp Web como alternativa
- Testar em dispositivo mobile

### Imagens não aparecem
**Solução:**
- Imagens padrão não foram criadas
- Adicionar imagens na pasta `static/images/`
- Usar URLs de imagens online temporariamente

## 🎯 Cenários de Teste Avançados

### Teste de Estoque
1. Tente adicionar mais produtos do que o estoque disponível
2. Verificar se sistema bloqueia e mostra erro

### Teste de Validação
1. Tente enviar formulário com campos vazios
2. Teste telefone com formato incorreto
3. Verificar se validações funcionam

### Teste de Sessão
1. Adicione produtos ao carrinho
2. Feche o navegador e abra novamente
3. Verificar se carrinho persiste (em sessão ativa)

## 📊 Dados de Teste

### Produtos Padrão Criados:
- Cerveja Skol Lata 350ml - R$ 3,50
- Cerveja Brahma Duplo Malte 350ml - R$ 4,20
- Cerveja Heineken Long Neck 330ml - R$ 6,90
- Vinho Tinto Seco 750ml - R$ 25,90
- Vinho Branco Suave 750ml - R$ 28,50
- Cachaça Artesanal 670ml - R$ 35,00
- Vodka Premium 1L - R$ 45,90
- Coca-Cola Lata 350ml - R$ 4,00
- Água Mineral 500ml - R$ 2,50

### Dados de Teste para Formulário:
```
Nome: Maria da Silva
Telefone: (11) 98765-4321
Endereço: Av. Paulista, 1000, Bela Vista, São Paulo/SP, CEP: 01310-100
Observações: Interfone 25B, entregar após 19h
```

## 🔍 Logs para Verificar

Observar no terminal onde a aplicação está rodando:
- Requisições HTTP
- Erros de banco de dados
- Mensagens de debug
- Criação de pedidos

## ✅ Checklist Final

Antes de considerar o teste concluído:

- [ ] Todos os produtos podem ser adicionados ao carrinho
- [ ] Carrinho calcula totais corretamente
- [ ] Formulário de checkout funciona completamente
- [ ] WhatsApp é aberto com mensagem correta
- [ ] Pedidos aparecem no painel admin
- [ ] Sistema funciona em mobile
- [ ] Não há erros no console do navegador
- [ ] Chave PIX pode ser copiada

## 🎓 Para Aprendizado

Enquanto testa, observe:

1. **No Backend (Terminal):**
   - Como Flask processa as requisições
   - Criação de registros no banco de dados
   - Logs de debug e erros

2. **No Frontend (DevTools F12):**
   - Requisições AJAX no Network tab
   - JavaScript logs no Console
   - HTML/CSS no Elements tab

3. **No Código:**
   - Como dados fluem entre templates e views
   - Como sessões mantêm estado do carrinho
   - Como formulários são validados

## 🎉 Próximos Passos

Após testar tudo com sucesso:

1. **Personalizar:** Adicione seus próprios produtos
2. **Modificar:** Altere cores, logos, informações
3. **Expandir:** Adicione novas funcionalidades
4. **Deploy:** Coloque online para uso real

---

**Divirta-se testando e aprendendo! 🚀**
