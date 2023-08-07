# Apex OCR Server

## Database

[database]: #database

Alembic is used for managing database migrations, but before running the first command, make sure to create/update the `db.yml` file in the root directory.

Sample file:

```yaml
dialect: postgresql
username: postgres
password: password
hostname: localhost
port: 5432
database_name: apex-legends
```

Once the proper database configurations have been set in `db.yml`, run the following command from the root project directory to initialize the database tables:

```bash
alembic upgrade head
```

If you want to drop everything from the database and start over, you can run the following commands from the project directory to re-initialize the tables.

```bash
alembic downgrade -1
alembic upgrade head
```
