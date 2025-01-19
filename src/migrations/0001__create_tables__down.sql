drop schema if exists domain cascade;

drop function domain__accounts__update_updated_ts();
drop function domain__customers__update_updated_ts();
drop function domain__account_customer_bridge__update_updated_ts();
drop function domain__loans__update_updated_ts();
