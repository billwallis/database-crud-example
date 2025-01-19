/* Sample actions */


/* A customer creates a new account */
start transaction;
    insert into domain.accounts
    default values
    returning account_id
    ;
    insert into domain.customers(forename, surname, date_of_birth, postcode)
    values ('Bandit', 'Banditerson', '1990-01-01', 'AB1 2CD')
    returning customer_id
    ;
    insert into domain.account_customer_bridge(account_id, customer_id)
    values (1, 1)
    ;
commit;


/* The customer adds another customer to the account */
start transaction;
    insert into domain.customers(forename, surname, date_of_birth, postcode)
    values ('Sapphire', 'Sapphirison', '1995-01-01', 'AB1 2CD')
    returning customer_id
    ;
    insert into domain.account_customer_bridge(account_id, customer_id)
    values (1, 2)
    ;
commit;


/* Another customer creates a new account */
start transaction;
    insert into domain.accounts
    default values
    returning account_id
    ;
    insert into domain.customers(forename, surname, date_of_birth, postcode)
    values ('Leeroy', 'Leeroyson', '2000-01-01', 'EF3 4GH')
    returning customer_id
    ;
    insert into domain.account_customer_bridge(account_id, customer_id)
    values (2, 3)
    ;
commit;


/* The new customer adds an existing customer to the account */
start transaction;
    insert into domain.account_customer_bridge(account_id, customer_id)
    values (2, 2)
    ;
commit;


/* The second customer opens a loan with each account */
start transaction;
    insert into domain.loans(account_id, amount, interest_rate, start_date, end_date, current_balance)
    values (1, 1000, 0.05, '2020-01-01', '2021-01-01', 1000)
    returning loan_id
    ;
commit;
start transaction;
    insert into domain.loans(account_id, amount, interest_rate, start_date, end_date, current_balance)
    values (2, 2000, 0.10, '2020-01-01', '2021-01-01', 2000)
    returning loan_id
    ;
commit;


/* The first customer deletes their profile */
start transaction;
    update domain.customers
    set deleted = true,
        /* Obfuscate the sensitive data */
        forename = gen_random_uuid(),
        surname = gen_random_uuid(),
        date_of_birth = '1990-01-01',
        postcode = gen_random_uuid()
    where customer_id = 1
    ;
    update domain.account_customer_bridge
    set deleted = true
    where customer_id = 1
    ;
commit;


/* Check the state of everything */

/* Accounts */
select * from domain.accounts order by account_id;

/* Customers */
select * from domain.customers order by customer_id;

/* Account-customer bridges */
select * from domain.account_customer_bridge order by account_id, customer_id;

/* Loans */
select * from domain.loans order by loan_id;
