-- Cria o banco de dados
CREATE DATABASE IF NOT EXISTS db_comercio;
USE db_comercio;
-- Tabela clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(11) DEFAULT NULL,
    telefone VARCHAR(15) DEFAULT NULL,
    email VARCHAR(255) DEFAULT NULL
);
-- Tabela produtos
CREATE TABLE IF NOT EXISTS produtos (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    preco DECIMAL(15, 2) NOT NULL,
    estoque INT NOT NULL
);
-- Tabela de usuarios do sistema
CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) not null,
    senha VARCHAR(8) not null
);
-- Tabela intermediária cliente_produto para registrar compras
CREATE TABLE IF NOT EXISTS cliente_produto (
    id_cliente INT NOT NULL,
    id_produto INT NOT NULL,
    preco DECIMAL(15, 2) NOT NULL,
    quantidade INT NOT NULL,
    total decimal(15, 2) NOT NULL default 0,
    data datetime NOT NULL default NOW(),
    PRIMARY KEY (id_cliente, id_produto),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    FOREIGN KEY (id_produto) REFERENCES produtos(id)
);
drop table cliente_produto;
-- Trigger para atualizar o estoque de produtos quando a quantidade for alterada
-- DELIMITER // CREATE TRIGGER atualiza_estoque_cliente_produto
-- AFTER
-- INSERT ON cliente_produto FOR EACH ROW BEGIN -- Atualiza o estoque do produto
-- UPDATE produtos
-- SET estoque = estoque - NEW.quantidade
-- WHERE id = NEW.id_produto;
-- END // DELIMITER;
-- DELIMITER // create trigger atualiza_preco_total
-- after
-- insert on cliente_produto for each row begin
-- update cliente_produto c
-- set total = NEW.quantidade * NEW.preco
-- where id_produto = NEW.id_produto
--     and id_cliente;
-- end // DELIMITER;