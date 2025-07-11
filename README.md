<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![tests](https://github.com/billwallis/database-crud-example/actions/workflows/tests.yaml/badge.svg)](https://github.com/billwallis/database-crud-example/actions/workflows/tests.yaml)
[![coverage](coverage.svg)](https://github.com/dbrgn/coverage-badge)
[![GitHub last commit](https://img.shields.io/github/last-commit/billwallis/database-crud-example)](https://shields.io/badges/git-hub-last-commit)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/billwallis/database-crud-example/main.svg)](https://results.pre-commit.ci/latest/github/billwallis/database-crud-example/main)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17.2-teal.svg)](https://www.postgresql.org/download/)

</div>

---

# Database CRUD Example

A simple example of a CRUD implementation for a database layer.

## Model

The model is loan system with accounts, customers, loans, and links between the accounts and customers ("account-customer bridges") since accounts can have multiple customers and customers can have multiple accounts.

```mermaid
---
title: Loan System
---
erDiagram
    accounts {
        int account_id
        timestamp created_ts
        timestamp updated_ts
        bool deleted
    }
    customers {
        int customer_id
        varchar forename
        varchar surname
        date date_of_birth
        varchar postcode
        timestamp created_ts
        timestamp updated_ts
        bool deleted
    }
    account_customer_bridge {
        int account_id
        int customer_id
        timestamp created_ts
        timestamp updated_ts
        bool deleted
    }
    loans {
        int loan_id
        int account_id
        decimal amount
        decimal interest_rate
        date start_date
        date end_date
        decimal current_balance
        timestamp created_ts
        timestamp updated_ts
        bool deleted
    }
    customers ||--|{ account_customer_bridge : ""
    accounts ||--|{ account_customer_bridge : ""
    accounts ||--o{ loans : "opens"
```
