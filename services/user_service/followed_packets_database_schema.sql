drop table if exists followed_packets;
    create table followed_packets (
    id integer primary key autoincrement,
    email text not null,
    packet text not null
);
