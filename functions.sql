DROP TRIGGER after_add_rent ON "Wypozyczenie";
DROP TRIGGER after_add_reservation ON "Rezerwacja";
DROP FUNCTION update_count();

CREATE OR REPLACE FUNCTION update_count()
RETURNS TRIGGER
LANGUAGE 'plpgsql' AS
$$
    BEGIN
        UPDATE "Ksiazka" SET ilosc_egzemplarzy = ilosc_egzemplarzy-1 WHERE id = NEW.id_ksiazka;
        RETURN NEW;
    END;
$$;

CREATE TRIGGER after_add_rent AFTER INSERT ON "Wypozyczenie"
FOR EACH ROW EXECUTE PROCEDURE update_count();

CREATE TRIGGER after_add_reservation AFTER INSERT ON "Rezerwacja"
FOR EACH ROW EXECUTE PROCEDURE update_count();

DROP TRIGGER before_add_client ON "Klient";
DROP FUNCTION check_for_client();

CREATE OR REPLACE FUNCTION check_for_client()
RETURNS TRIGGER
LANGUAGE 'plpgsql' AS
$$
    DECLARE
        pes VARCHAR;
    BEGIN
        FOR pes in SELECT pesel FROM "Klient" LOOP
            IF pes = NEW.PESEL THEN
                RAISE EXCEPTION 'Klient o podanym peselu już jest w bazie danych.';
            ELSE
                RETURN NEXT pes;
            END IF;
        END LOOP;
        RETURN;
    END;
$$;

CREATE TRIGGER before_add_client BEFORE INSERT ON "Klient"
FOR EACH ROW EXECUTE PROCEDURE check_for_client();

CREATE OR REPLACE FUNCTION check_pesel()
RETURNS TRIGGER
LANGUAGE 'plpgsql' AS
$$
    DECLARE
        pes VARCHAR;
    BEGIN
        IF (NEW.PESEL ~ '^[0-9]*$' AND LENGTH(NEW.PESEL) IN (11)) THEN
            RETURN NEW;
        ELSE
            RAISE EXCEPTION 'Pesel niepoprawny';
        END IF;
    END;
$$;

CREATE TRIGGER before_add_client_check_pesel BEFORE INSERT ON "Klient"
FOR EACH ROW EXECUTE PROCEDURE check_pesel();