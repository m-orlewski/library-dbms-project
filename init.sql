DROP TABLE IF EXISTS "Ksiazka" CASCADE;
DROP TABLE IF EXISTS "Wypozyczenie" CASCADE;
DROP TABLE IF EXISTS "Status" CASCADE;
DROP TABLE IF EXISTS "Autor" CASCADE;
DROP TABLE IF EXISTS "Autor_Ksiazka" CASCADE;
DROP TABLE IF EXISTS "Rezerwacja" CASCADE;
DROP TABLE IF EXISTS "Klient" CASCADE;
DROP TABLE IF EXISTS "Recenzja" CASCADE;
DROP TABLE IF EXISTS "Wydawnictwo" CASCADE;
DROP TABLE IF EXISTS "Wydawnictwo_Ksiazka" CASCADE;
DROP TABLE IF EXISTS "Oplata" CASCADE;
DROP TABLE IF EXISTS "Gatunek" CASCADE;
DROP TABLE IF EXISTS "Gatunek_Ksiazka" CASCADE;

CREATE TABLE "Ksiazka" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "tytul" varchar(40) NOT NULL UNIQUE,
  "ilosc_egzemplarzy" int NOT NULL,
  "data_wydania" date NOT NULL
);

CREATE TABLE "Wypozyczenie" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "id_ksiazka" int NOT NULL,
  "id_klient" int NOT NULL,
  "data_wypozyczenia" date NOT NULL,
  "data_oddania" date NOT NULL,
  "aktualne" boolean NOT NULL DEFAULT 'TRUE'
);

CREATE TABLE "Status" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "status" varchar(20) NOT NULL UNIQUE
);

CREATE TABLE "Autor" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "imie" varchar(20) NOT NULL,
  "nazwisko" varchar(20) NOT NULL
);

CREATE TABLE "Autor_Ksiazka" (
  "id_ksiazka" int NOT NULL,
  "id_autor" int NOT NULL
);

CREATE TABLE "Rezerwacja" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "id_ksiazka" int NOT NULL,
  "id_klient" int NOT NULL,
  "data_rezerwacji" date NOT NULL,
  "id_status" int NOT NULL DEFAULT 1
);

CREATE TABLE "Klient" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "imie" varchar(20) NOT NULL,
  "nazwisko" varchar(20) NOT NULL,
  "pesel" varchar(11) NOT NULL UNIQUE,
  "email" varchar(40) NOT NULL UNIQUE
);

CREATE TABLE "Recenzja" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "id_ksiazka" int,
  "ocena" int NOT NULL,
  "opinia" text
);

CREATE TABLE "Wydawnictwo" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "nazwa" varchar(40) UNIQUE
);

CREATE TABLE "Wydawnictwo_Ksiazka" (
  "id_wydawnictwo" int NOT NULL,
  "id_ksiazka" int NOT NULL
);

CREATE TABLE "Gatunek" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "nazwa" varchar(20) NOT NULL UNIQUE
);

CREATE TABLE "Gatunek_Ksiazka" (
  "id_gatunek" int NOT NULL,
  "id_ksiazka" int NOT NULL
);

ALTER TABLE "Rezerwacja" ADD FOREIGN KEY ("id_status") REFERENCES "Status" ("id");
ALTER TABLE "Autor_Ksiazka" ADD FOREIGN KEY ("id_ksiazka") REFERENCES "Ksiazka" ("id");
ALTER TABLE "Autor_Ksiazka" ADD FOREIGN KEY ("id_autor") REFERENCES "Autor" ("id");
ALTER TABLE "Rezerwacja" ADD FOREIGN KEY ("id_ksiazka") REFERENCES "Ksiazka" ("id");
ALTER TABLE "Rezerwacja" ADD FOREIGN KEY ("id_klient") REFERENCES "Klient" ("id");
ALTER TABLE "Wypozyczenie" ADD FOREIGN KEY ("id_ksiazka") REFERENCES "Ksiazka" ("id");
ALTER TABLE "Wypozyczenie" ADD FOREIGN KEY ("id_klient") REFERENCES "Klient" ("id");
ALTER TABLE "Recenzja" ADD FOREIGN KEY ("id_ksiazka") REFERENCES "Ksiazka" ("id");
ALTER TABLE "Wydawnictwo_Ksiazka" ADD FOREIGN KEY ("id_wydawnictwo") REFERENCES "Wydawnictwo" ("id");
ALTER TABLE "Wydawnictwo_Ksiazka" ADD FOREIGN KEY ("id_ksiazka") REFERENCES "Ksiazka" ("id");
ALTER TABLE "Gatunek_Ksiazka" ADD FOREIGN KEY ("id_gatunek") REFERENCES "Gatunek" ("id");
ALTER TABLE "Gatunek_Ksiazka" ADD FOREIGN KEY ("id_ksiazka") REFERENCES "Ksiazka" ("id");

INSERT INTO "Ksiazka" (tytul, ilosc_egzemplarzy, data_wydania) VALUES ('Opowieść o dwóch miastach', 5, '1859-11-26');
INSERT INTO "Ksiazka" (tytul, ilosc_egzemplarzy, data_wydania) VALUES ('Hobbit, czyli tam i z powrotem', 3, '1937-09-21');
INSERT INTO "Ksiazka" (tytul, ilosc_egzemplarzy, data_wydania) VALUES ('Harry Potter i Kamień Filozoficzny', 1, '1997-06-26');
INSERT INTO "Ksiazka" (tytul, ilosc_egzemplarzy, data_wydania) VALUES ('I nie było już nikogo', 3, '1939-02-03');
INSERT INTO "Ksiazka" (tytul, ilosc_egzemplarzy, data_wydania) VALUES ('Morderstwo w Orient Expressie', 3, '1934-01-01');

INSERT INTO "Gatunek" (nazwa) VALUES ('Kryminał');
INSERT INTO "Gatunek" (nazwa) VALUES ('Fantasy');
INSERT INTO "Gatunek" (nazwa) VALUES ('Historyczna');

INSERT INTO "Gatunek_Ksiazka" (id_gatunek, id_ksiazka) VALUES (3, 1);
INSERT INTO "Gatunek_Ksiazka" (id_gatunek, id_ksiazka) VALUES (2, 2);
INSERT INTO "Gatunek_Ksiazka" (id_gatunek, id_ksiazka) VALUES (2, 3);
INSERT INTO "Gatunek_Ksiazka" (id_gatunek, id_ksiazka) VALUES (1, 4);
INSERT INTO "Gatunek_Ksiazka" (id_gatunek, id_ksiazka) VALUES (1, 5);

INSERT INTO "Autor" (imie, nazwisko) VALUES ('Charles', 'Dickens');
INSERT INTO "Autor" (imie, nazwisko) VALUES ('J.R.R', 'Tolkien');
INSERT INTO "Autor" (imie, nazwisko) VALUES ('J.K.', 'Rowling');
INSERT INTO "Autor" (imie, nazwisko) VALUES ('Agatha', 'Christie');

INSERT INTO "Autor_Ksiazka" (id_ksiazka, id_autor) VALUES (1, 1);
INSERT INTO "Autor_Ksiazka" (id_ksiazka, id_autor) VALUES (2, 2);
INSERT INTO "Autor_Ksiazka" (id_ksiazka, id_autor) VALUES (3, 3);
INSERT INTO "Autor_Ksiazka" (id_ksiazka, id_autor) VALUES (4, 4);
INSERT INTO "Autor_Ksiazka" (id_ksiazka, id_autor) VALUES (5, 4);

INSERT INTO "Wydawnictwo" (nazwa) VALUES ('PWN');
INSERT INTO "Wydawnictwo" (nazwa) VALUES ('Agora');
INSERT INTO "Wydawnictwo" (nazwa) VALUES ('Zysk i S-KA');

INSERT INTO "Wydawnictwo_Ksiazka" (id_wydawnictwo, id_ksiazka) VALUES (1, 1);
INSERT INTO "Wydawnictwo_Ksiazka" (id_wydawnictwo, id_ksiazka) VALUES (3, 2);
INSERT INTO "Wydawnictwo_Ksiazka" (id_wydawnictwo, id_ksiazka) VALUES (3, 3);
INSERT INTO "Wydawnictwo_Ksiazka" (id_wydawnictwo, id_ksiazka) VALUES (1, 4);
INSERT INTO "Wydawnictwo_Ksiazka" (id_wydawnictwo, id_ksiazka) VALUES (2, 5);

INSERT INTO "Status" (status) VALUES ('Złożona'); 
INSERT INTO "Status" (status) VALUES ('Odebrana');

INSERT INTO "Recenzja" (id_ksiazka, ocena, opinia) VALUES (1, 8, 'Dobra książka');
INSERT INTO "Recenzja" (id_ksiazka, ocena, opinia) VALUES (1, 5, 'Meeh');
INSERT INTO "Recenzja" (id_ksiazka, ocena, opinia) VALUES (2, 9, 'Genialna książka');
INSERT INTO "Recenzja" (id_ksiazka, ocena, opinia) VALUES (3, 10, '10/10');
INSERT INTO "Recenzja" (id_ksiazka, ocena, opinia) VALUES (3, 7, 'Słabe zakończenie');
INSERT INTO "Recenzja" (id_ksiazka, ocena, opinia) VALUES (4, 7, 'Za droga');

INSERT INTO "Klient" (imie, nazwisko, pesel, email) VALUES ('Jan', 'Kowalski', '00347612113', 'jan.kowalski@wp.pl');
INSERT INTO "Klient" (imie, nazwisko, pesel, email) VALUES ('Jan', 'Nowak', '23345612611', 'jnowak@onet.pl');
INSERT INTO "Klient" (imie, nazwisko, pesel, email) VALUES ('Anna', 'Malinowska', '01379342148', 'malinowska.a@gmail.com');
INSERT INTO "Klient" (imie, nazwisko, pesel, email) VALUES ('Piotr', 'Szpak', '10347426713', 'p.szpak@wp.pl');

INSERT INTO "Wypozyczenie" (id_ksiazka, id_klient, data_wypozyczenia, data_oddania) VALUES (1, 1, '2022-01-27', '2022-01-31');
INSERT INTO "Wypozyczenie" (id_ksiazka, id_klient, data_wypozyczenia, data_oddania) VALUES (3, 1, '2022-01-29', '2022-02-06');
INSERT INTO "Wypozyczenie" (id_ksiazka, id_klient, data_wypozyczenia, data_oddania) VALUES (4, 2, '2022-01-20', '2022-01-30');

INSERT INTO "Rezerwacja" (id_ksiazka, id_klient, data_rezerwacji, id_status) VALUES (2, 4, '2022-01-31', 1);
INSERT INTO "Rezerwacja" (id_ksiazka, id_klient, data_rezerwacji, id_status) VALUES (3, 4, '2022-02-03', 1);
INSERT INTO "Rezerwacja" (id_ksiazka, id_klient, data_rezerwacji, id_status) VALUES (2, 3, '2022-02-01', 1);