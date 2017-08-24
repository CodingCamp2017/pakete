drop table if exists users;
    create table users (
    id integer primary key autoincrement,
    email text not null,
    password text not null,
    name text not null,
    street text not null,
    zip text not null,
    city text not null,
    session_id text not null,
    session_id_timestamp text not null
);
