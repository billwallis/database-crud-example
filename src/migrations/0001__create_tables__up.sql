create schema domain;


create table domain.accounts(
    account_id int primary key generated always as identity,
    created_ts timestamp default current_timestamp,
    updated_ts timestamp default current_timestamp,
    deleted bool default false
);
create function domain__accounts__update_updated_ts()
returns trigger as
$$
    begin
        update domain.accounts
        set updated_ts = current_timestamp
        where account_id = new.account_id;
        return new;
    end;
$$
language plpgsql
;
create trigger domain__accounts__updated_ts
    after update on domain.accounts
    for each row
    when (pg_trigger_depth() = 0)  /* only valid if no other trigger triggers this */
    execute function domain__accounts__update_updated_ts()
;


create table domain.customers(
    customer_id int primary key generated always as identity,
    forename varchar,
    surname varchar,
    date_of_birth date,
    postcode varchar,
    created_ts timestamp default current_timestamp,
    updated_ts timestamp default current_timestamp,
    deleted bool default false
);
create function domain__customers__update_updated_ts()
returns trigger as
$$
    begin
        update domain.customers
        set updated_ts = current_timestamp
        where customer_id = new.customer_id;
        return new;
    end;
$$
language plpgsql
;
create trigger domain__customers__updated_ts
    after update on domain.customers
    for each row
    when (pg_trigger_depth() = 0)  /* only valid if no other trigger triggers this */
    execute function domain__customers__update_updated_ts()
;


create table domain.account_customer_bridge(
    account_id int references domain.accounts(account_id),
    customer_id int references domain.customers(customer_id),
    created_ts timestamp default current_timestamp,
    updated_ts timestamp default current_timestamp,
    deleted bool default false,
    primary key(account_id, customer_id)
);
create function domain__account_customer_bridge__update_updated_ts()
returns trigger as
$$
    begin
        update domain.account_customer_bridge
        set updated_ts = current_timestamp
        where account_id = new.account_id
        and customer_id = new.customer_id;
        return new;
    end;
$$
language plpgsql
;
create trigger domain__account_customer_bridge__updated_ts
    after update on domain.account_customer_bridge
    for each row
    when (pg_trigger_depth() = 0)  /* only valid if no other trigger triggers this */
    execute function domain__account_customer_bridge__update_updated_ts()
;


create table domain.loans(
    loan_id int primary key generated always as identity,
    account_id int references domain.accounts(account_id),
    amount decimal(18, 2),
    interest_rate decimal(8, 4),
    start_date date,
    end_date date,
    current_balance decimal(18, 2),
    created_ts timestamp default current_timestamp,
    updated_ts timestamp default current_timestamp,
    deleted bool default false
);
create function domain__loans__update_updated_ts()
returns trigger as
$$
    begin
        update domain.loans
        set updated_ts = current_timestamp
        where loan_id = new.loan_id;
        return new;
    end;
$$
language plpgsql
;
create trigger domain__loans__updated_ts
    after update on domain.loans
    for each row
    when (pg_trigger_depth() = 0)  /* only valid if no other trigger triggers this */
    execute function domain__loans__update_updated_ts()
;
