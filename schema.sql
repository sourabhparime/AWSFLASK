USE fl;
drop table if exists emails;
CREATE table emails(
  id INTEGER PRIMARY KEY auto_increment,
  user_name varchar(20) NOT NULL,
  user_email varchar(30) UNIQUE NOT NULL

);