/*
    1. Escreva um script para criar um novo usuario chamado ”aluno”com senha ”password123”no
       PostgreSQL.
*/

CREATE ROLE aluno WITH LOGIN PASSWORD 'password123';

/*
    2. Escreva um script para conceder SELECT, INSERT e UPDATE de privilegios para ”aluno”na
       tabela ”artist”.
*/

SELECT rolname FROM pg_roles WHERE rolcanlogin = true;
GRANT SELECT, INSERT, UPDATE ON "Artist" TO aluno;

/*
    3. Escreva um script para revogar o privilégio INSERT de ”aluno” na tabela ”artist”.
*/

REVOKE INSERT ON "Artist" FROM aluno;

/*
    4. Escreva um script para criar um novo esquema chamado ”novo” e conceder todos os privilégios
       a ”aluno” nesse esquema.
*/

CREATE SCHEMA IF NOT EXISTS novo AUTHORIZATION aluno;
ALTER DEFAULT PRIVILEGES FOR ROLE aluno IN SCHEMA novo
GRANT ALL ON TABLES TO aluno;

/*
    5. Escreva um script para listar todos os privilégios concedidos ao usuário ”aluno” em todas as
       tabelas do banco de dados atual.
*/

SELECT grantor, table_name, grantee, privilege_type FROM information_schema.role_table_grants WHERE grantee = 'aluno'

/*
    6. (Banco 2) Para o banco fornecido desenvolva as subconsultas:

        (a) Encontre o valor total gasto pelos 5 principais clientes.

        (b) Liste os artistas que têm um número de  álbuns lançados acima da média.

        (c) Encontre a quantidade de faixas em cada playlist com uma duração total acima da
            média das playlists.

        (d) Mostre os álbuns com uma duração total de faixas maior do que a média de duração de
            todos os álbuns
*/

/* a */
SELECT "CustomerId", SUM("Total") AS total_gasto FROM "Invoice"
GROUP BY "CustomerId" ORDER BY total_gasto DESC
                      LIMIT 5;

/* b */
SELECT "ArtistId", COUNT("ArtistId") AS num_albuns FROM "Album"
GROUP BY "ArtistId"
HAVING COUNT("ArtistId") > (SELECT AVG(num_albuns) FROM (SELECT COUNT("ArtistId") AS num_albuns FROM "Album" GROUP BY "ArtistId") AS subquery)
ORDER BY num_albuns DESC;

/* c */

SELECT PLTCOUNT."PlaylistId",  COUNT(PLTCOUNT."PlaylistId") AS amount_track FROM "PlaylistTrack" PLTCOUNT
    WHERE PLTCOUNT."PlaylistId" IN (

    SELECT PLTSUM."PlaylistId" FROM "PlaylistTrack" PLTSUM
    INNER JOIN "Track" ON PLTSUM."PlaylistId" = "Track"."TrackId"
    GROUP BY PLTSUM."PlaylistId"
    HAVING SUM("Track"."Milliseconds") > (
                                            SELECT AVG("Track"."Milliseconds") FROM "PlaylistTrack" PTAVG
                                            INNER JOIN "Track" on PTAVG."TrackId" = "Track"."TrackId"
                                         )
)

GROUP BY PLTCOUNT."PlaylistId";

/* d */

SELECT * FROM "Album",
(SELECT "AlbumId", SUM("Milliseconds") AS duration_total FROM "Track" GROUP BY "AlbumId") subquery_track,
(SELECT AVG("Milliseconds") AS total FROM "Track") average_total
WHERE "Album"."AlbumId" = subquery_track."AlbumId" AND subquery_track.duration_total > average_total.total;