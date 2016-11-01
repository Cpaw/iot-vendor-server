#!/usr/bin/env sh
sqlite3 jihanki.db <<-HERE
create table menu(
  name  text not null,
  price int  not null,
  value int  not null,
  PRIMARY KEY(name)
);
insert into menu values('Orange',  120, 3);
insert into menu values('Soda',    100, 3);
insert into menu values('RedBull', 200, 3);
.exit
HERE
