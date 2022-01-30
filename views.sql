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

DROP VIEW IF EXISTS KlienciView;
CREATE VIEW KlienciView AS (
    SELECT K.imie AS "Imie", K.nazwisko AS "Nazwisko", K.pesel AS "Pesel", K.email AS "Email"
    FROM "Klient" AS K
    ORDER BY K.nazwisko);

DROP VIEW IF EXISTS KlientWypozyczenieView;
CREATE VIEW KlientWypozyczenieView AS (
    SELECT K.imie AS "Imie", K.nazwisko AS "Nazwisko", K.pesel AS "Pesel", K.email AS "Email",
    Ks.tytul AS "Tytul", W.id AS "ID Wypozyczenia", W.data_wypozyczenia AS "Data Wypozyczenia",
    W.data_oddania AS "Data Oddania"
    FROM "Klient" AS K, "Ksiazka" AS Ks, "Wypozyczenie" AS W
    WHERE W.id_ksiazka = Ks.id AND W.id_klient = K.id
    ORDER BY K.nazwisko);

DROP VIEW IF EXISTS KlientAktualneWypozyczenieView;
CREATE VIEW KlientAktualneWypozyczenieView AS (
    SELECT K.imie AS "Imie", K.nazwisko AS "Nazwisko", K.pesel AS "Pesel", K.email AS "Email",
    Ks.tytul AS "Tytul", W.id AS "ID Wypozyczenia", W.data_wypozyczenia AS "Data Wypozyczenia",
    W.data_oddania AS "Data Oddania"
    FROM "Klient" AS K, "Ksiazka" AS Ks, "Wypozyczenie" AS W
    WHERE W.id_ksiazka = Ks.id AND W.id_klient = K.id AND W.aktualne = 'TRUE'
    ORDER BY K.nazwisko);

DROP VIEW IF EXISTS DostepneKsiazkiView;
CREATE VIEW DostepneKsiazkiView AS (
    SELECT Ks.id AS "Id", Ks.tytul AS "Tytul"
    FROM "Ksiazka" AS Ks
    WHERE Ks.ilosc_egzemplarzy > 0
    ORDER BY Ks.tytul);

DROP VIEW IF EXISTS RezerwacjeView;
CREATE VIEW RezerwacjeView AS (
    SELECT R.id AS "Id Rezerwacji", R.id_ksiazka AS "Id Książki", K.pesel AS "Pesel", R.data_rezerwacji AS "Data Rezerwacji", S.status AS "Status"
    FROM "Rezerwacja" AS R, "Klient" AS K, "Status" AS S
    WHERE K.id = R.id_klient AND R.id_status = S.id
    ORDER BY R.id);