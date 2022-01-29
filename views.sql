DROP VIEW IF EXISTS KsiazkiView;
CREATE VIEW KsiazkiView AS (
    SELECT Ks.tytul AS "Tytul", Ks.data_wydania AS "Data Wydania", Ks.ilosc_egzemplarzy AS "Ilość Egzemplarzy", G.nazwa AS "Gatunek", A.imie AS "Imie",
    A.nazwisko AS "Nazwisko", W.nazwa AS "Wydawnictwo"
    FROM "Ksiazka" AS Ks, "Gatunek" AS G, "Autor" AS A, "Wydawnictwo" AS W, "Gatunek_Ksiazka" AS GK, "Wydawnictwo_Ksiazka" AS WK, "Autor_Ksiazka" AS AK
    WHERE Ks.id = GK.id_ksiazka AND GK.id_gatunek = G.id AND
          Ks.id = WK.id_ksiazka AND WK.id_wydawnictwo = W.id AND
          Ks.id = AK.id_ksiazka AND AK.id_autor = A.id
    ORDER BY Ks.tytul);

DROP VIEW IF EXISTS RecenzjaView;
CREATE VIEW RecenzjaView AS (
    SELECT Ks.tytul AS "Tytul", R.ocena AS "Ocena", R.opinia AS "Opinia"
    FROM "Ksiazka" AS Ks, "Recenzja" AS R
    WHERE Ks.id = R.id_ksiazka
    ORDER BY Ks.tytul);