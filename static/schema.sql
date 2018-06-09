USE fl;
drop table if exists emails;
CREATE table emails(
  user_name varchar(20) NOT NULL,
  user_email varchar(30) UNIQUE NOT NULL primary key

);