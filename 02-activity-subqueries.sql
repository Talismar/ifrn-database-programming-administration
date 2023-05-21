/*
    1. Crie uma consulta que mostre o estado e a quantidade de cidades de cada
       estado que a empresa tem clientes.
*/

SELECT uf, COUNT("cidade") AS amount_city FROM cliente GROUP BY cliente.uf ORDER BY COUNT(cidade) ASC;

/*
    2. Crie uma consulta que será o ranking de vendas da empresa. Neste ranking
       deverá ser exibido o código do vendedor, bem como a quantidade de vendas
       efetuadas por cada vendedor. Lembre-se que em um ranking o vendedor que
       efetuou o maior número de vendas (pedidos), deverá aparecer no topo da lista.
*/

SELECT cod_vendedor, COUNT("cod_vendedor") AS "quantidade_vendas" FROM pedido GROUP BY pedido.cod_vendedor ORDER BY quantidade_vendas ASC;

/*
    3. Crie uma consulta que será o ranking de pedidos da empresa. Neste ranking
       deverá ser exibido o código do cliente, bem como a quantidade de pedidos
       efetuados por cada cliente. Lembre-se que em um ranking o cliente que
       efetuou o maior número de pedidos, deverá aparecer no topo da lista.
*/

SELECT cod_cliente, COUNT("cod_cliente") AS "quantidade_de_pedidos" FROM pedido GROUP BY pedido.cod_cliente ORDER BY quantidade_de_pedidos DESC;

/*
    4. Criar uma consulta que mostre o ano, o mês e a quantidade de pedidos em
       cada (ano/mês). A visão deverá ser ordenada pela quantidade de pedidos em
       cada ano/mês.
*/

SELECT extract(MON FROM data_pedido) AS month, extract(YEAR FROM data_pedido) AS year, COUNT(pedido) as pedidos
FROM pedido GROUP BY month, year ORDER BY pedidos;

/*
    5. Crie uma consulta que mostre a data dos pedidos, o nome do vendedor e o
       nome do cliente. Nesta relação deverá constar apenas os pedidos emitidos em
       agosto de 2015 e deve estar em ordem cronológica da data dos pedidos.
*/

SELECT data_pedido, vendedor.nome, cliente.nome FROM pedido
INNER JOIN cliente ON pedido.cod_cliente = cliente.cod_cliente
INNER JOIN vendedor ON pedido.cod_vendedor = vendedor.cod_vendedor
WHERE pedido.data_pedido BETWEEN '2015-08-01' AND '2015-08-31';

/*
    6. Os vendedores têm seus salários fixo acrescido de 10% da soma dos valores dos
       pedidos. Crie uma consulta que exiba o nome dos vendedores e o total de
       comissão desses funcionários.
*/

SELECT vendedor.cod_vendedor, (SUM(pro.valor_unitario * ip.quantidade)) * 0.1
FROM pedido p
INNER JOIN item_pedido ip ON(p.cod_pedido = ip.cod_pedido)
INNER JOIN produto pro on(ip.cod_produto = pro.cod_produto)
INNER JOIN vendedor ON(p.cod_vendedor = vendedor.cod_vendedor)
group by vendedor.cod_vendedor;

/*
    7. Crie uma consulta que contenha o nome do cliente e o total de pedidos que
       este já fez em toda sua história como cliente da loja. O nome de um cliente não
       deve ser repetido na relação. Ordene esta lista pelo total de pedidos efetuados
       pelo cliente.
*/

SELECT cliente.nome, COUNT(pedido) AS total_pedidos FROM pedido
INNER JOIN cliente ON (pedido.cod_cliente = cliente.cod_cliente)
GROUP BY cliente.nome ORDER BY total_pedidos DESC;

/*
    8. A diretoria da loja deseja saber quais são os produtos que geram a maior
       receita para o caixa da loja, bem como a quantidade de unidades vendidas.
       Para isso, é necessário criar uma visão contendo o código do produto, o nome
       do produto, a quantidade total vendida desde a abertura da loja, o valor
       unitário e o valor total obtido com as vendas deste produto. É importante
       lembrar que o produto não pode ser repetido na relação e que o ordenamento
       deve ser feito do produto que mais gerou receita para a loja para o que menos
       gerou, limitando-se aos produtos que foram vendidos.
*/

SELECT produto.cod_produto, produto.descricao, produto.valor_unitario,
SUM(item_pedido.quantidade) AS quantidade_items_vendidos, SUM(produto.valor_unitario * item_pedido.quantidade) AS valor_total_obtido
FROM pedido
INNER JOIN item_pedido ON pedido.cod_pedido = item_pedido.cod_pedido
INNER JOIN produto ON item_pedido.cod_produto = produto.cod_produto
GROUP BY produto.cod_produto ORDER BY valor_total_obtido DESC;

/* ########################## Sub-Consultas ################################ */
/*
    9. Crie uma consulta que exiba o nome, cidade e estado dos clientes que fizeram
       pelo menos um pedido em 2015. Ordene os resultados pelo nome dos clientes
       em ordem alfabética.
*/

SELECT nome, cidade, uf FROM cliente
WHERE cliente.cod_cliente IN (SELECT pedido.cod_cliente FROM pedido
                              GROUP BY pedido.cod_cliente, extract(YEAR FROM pedido.data_pedido)
                              HAVING COUNT(pedido) >= 1 AND extract(YEAR FROM pedido.data_pedido) = '2015')
ORDER BY cliente.nome;

/*
    10. Mostre a quantidade de pedidos realizados por clientes que moram no Rio
        Grande do Sul (RS) ou em Santa Catarina (SC).
*/

SELECT COUNT(pedido) as quantidade_pedidos FROM pedido WHERE pedido.cod_cliente IN
                                               (SELECT cliente.cod_cliente FROM cliente WHERE cliente.uf = 'RS' OR cliente.uf = 'SC');

/*
    11. Mostre o código, nome e valor unitário dos produtos que possuem pedidos
        com entrega prevista entre os dias 01/12/2014 e 31/01/2015. Ordene a lista
        pelo valor unitário decrescente dos produtos. - DONE
*/

SELECT * FROM produto
WHERE produto.cod_produto IN (
                            SELECT item_pedido.cod_produto FROM item_pedido
                            WHERE item_pedido.cod_pedido IN (
                                SELECT pedido.cod_pedido FROM pedido
                                                         WHERE pedido.prazo_entrega BETWEEN '2014-12-01' AND '2015-04-30'
                                )
                        )
ORDER BY produto.valor_unitario DESC;

/*
    12. Exiba os dados dos clientes que fizeram pedidos com mais de 10 itens,
        independente se forem produtos iguais ou diferentes. - DONE
*/

SELECT * FROM cliente INNER JOIN pedido ON cliente.cod_cliente = pedido.cod_cliente,
(SELECT item_pedido.cod_pedido, SUM(quantidade) FROM item_pedido GROUP BY cod_pedido HAVING SUM(quantidade) > 10) somatorio_items
WHERE pedido.cod_cliente = somatorio_items.cod_pedido;

/*
    13. Crie uma consulta que exiba o nome do cliente, endereço, cidade, estado, CEP,
        código do pedido e prazo de entrega dos pedidos que NÃO sejam de
        vendedores que ganham menos de R$ 1500,00.
*/

SELECT pedido.cod_vendedor, nome, endereco, cidade, uf, cep, cod_pedido, prazo_entrega FROM pedido
INNER JOIN cliente ON(pedido.cod_cliente = cliente.cod_cliente),
(SELECT cod_vendedor FROM vendedor WHERE salario_fixo > 1500) vendedor_data
WHERE pedido.cod_vendedor = vendedor_data.cod_vendedor;

/*
    14. Crie uma consulta que exiba o código do pedido e a soma da quantidade de
        itens deste pedido. Devem ser exibidos somente os pedidos em que a soma das
        quantidades de itens de um pedido seja maior do que a média da quantidade
        de itens de todos os pedidos.
*/

SELECT cod_pedido, SUM(quantidade) FROM item_pedido
GROUP BY cod_pedido HAVING SUM(quantidade) > (SELECT AVG(quantidade) AS average FROM item_pedido);

/*
    15. Selecione o nome e valor unitário dos produtos que possuem valor unitário
        maior do que todos os produtos que começam com a letra &quot;L&quot;. A lista deve ser
        ordenada em ordem alfabética.
*/

SELECT p1.descricao, p1.valor_unitario FROM produto p1
WHERE p1.valor_unitario > ALL (
    SELECT p2.valor_unitario FROM produto p2
    WHERE SUBSTRING(p2.descricao, 1, 1) = 'N'
);

/*
    16. Mostre os dados (código, nome, salário e faixa de comissão) dos vendedores
        que venderam algum produto cuja descrição inicie com &quot;IPHONE 6 PLUS&quot;.
*/

SELECT v.cod_vendedor, v.nome, v.salario_fixo, v.faixa_comissao FROM vendedor v
INNER JOIN pedido ON(v.cod_vendedor = pedido.cod_vendedor)
INNER JOIN item_pedido ip ON pedido.cod_pedido = ip.cod_pedido
INNER JOIN produto p ON ip.cod_produto = p.cod_produto
WHERE starts_with(descricao, 'IPHONE 6 PLUS');

/*
    17. Crie um ranking contendo o nome dos vendedores e o valor total gasto por
        cada cliente na loja. Note que o valor total não é por pedido e sim por cliente
        (se um cliente efetuou mais de um pedido, os valores devem ser somados).
        Ordene a lista pelo total gasto por cada cliente.
*/

SELECT vendedor.cod_vendedor, vendedor.nome, results.somatorio  FROM vendedor,
                           (
SELECT pedido.cod_vendedor AS id_vend, SUM(item_pedido.quantidade * produto.valor_unitario) AS somatorio FROM pedido
INNER JOIN item_pedido ON(pedido.cod_pedido = item_pedido.cod_pedido)
INNER JOIN produto ON(item_pedido.cod_produto = produto.cod_produto)
GROUP BY pedido.cod_pedido
              ) results
WHERE vendedor.cod_vendedor = results.id_vend ORDER BY results.somatorio;

/*
    18. Liste os pedidos que têm mais de três produtos. - DONE
*/

SELECT * FROM pedido,
(SELECT item_pedido.cod_pedido, COUNT(cod_pedido) FROM item_pedido GROUP BY cod_pedido HAVING COUNT(cod_pedido) > 3) quant_pedido
WHERE pedido.cod_pedido = quant_pedido.cod_pedido;