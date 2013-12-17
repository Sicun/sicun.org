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
    is_activated bool NOT NULL DEFAULT false,
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
    createtime timestamp DEFAULT now(),
    reply_count integer DEFAULT 0
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
    createtime timestamp DEFAULT now(),
    reply_count integer DEFAULT 0
);


DROP TABLE IF EXISTS reply CASCADE;
CREATE TABLE reply (
    id serial PRIMARY KEY,
    uid integer REFERENCES users(uid),
    content varchar(1000),
    createtime timestamp DEFAULT now(),
    reply_to integer
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
    cost integer,
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
-- view
--------------------------------------------------------------------------------

CREATE VIEW message_list_v
  AS
SELECT m.id, m.title, m.createtime, m.reply_count,
       u.nickname, u.avatar
  FROM (
        SELECT id, uid, title, createtime, reply_count
          FROM notice
         UNION
        SELECT id, uid, title, createtime, reply_count
          FROM message
     ) m,
       users u
 WHERE u.uid = m.uid;


CREATE VIEW reply_list_v
  AS
SELECT r.id, r.content, r.createtime, r.reply_to,
       u.nickname, u.avatar
  FROM reply r,
       users u
 WHERE u.uid = r.uid;


--------------------------------------------------------------------------------
-- function
--------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_user_id(_account varchar)
  RETURNS integer
AS $$
    SELECT uid
      FROM users
     WHERE nickname = $1
        OR qq = $1
        OR email = $1
        OR phone = $1;
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION get_userinfo(_uid integer)
  RETURNS json
AS $$
    SELECT row_to_json(j.*)
      FROM (
            SELECT *
              FROM users
             WHERE uid = $1
         ) j;
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION do_login_user(
    _account varchar,
    _password varchar)
  RETURNS integer
AS $$
    SELECT uid
      FROM users
     WHERE nickname = $1
        OR qq = $1
        OR email = $1
        OR phone = $1)
       AND password = crypt($2, password);
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION do_register_user(
    _email varchar,
    _password varchar)
  RETURNS varchar AS
$$
    PERFORM uid
       FROM users
      WHERE email = $1;
    IF FOUND THEN
        RETURN NULL;
    END IF;

    INSERT INTO users (email, password)
    VALUES ($1, crypt($2, gen_salt('bf')))
    RETURNING md5(CAST(uid AS varchar))
    INTO _hashuid;
    RETURN _hashuid;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION do_activate_user(_hashuid varchar)
  RETURNS integer AS
$$
    UPDATE users
       SET is_activated = true
     WHERE is_activated = false
       AND $1 = md5(CAST(uid AS varchar))
     RETURNING uid;
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION get_message_list(
    _limit integer,
    _offset integer)
  RETURNS json
AS $$
    SELECT array_to_json(array_agg(aj))
      FROM (
            SELECT *
              FROM message_list_v
             ORDER BY id DESC
             LIMIT $1
            OFFSET $2
         ) aj;
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION get_reply_list(
    _reply_to integer,
    _limit integer,
    _offset integer)
  RETURNS json
AS $$
    SELECT array_to_json(array_agg(aj))
      FROM (
            SELECT *
              FROM reply_list_v
             WHERE reply_to = $1
             ORDER BY id DESC
             LIMIT $2
            OFFSET $3
         ) aj;
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION get_notice(_id integer)
  RETURNS json
AS $$
    SELECT row_to_json(j.*)
      FROM (
            SELECT *
              FROM notice
             WHERE id = $1
         ) j;
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION get_message(_id integer)
  RETURNS json
AS $$
    SELECT row_to_json(j.*)
      FROM (
            SELECT *
              FROM message
             WHERE id = $1
         ) j;
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION create_reply(
    _uid integer,
    _content varchar,
    _reply_to integer)
  RETURNS integer
AS $$
    INSERT INTO reply (
        uid, content, reply_to)
    VALUES ($1, $2, $3)
    RETURNING id;
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION create_message(
    _uid integer,
    _title varchar,
    _content varchar)
  RETURNS integer
AS $$
    INSERT INTO message (
        uid, title, content)
    VALUES ($1, $2, $3)
    RETURNING id;
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION create_notice(
    _uid integer,
    _title varchar,
    _content varchar,
    _sort varchar DEFAULT NULL,
    _place varchar DEFAULT NULL,
    _is_use_sms bool DEFAULT false,
    _is_use_email bool DEFAULT false)
  RETURNS integer
AS $$
    INSERT INTO notice (
        uid, title, content, sort, place, is_use_sms, is_use_email)
    VALUES ($1, $2, $3, $4, $5, $6, $7)
    RETURNING id;
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION reply_after_t()
  RETURNS trigger
AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        UPDATE notice SET reply_count = reply_count + 1 WHERE id = NEW.reply_to;
        UPDATE message SET reply_count = reply_count + 1 WHERE id = NEW.reply_to;
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


--------------------------------------------------------------------------------
-- trigger
--------------------------------------------------------------------------------

DROP TRIGGER IF EXISTS reply_after_t ON reply;
CREATE TRIGGER reply_after_t AFTER INSERT ON reply
   FOR EACH ROW EXECUTE PROCEDURE reply_after_t();
