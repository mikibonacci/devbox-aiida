# PostgreSQL Basics — The Essential 20%

---

A nice tutorial can be found [here](https://www.postgresql.org/docs/current/index.html).

## Concepts

| Term | What it is |
|------|-----------|
| **cluster** | One PostgreSQL server instance, containing many databases |
| **database** | An isolated namespace — like a project folder |
| **schema** | A sub-namespace inside a database (default: `public`) |
| **table** | Rows + columns, like a spreadsheet |
| **role** | A user or a group (PostgreSQL merges both concepts) |

---

## First-time setup (from the shell, no psql needed)

When PostgreSQL is freshly initialized there are no users or databases yet
(except the internal `postgres` superuser role). Do this first:

```bash
# List existing databases
psql -d postgres -c "\l"

# List existing roles/users
psql -d postgres -c "\du"

# Create a user with a password (non-interactive)
createuser --login --pwprompt myuser
# or without the prompt, passing the password via env var:
PGPASSWORD=secret createuser --login myuser
# then set the password afterwards:
psql -d postgres -c "ALTER ROLE myuser WITH PASSWORD 'secret';"

# Create a database owned by that user
createdb --owner=myuser mydb

# Verify
psql -d postgres -c "\l"
```

Once a database exists, connect to it directly:

```bash
psql -U myuser -d mydb
# bare `psql` connects to a DB named after your OS user — create it to make that work:
createdb $USER
psql   # now works
```

---

## Connect

```bash
psql -h localhost -p 5432 -U myuser -d mydb
# or use the connection string form:
psql "postgresql://myuser:mypassword@localhost:5432/mydb"
```

Once inside `psql`, useful meta-commands:

```
\l          list databases
\c mydb     connect to a database
\dt         list tables in current schema
\d mytable  describe a table (columns, types, constraints)
\q          quit
```

---

## Users & Databases

If this is the first time you create users, run `psql -d postgres`.

```sql
-- Create a user with a password
CREATE ROLE myuser WITH LOGIN PASSWORD 'secret';

-- Create a database owned by that user
CREATE DATABASE mydb OWNER myuser;

-- Grant connection privileges on a database
-- NOTE: this does NOT grant access to tables — it only allows connecting
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;

-- Grant access to all existing tables in the public schema
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO myuser;

-- Also grant access to tables created in the future
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO myuser;

-- Drop them
DROP DATABASE mydb;
DROP ROLE myuser;
```

---

## Tables

```sql
-- Create
CREATE TABLE users (
    id      SERIAL PRIMARY KEY,    -- auto-increment integer
    name    TEXT        NOT NULL,
    email   TEXT        UNIQUE,
    created TIMESTAMPTZ DEFAULT now()
);

-- Alter
ALTER TABLE users ADD COLUMN age INT;
ALTER TABLE users DROP COLUMN age;

-- Drop
DROP TABLE users;
```

Common types: `INT`, `BIGINT`, `SERIAL`, `TEXT`, `VARCHAR(n)`, `BOOLEAN`, `FLOAT`, `NUMERIC`, `DATE`, `TIMESTAMPTZ`, `JSONB`

---

## CRUD

```sql
-- Insert
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');

-- Select
SELECT * FROM users;
SELECT name, email FROM users WHERE id = 1;
SELECT * FROM users ORDER BY created DESC LIMIT 10;

-- Update
UPDATE users SET name = 'Bob' WHERE id = 1;

-- Delete
DELETE FROM users WHERE id = 1;
```

---

## Joins

```sql
CREATE TABLE orders (
    id      SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    amount  NUMERIC
);

-- INNER JOIN: only rows that match on both sides
SELECT u.name, o.amount
FROM users u
JOIN orders o ON o.user_id = u.id;

-- LEFT JOIN: all users, even those with no orders
SELECT u.name, o.amount
FROM users u
LEFT JOIN orders o ON o.user_id = u.id;
```

---

## Indexes

```sql
-- PostgreSQL creates an index automatically on PRIMARY KEY and UNIQUE columns.
-- Add one manually for columns you filter/sort on frequently:
CREATE INDEX ON users (email);
CREATE INDEX ON orders (user_id);

-- See indexes on a table
\d users
```

---

## Transactions

```sql
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;   -- or ROLLBACK; to undo everything
```

---

## Backup & Restore

```bash
# Dump a database to a file
pg_dump -U myuser mydb > mydb.sql

# Restore it
psql -U myuser -d mydb < mydb.sql

# Binary format (faster, supports parallel restore)
pg_dump -Fc -U myuser mydb > mydb.dump
pg_restore -U myuser -d mydb mydb.dump
```

---

## The one `psql` trick you'll use constantly

```bash
# Run a query directly from the shell without entering the interactive prompt
psql -U myuser -d mydb -c "SELECT count(*) FROM users;"
```
