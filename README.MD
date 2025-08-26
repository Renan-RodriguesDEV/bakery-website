# Sistema de Gerenciamento de Padaria 🥖

Sistema web desenvolvido em Python usando Streamlit para gerenciamento de uma padaria, com funcionalidades para clientes e funcionários/proprietários.

## 🛠️ Tecnologias Utilizadas

- Python 3.8+
- Streamlit 1.41.1
- PostgreSQL (Neon.tech ou outro host gratuito)
- SQLAlchemy
- Pandas
- MercadoPago API
- RabbitMQ (pika) — fila de mensagens para notificações e processamento assíncrono

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
- Processamento assíncrono e notificações via RabbitMQ

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

3. Configure as variáveis de ambiente no arquivo `secrets.toml` (veja exemplo abaixo)
4. Crie o banco de dados PostgreSQL (recomendado Neon.tech, Railway, Supabase ou ElephantSQL)
5. Configure uma instância RabbitMQ (ex.: CloudAMQP) e defina a URL no `secrets.toml` (link: https://customer.cloudamqp.com/instance/)
6. Execute o aplicativo:

```bash
streamlit run main/app.py
```

## 🔐 Variáveis de Ambiente Necessárias

```toml
USER = "email@exemplo.com"
PASSWORD = "sua_senha"
ACESS_TOKEN = "token_mercado_pago"
PIX_KEY = "sua_chave_pix"
TOKEN_TELEGRAM = "seu_token_telegram"

# RabbitMQ (pika) - exemplo de URL amqps
# Exemplo CloudAMQP: amqps://usuario:senha@hostname/vhost
RABBITMQ_URL = "amqps://usuario:senha@host/vhost"

# Dados do banco PostgreSQL
TEST_USER_DB = "usuario_db"  # (opcional, se usar DATABASE_URL)
TEST_DATABASE_NAME = "nome_banco"  # (opcional)
TEST_HOST_DB = "host_postgres"  # (opcional)
TEST_PASSWORD_DB = "senha_db"  # (opcional)
DATABASE_URL = "postgresql://usuario:senha@host:porta/nome_banco?sslmode=require"
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

Developer: Renan Rodrigues [(@rodrigues_renan)](https://instagram.com/rodrigues_renan)
