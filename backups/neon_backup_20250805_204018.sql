INSERT INTO users
VALUES (
        1,
        'Renan de Souza Rodrigues',
        'dev.rodrigues.renan@gmail.com',
        '$2b$12$kwccQcNogtU6/2vEwvF1q.nKp005EGq0m8P6bVMkXO.tpTXo3sJFa'
    );
INSERT INTO clientes
VALUES (
        1,
        'Renan de Souza Rodrigues',
        '45671967830',
        '$2b$12$RPvKKNn8LKblEP1t9WovUu0xgFhSyDBOBnTtJJYTc4Fl6GkNib.F2',
        '19998722472',
        'renanrodrigues7110@gmail.com',
        None,
        True
    );
INSERT INTO clientes
VALUES (
        2,
        'Jefferson Rodrigues da Silva',
        '29921637835',
        '$2b$12$S8B65Ak.fBwnVlGlvC4YweVsdIWEl0xJHgwA0xLo3812v/0hPG4f2',
        '14 997526985',
        'jeffersonrodrigues7110@gmail.com',
        None,
        True
    );
INSERT INTO clientes
VALUES (
        3,
        'Sr. Teste Supremo',
        '11122233344',
        '$2b$12$C4H1zsTCgy/Rfj3zGKz2IumTCcLWZ6.Us/5ve6Mw7QdRx5m5pG8JS',
        '19998722472',
        'renan.rodrigues@ead.eduvaleavare.com.br',
        None,
        True
    );
INSERT INTO cliente_produto
VALUES (
        1,
        2,
        1,
        Decimal('13.00'),
        3,
        Decimal('39.00'),
        datetime.datetime(2025, 8, 1, 16, 44, 40, 733944)
    );
INSERT INTO cliente_produto
VALUES (
        2,
        1,
        1,
        Decimal('13.00'),
        10,
        Decimal('130.00'),
        datetime.datetime(2025, 8, 5, 9, 49, 28, 63735)
    );
INSERT INTO cliente_produto
VALUES (
        4,
        3,
        19,
        Decimal('100.00'),
        96,
        Decimal('9600.00'),
        datetime.datetime(2025, 8, 5, 22, 51, 52, 40766)
    );
INSERT INTO produtos
VALUES (
        2,
        'Conquista 2L',
        Decimal('6.00'),
        'Bebidas',
        1000
    );
INSERT INTO produtos
VALUES (
        4,
        'P�o de forma panco (500g)',
        Decimal('9.90'),
        'Padaria',
        500
    );
INSERT INTO produtos
VALUES (
        5,
        'Brahma lata 350ml (Uni.)',
        Decimal('5.00'),
        'Bebidas',
        1000
    );
INSERT INTO produtos
VALUES (
        6,
        'Skol lata 350ml (Uni.)',
        Decimal('5.00'),
        'Bebidas',
        999
    );
INSERT INTO produtos
VALUES (
        7,
        'Ant�rtica lata 350ml (Uni.)',
        Decimal('5.00'),
        'Bebidas',
        1000
    );
INSERT INTO produtos
VALUES (
        8,
        'Crystal lata 350ml (Uni.)',
        Decimal('3.50'),
        'Bebidas',
        1000
    );
INSERT INTO produtos
VALUES (
        9,
        'Caixinha de Crystal (12x) ',
        Decimal('42.00'),
        'Bebidas',
        1000
    );
INSERT INTO produtos
VALUES (
        10,
        'Caixinha de Brahma (12x) ',
        Decimal('60.00'),
        'Bebidas',
        1000
    );
INSERT INTO produtos
VALUES (
        11,
        'Caixinha de Skol (12x) ',
        Decimal('60.00'),
        'Bebidas',
        1000
    );
INSERT INTO produtos
VALUES (
        12,
        'Caixinha de Ant�rtica (12x) ',
        Decimal('60.00'),
        'Bebidas',
        1000
    );
INSERT INTO produtos
VALUES (13, 'Leite 1L', Decimal('6.50'), 'Bebidas', 1000);
INSERT INTO produtos
VALUES (
        14,
        'Sonho de padaria (Creme e outros)',
        Decimal('4.50'),
        'Padaria',
        1000
    );
INSERT INTO produtos
VALUES (
        15,
        'Rosca doce (Creme e outros)',
        Decimal('9.90'),
        'Doces',
        1000
    );
INSERT INTO produtos
VALUES (16, 'Coxinha', Decimal('6.00'), 'Salgados', 1000);
INSERT INTO produtos
VALUES (
        3,
        'P�o franc�s  (Uni.)',
        Decimal('0.90'),
        'Padaria',
        1000
    );
INSERT INTO produtos
VALUES (
        17,
        'Esfirra salgada',
        Decimal('5.00'),
        'Salgados',
        1000
    );
INSERT INTO produtos
VALUES (
        1,
        'Coca Cola 2L',
        Decimal('13.00'),
        'Bebidas',
        971
    );
INSERT INTO produtos
VALUES (
        19,
        'Super p�o de forma 1kg',
        Decimal('100.00'),
        'Padaria',
        0
    );
INSERT INTO dividas
VALUES (
        1,
        2,
        Decimal('39.00'),
        Decimal('0.00'),
        True,
        datetime.datetime(2025, 8, 1, 18, 4, 27)
    );
INSERT INTO dividas
VALUES (
        2,
        1,
        Decimal('130.00'),
        Decimal('30.00'),
        True,
        datetime.datetime(2025, 8, 5, 10, 4, 31)
    );
INSERT INTO dividas
VALUES (
        3,
        3,
        Decimal('9600.00'),
        Decimal('0.00'),
        True,
        datetime.datetime(2025, 8, 5, 10, 12, 41)
    );