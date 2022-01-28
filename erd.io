Table Ksiazka
{
  id int [pk, increment, not null]
  
  tytul varchar(40) [not null]
  ilosc_egzemplarzy int [not null]
  data_wydania date [not null]
}

Table Wypozyczenie
{
  id int [pk, increment, not null]
  
  id_ksiazka int [not null]
  id_klient int [not null]
  
  data_wypozyczenia date [not null]
  data_oddania date [not null]
}

Table Status
{
  id int [pk, increment, not null]
  
  status varchar(20) [not null]
}

Table Autor
{
  id int [pk, increment, not null]
  
  imie varchar(20) [not null]
  nazwisko varchar(20) [not null]
}

Table Autor_Ksiazka
{
  id_ksiazka int [not null]
  id_autor int [not null]
}

Table Rezerwacja
{
  id int [pk, increment, not null]
  
  id_ksiazka int [not null]
  id_klient int [not null]
  
  data_rezerwacji date [not null]
  id_status int [not null]
}

Table Klient
{
  id int [pk, increment, not null]
  
  imie varchar(20) [not null]
  nazwisko varchar(20) [not null]
}

Table Recenzja
{
  id int [pk, increment, not null]
  
  id_ksiazka int [not null]
  
  ocena int [not null]
  opinia text
}

Table Wydawnictwo
{
  id int [pk, increment, not null]
  nazwa varchar(40)
}

Table Wydawnictwo_Ksiazka
{
  id_wydawnictwo int [not null]
  id_ksiazka int [not null]
}

Table Oplata
{
  id int [pk, increment, not null]
  
  id_klient int [not null]
  id_wypozyczenie int [not null]
  
  termin_zaplaty date [not null]
  kwota int [not null]
}

Table Kategoria
{
  id int [pk, increment, not null]
  nazwa varchar(20) [not null]
}

Table Kategoria_Ksiazka
{
  id_kategoria int [not null]
  id_ksiazka int [not null]
}

Ref: Status.id < Rezerwacja.id_status
Ref: Ksiazka.id < Autor_Ksiazka.id_ksiazka
Ref: Autor.id < Autor_Ksiazka.id_autor
Ref: Ksiazka.id - Rezerwacja.id_ksiazka
Ref: Klient.id > Rezerwacja.id_klient
Ref: Ksiazka.id - Wypozyczenie.id_ksiazka
Ref: Klient.id > Wypozyczenie.id_klient
Ref: Ksiazka.id < Recenzja.id_ksiazka
Ref: Wydawnictwo.id < Wydawnictwo_Ksiazka.id_wydawnictwo
Ref: Ksiazka.id < Wydawnictwo_Ksiazka.id_ksiazka
Ref: Klient.id < Oplata.id_klient
Ref: Wypozyczenie.id - Oplata.id_wypozyczenie
Ref: Kategoria.id < Kategoria_Ksiazka.id_kategoria
Ref: Ksiazka.id < Kategoria_Ksiazka.id_ksiazka