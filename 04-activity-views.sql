/*
    Exercício 1
    •   Neste exercício, você criará uma view que mostra os
        artistas mais vendidos no banco de dados Chinook. A view
        deve incluir o nome do artista, o número total de faixas
        vendidas e o valor total de vendas. O nome da view
        top_selling_artists.

    •   A view deve listar os artistas em ordem decrescente com
        base no número total de faixas vendidas.
*/

CREATE VIEW top_selling_artists AS
SELECT "Artist"."Name", COUNT("InvoiceLine"."Quantity") AS Amount, SUM("InvoiceLine"."UnitPrice") FROM "InvoiceLine"
INNER JOIN "Track" ON("InvoiceLine"."TrackId" = "Track"."TrackId")
INNER JOIN "Album" ON("Track"."AlbumId" = "Album"."AlbumId")
INNER JOIN "Artist" ON("Album"."ArtistId" = "Artist"."ArtistId")
GROUP BY "Artist"."ArtistId" ORDER BY Amount DESC;

-- EXECUTE VIEW
SELECT * FROM top_selling_artists;


/*
    Exercício 2
    •   Vamos supor que você possui o banco de dados Chinook
        com informações sobre artistas, álbuns e faixas. Você
        criou uma view chamada artist_albums que mostra
        informações detalhadas sobre os álbuns de cada artista.
        Agora, você deseja gerenciar o acesso a essa view para
        diferentes usuários:

    a)  Conceda permissão de SELECT na view artist_albums
        para o usuário "user1".
    b)  Conceda todas as permissões na view artist_albums
        para um grupo de usuários chamado "music_team".
*/

CREATE VIEW artist_albums AS
SELECT
    "Artist"."ArtistId", "Artist"."Name" AS Artist_Name, "Album"."AlbumId",
    "Album"."Title", "Track"."TrackId", "Track"."Name" AS Track_Name,
    "Track"."Composer", "Track"."Milliseconds", "Track"."UnitPrice", "Track"."Bytes"
FROM "Artist"
INNER JOIN "Album" ON("Artist"."ArtistId" = "Album"."ArtistId")
INNER JOIN "Track" ON("Album"."AlbumId" = "Track"."AlbumId");

-- EXECUTE VIEW
SELECT * FROM artist_albums;

-- a)
REVOKE SELECT ON artist_albums FROM user1;

-- b)
GRANT ALL ON artist_albums TO music_team;
