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


DROP TRIGGER before_add_client_check_pesel ON "Klient";
DROP FUNCTION check_pesel();

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


DROP TRIGGER before_add_client_check_email ON "Klient";
DROP FUNCTION check_email();

CREATE OR REPLACE FUNCTION check_email()
RETURNS TRIGGER
LANGUAGE 'plpgsql' AS
$$
    DECLARE
        pes VARCHAR;
    BEGIN
        IF NEW.email !~ '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$' THEN
            RETURN NEW;
        ELSE
            RAISE EXCEPTION 'Email niepoprawny';
        END IF;
    END;
$$;

CREATE TRIGGER before_add_client_check_email BEFORE INSERT ON "Klient"
FOR EACH ROW EXECUTE PROCEDURE check_email();