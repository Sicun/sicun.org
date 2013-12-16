-- PostgreSQL

SET client_min_messages = ERROR;
SET client_encoding = 'UTF8';
CREATE EXTENSION IF NOT EXISTS pgcrypto;


-------------------------------------------------------------------------------
-- table
-------------------------------------------------------------------------------

DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
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


DROP TABLE IF EXISTS groups CASCADE;
CREATE TABLE groups (
    gid serial PRIMARY KEY,
    name varchar(32) NOT NULL UNIQUE,
    leader varchar(32)
);


DROP TABLE IF EXISTS group_member CASCADE;
CREATE TABLE group_member (
    gid integer REFERENCES groups(gid) NOT NULL,
    uid integer REFERENCES users(uid) NOT NULL,
    -- 副组长
    is_subleader bool NOT NULL DEFAULT false,
    PRIMARY KEY (gid, uid)
);


DROP SEQUENCE IF EXISTS message_seq CASCADE;
CREATE SEQUENCE message_seq;
DROP TABLE IF EXISTS message CASCADE;
CREATE TABLE message (
    id integer PRIMARY KEY DEFAULT nextval('message_seq'),
    uid integer REFERENCES users(uid),
    title varchar(100),
    content varchar(1000),
    createtime timestamp DEFAULT now()
);


DROP TABLE IF EXISTS notice CASCADE;
CREATE TABLE notice (
    id integer PRIMARY KEY DEFAULT nextval('message_seq'),
    uid integer REFERENCES users(uid),
    title varchar(100),
    content varchar(1000),
    sort varchar(20),
    place varchar(20),
    is_use_sms bool default false,
    is_use_email bool default false,
    createtime timestamp DEFAULT now()
);


DROP TABLE IF EXISTS share CASCADE;
CREATE TABLE share (
    id serial PRIMARY KEY,
    uid integer REFERENCES users(uid),
    title varchar(100),
    content varchar(1000),
    url varchar(255),
    createtime timestamp DEFAULT now()
);


DROP TABLE IF EXISTS activity CASCADE;
CREATE TABLE activity (
    id serial PRIMARY KEY,
    uid integer REFERENCES users(uid),
    content varchar(1000),
    begintime timestamp,
    -- 集合地点
    venue varchar(100),
    cost int,
    -- 目的地
    destination varchar(20),
    is_use_sms bool default false,
    is_use_email bool default false,
    createtime timestamp DEFAULT now()
);


DROP TABLE IF EXISTS project CASCADE;
CREATE TABLE project (
    id serial PRIMARY KEY,
    uid integer REFERENCES users(uid),
    name varchar(100),
    -- 摘要
    abstract varchar(200),
    need_staff varchar(30),
    definition varchar(400),
    -- 项目定位
    positioning varchar(200),
    -- 目标
    destination varchar(20),
    news varchar(20),
    createtime timestamp DEFAULT now()
);


DROP TABLE IF EXISTS footprint CASCADE;
CREATE TABLE footprint (
    id serial PRIMARY KEY,
    content varchar(280),
    nickname varchar(18),
    email varchar(50),
    createtime timestamp DEFAULT now()
);


DROP TABLE IF EXISTS book CASCADE;
CREATE TABLE book (
    id serial PRIMARY KEY,
    name varchar(100),
    isbn varchar(13),
    createtime timestamp DEFAULT now()
);


DROP TABLE IF EXISTS book_debit CASCADE;
CREATE TABLE book_debit (
    book_id integer REFERENCES book(id),
    uid integer REFERENCES users(uid),
    createtime timestamp DEFAULT now()
);


--------------------------------------------------------------------------------
-- function
--------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_uid(account_s varchar)
  RETURNS integer
AS $$
    SELECT uid
      FROM users
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
       FROM users
      WHERE email = $1
         OR penname = $2;
    IF FOUND THEN
        RETURN NULL;
    END IF;

    INSERT INTO users (
        email, penname, password)
    VALUES (
        $1, $2, crypt($3, gen_salt('bf')))
    RETURNING md5(CAST(uid AS varchar))
    INTO hashuid_s;
    RETURN hashuid_s;
END;
$$ LANGUAGE plpgsql;

