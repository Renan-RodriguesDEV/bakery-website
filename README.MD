# Sistema de Gerenciamento de Padaria 🥖

Sistema web desenvolvido em Python usando Streamlit para gerenciamento de uma padaria, com funcionalidades para clientes e funcionários/proprietários.

## 🛠️ Tecnologias Utilizadas

- Python 3.8+
- Streamlit 1.41.1
- MySQL/MariaDB
- SQLAlchemy
- Pandas
- MercadoPago API

## 📋 Funcionalidades

### Área do Cliente

- Login/Cadastro de clientes
- Catálogo de produtos
- Carrinho de compras
- Histórico de compras
- Consulta de pendências/dívidas
- Pagamento via PIX/MercadoPago
- Reset de senha via email
- Suporte ao usuário

### Área do Proprietário/Funcionário

- Gerenciamento de produtos
- Gerenciamento de clientes
- Controle de estoque
- Gestão de dívidas
- Relatórios de vendas
- Visualização de feedbacks

## 🗄️ Estrutura do Banco de Dados

- Produtos
- Clientes
- Vendas
- Carrinho
- Dívidas
- Usuários (Funcionários)

## 💻 Como Executar

1. Clone o repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente no arquivo secrets.toml
4. Execute o aplicativo:

```bash
streamlit run main/app.py
```

## 🔐 Variáveis de Ambiente Necessárias

```toml
USER = "email@exemplo.com"
PASSWORD = "sua_senha"
ACESS_TOKEN = "token_mercado_pago"
TEST_USER_DB = "usuario_db"
TEST_DATABASE_NAME = "nome_banco"
TEST_HOST_DB = "localhost"
TEST_PASSWORD_DB = "senha_db"
PIX_KEY = "sua_chave_pix"
```

## 🎨 Customização

O tema da aplicação pode ser customizado através do arquivo config.toml:

```toml
[theme]
base = "dark"
primaryColor = "#DAA520"  # GoldenRod
secondaryBackgroundColor = "#8B4513"  # SaddleBrown
textColor = "#FFFFFF"
```

## 📱 Preview da Interface

- Interface responsiva
- Tema escuro por padrão
- Cores personalizadas
- Ícones intuitivos
- Mapa de localização integrado

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## 📄 Licença

Este projeto está sob a licença MIT.

---

Desenvolvido com ❤️ por Renan Rodrigues [(@_little_renan_.py)](https://instagram.com/__little_renan__.py)
