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
DROP TABLE IF EXISTS "Kategoria" CASCADE;
DROP TABLE IF EXISTS "Kategoria_Ksiazka" CASCADE;

CREATE TABLE "Ksiazka" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "tytul" varchar(40) NOT NULL,
  "ilosc_egzemplarzy" int NOT NULL,
  "data_wydania" date NOT NULL
);

CREATE TABLE "Wypozyczenie" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "id_ksiazka" int NOT NULL UNIQUE,
  "id_klient" int NOT NULL UNIQUE,
  "data_wypozyczenia" date NOT NULL,
  "data_oddania" date NOT NULL
);

CREATE TABLE "Status" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "status" varchar(20) NOT NULL
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
  "id_ksiazka" int NOT NULL UNIQUE,
  "id_klient" int NOT NULL UNIQUE,
  "data_rezerwacji" date NOT NULL,
  "id_status" int NOT NULL UNIQUE
);

CREATE TABLE "Klient" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "imie" varchar(20) NOT NULL,
  "nazwisko" varchar(20) NOT NULL
);

CREATE TABLE "Recenzja" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "id_ksiazka" int NOT NULL,
  "ocena" int NOT NULL,
  "opinia" text
);

CREATE TABLE "Wydawnictwo" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "nazwa" varchar(40)
);

CREATE TABLE "Wydawnictwo_Ksiazka" (
  "id_wydawnictwo" int NOT NULL,
  "id_ksiazka" int NOT NULL
);

CREATE TABLE "Oplata" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "id_klient" int NOT NULL UNIQUE,
  "id_wypozyczenie" int NOT NULL UNIQUE,
  "termin_zaplaty" date NOT NULL,
  "kwota" int NOT NULL
);

CREATE TABLE "Kategoria" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "nazwa" varchar(20) NOT NULL
);

CREATE TABLE "Kategoria_Ksiazka" (
  "id_kategoria" int NOT NULL,
  "id_ksiazka" int NOT NULL
);

ALTER TABLE "Rezerwacja" ADD FOREIGN KEY ("id_status") REFERENCES "Status" ("id");

ALTER TABLE "Autor_Ksiazka" ADD FOREIGN KEY ("id_ksiazka") REFERENCES "Ksiazka" ("id");

ALTER TABLE "Autor_Ksiazka" ADD FOREIGN KEY ("id_autor") REFERENCES "Autor" ("id");

ALTER TABLE "Ksiazka" ADD FOREIGN KEY ("id") REFERENCES "Rezerwacja" ("id_ksiazka");

ALTER TABLE "Klient" ADD FOREIGN KEY ("id") REFERENCES "Rezerwacja" ("id_klient");

ALTER TABLE "Ksiazka" ADD FOREIGN KEY ("id") REFERENCES "Wypozyczenie" ("id_ksiazka");

ALTER TABLE "Klient" ADD FOREIGN KEY ("id") REFERENCES "Wypozyczenie" ("id_klient");

ALTER TABLE "Recenzja" ADD FOREIGN KEY ("id_ksiazka") REFERENCES "Ksiazka" ("id");

ALTER TABLE "Wydawnictwo_Ksiazka" ADD FOREIGN KEY ("id_wydawnictwo") REFERENCES "Wydawnictwo" ("id");

ALTER TABLE "Wydawnictwo_Ksiazka" ADD FOREIGN KEY ("id_ksiazka") REFERENCES "Ksiazka" ("id");

ALTER TABLE "Oplata" ADD FOREIGN KEY ("id_klient") REFERENCES "Klient" ("id");

ALTER TABLE "Wypozyczenie" ADD FOREIGN KEY ("id") REFERENCES "Oplata" ("id_wypozyczenie");

ALTER TABLE "Kategoria_Ksiazka" ADD FOREIGN KEY ("id_kategoria") REFERENCES "Kategoria" ("id");

ALTER TABLE "Kategoria_Ksiazka" ADD FOREIGN KEY ("id_ksiazka") REFERENCES "Ksiazka" ("id");
