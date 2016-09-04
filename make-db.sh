#!/usr/bin/env sh
sqlite3 test.db <<-HERE
create table menu(name text, price integer, value integer);
insert into menu values("Orange", 120, 7);
insert into menu values("Soda", 100, 4);
insert into menu values("RedBull", 200, 15);
.exit
HERE
