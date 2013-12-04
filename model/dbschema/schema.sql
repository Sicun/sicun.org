-- PostgreSQL

SET client_min_messages = ERROR;
SET client_encoding = 'UTF8';
CREATE EXTENSION IF NOT EXISTS pgcrypto;


-------------------------------------------------------------------------------
-- table
-------------------------------------------------------------------------------

DROP TABLE IF EXISTS "user" CASCADE;
CREATE TABLE "user" (
    uid serial PRIMARY KEY,
    nickname varchar(18) UNIQUE,
    qq varchar(18) UNIQUE,
    phone varchar(18) UNIQUE,
    email varchar(50) UNIQUE,
    password varchar(128) NOT NULL,
    realname varchar(32),
    -- 头像url
    avatar varchar(255),
    jointime timestamp NOT NULL DEFAULT now(),
    is_admin bool NOT NULL DEFAULT false
);


DROP TABLE IF EXISTS "group" CASCADE;
CREATE TABLE "group" (
    uid serial PRIMARY KEY,
    name varchar(32) NOT NULL UNIQUE,
    leader varchar(32)
);


DROP TABLE IF EXISTS group_member CASCADE;
CREATE TABLE group_member (
    gid serial REFERENCES "group"(gid) NOT NULL,
    uid serial REFERENCES "user"(uid) NOT NULL,
    -- 副组长
    is_subleader bool NOT NULL DEFAULT false
);


--------------------------------------------------------------------------------
-- function
--------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_uid(account_s varchar)
  RETURNS integer
AS $$
    SELECT uid
      FROM "user"
     WHERE email = $1
        OR nickname = $1
        OR qq = $1
        OR phone = $1;
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION do_register_user(
    email_s varchar,
    penname_s varchar,
    password_s varchar)
  RETURNS varchar AS
$$
DECLARE
    hashuid_s varchar;
BEGIN
    PERFORM uid
       FROM "user"
      WHERE email = $1
         OR penname = $2;
    IF FOUND THEN
        RETURN NULL;
    END IF;

    INSERT INTO "user" (
        email, penname, password)
    VALUES (
        $1, $2, crypt($3, gen_salt('bf')))
    RETURNING md5(CAST(uid AS varchar))
    INTO hashuid_s;
    RETURN hashuid_s;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION user_t()
  RETURNS trigger
AS $$
BEGIN
    IF (TG_OP = 'DELETE') THEN
        --DELETE FROM "group" WHERE uid = OLD.uid;
        RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
        RETURN OLD;
    ELSIF (TG_OP = 'INSERT') THEN
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


--------------------------------------------------------------------------------
-- 触发器
--------------------------------------------------------------------------------
DROP TRIGGER IF EXISTS user_t ON "user";
CREATE TRIGGER user_t BEFORE DELETE ON "user"
   FOR EACH ROW EXECUTE PROCEDURE user_t();
