# Cadastru – project handout

State as of 2026-11-17. Purpose: one place that holds the whole context, so a new conversation can start from here.

---

## 1. The project in one paragraph

Cadastru is a cadastre web application: it registers **land parcels**, the **buildings** on them and their **owners** (persons or companies), and keeps the **ownership history** (shares, price paid, periods). Stack: **plain Java 21** (Javalin, JDBC, HikariCP, no Spring), **Angular + TypeScript**, **PostgreSQL 17 in Docker**. It is a one-month learning project (course topics: algorithms, DSA, OOP, SOLID, design patterns, DB normal forms, Java/Angular/SQL, Git, Agile).

## 2. How the user wants to work

- **The user writes the code and the SQL by hand.** Claude explains, gives templates and hints, and reviews. Do not write files into the project unless asked.
- **Socratic style** when they ask for reasoning: questions first. When they ask for a recommendation, give one.
- **Do not install software** (installs were rejected twice). Use what is already on the Mac.
- **Check before overwriting a Word file:** if `~$name.docx` exists, Word has it open. Save to a new file name instead.
- **Never paste real passwords** in chat. The password lives in `.env`.
- Short, plain answers. When the user says "I don't get it", use a concrete example or an analogy.

## 3. Decisions already made

### Access model (three levels)
| Who | Sees / does |
|---|---|
| **Visitor** (no login) | Public search. Parcels and buildings shown only as **owned / not owned**. No names, no prices. Can register an account. |
| **User** (registered, not linked) | Same as visitor, plus log in / out. |
| **Owner** (account linked to an owner record) | Own properties in detail, ownership history. Read-only. |
| **Clerk** | Everything: edits register, manages owners, **links accounts to owners**, assigns / changes ownership. Clerk accounts are created in the database only. |

- **Account roles are only `user` and `clerk`.** "Owner" is a *fact* (the account is linked to an owner record), not a role.
- A person or company can own property **without** having an account.
- The role is **never** taken from the registration request.

### Data model rules
- `owner` is the "someone who can own" table: **exactly one** of `single_user_id` / `company_id` (CHECK), each unique.
- Ownership is in **two tables** (`parcel_ownership`, `building_ownership`), independent of each other.
- Co-owners are separate rows. `share` is a percentage (> 0 and <= 100); **price is what that owner paid for that share**.
- `end_date` is the **last day owned (inclusive)**; empty = current period. Periods of one owner on one property **never overlap** (exclusion constraint).
- A change of owner/share = **UPDATE** (close the current row: `end_date = new start - 1 day`) then **INSERT** (new row), **in one transaction**, UPDATE first.
- A building belongs to exactly **one parcel** (`parcel_id` NOT NULL). Owner of a building may differ from owner of the parcel.
- Land use and building type are **lookup tables**. Building has both `size_sqm` and `usable_area_sqm` (usable <= size), floors >= 1, `year_built`.
- Every FK refuses deletes where history exists (`RESTRICT`); `account.owner_id` is `ON DELETE SET NULL`.

### Rules checked in Java (not in the database)
- Sum of the current shares of a property <= 100%.
- A building may be registered only on an **owned** parcel.
- Full CNP validation (checksum, date). The DB only checks length 13.
- Anything that needs today's date (e.g. year not in the future).

## 4. The database (implemented and tested)

Connection: host `localhost`, port `5432`, database `cadastru`, user `cadastru_app`, password in `.env` (`POSTGRES_PASSWORD`).

| Table | Main columns |
|---|---|
| `account` | id, email (unique), password_hash varchar(60), role (`user`/`clerk`), owner_id (unique, optional, FK owner) |
| `owner` | id, single_user_id (unique FK), company_id (unique FK) |
| `single_user` | id, cnp varchar(13) unique, first_name, last_name, phone (optional) |
| `company` | id, tax_id unique, name |
| `parcel` | id, cadastral_number unique, address, size_sqm numeric(10,2), land_use_id FK |
| `land_use` | id, name unique (6 rows: Residential, Agricultural, Commercial, Industrial, Forest, Pasture) |
| `building` | id, cadastral_number unique, parcel_id FK, building_type_id FK, size_sqm, usable_area_sqm, floors, year_built |
| `building_type` | id, name unique (6 rows: House, Apartment block, Garage, Warehouse, Office building, Shed) |
| `parcel_ownership` | id, owner_id FK, parcel_id FK, share numeric(5,2), price numeric(14,2), start_date, end_date |
| `building_ownership` | same, with building_id |

All ids: `integer generated always as identity`. Extensions: `btree_gist`. Every FK column has an index. Constraint names follow `<table>_<what>_check/_key/_fkey/_pkey/_excl` (a few older ones are `valid_cnp`, `valid_size`, `cnp`, `tax_id`; the user chose to keep them).

**Not done yet in the database**
1. **The schema is not saved as files.** `docs/sql/` is empty. If the Docker volume is lost, the database is lost. Next step: export to `docs/sql/01_schema.sql` + `02_seed.sql`.
2. The app currently connects as a **superuser** (`cadastru_app`). A production setup uses an owner role plus a limited app role.
3. No seed rows (no first clerk with a BCrypt hash, no sample parcels).
4. No `created_at` / `updated_at` / audit columns.
5. CNP check only tests length (not "digits only").

## 5. Environment and commands

Docker (Docker Desktop must be running), from `~/Project_Cadastru`:
```bash
docker compose up -d      # start database + pgAdmin
docker compose ps         # check
docker compose stop       # stop (data kept)
docker compose down -v    # DELETES the database data
docker exec -it cadastru-db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"'   # SQL shell
```
- `docker-compose.yml` services: `db` (postgres:17, port 5432), `pgadmin` (http://localhost:5050, login `admin@example.com`, password = `PGADMIN_DEFAULT_PASSWORD` in `.env`; the server "Cadastru (Docker)" is pre-registered; DB password = `POSTGRES_PASSWORD`).
- `.env` (ignored by Git): POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_PORT, PGADMIN_DEFAULT_EMAIL, PGADMIN_DEFAULT_PASSWORD, PGADMIN_PORT. `.env.example` is the committed template.
- Java: `openjdk@21` via Homebrew (keg-only; IntelliJ SDK name `homebrew-21`). Maven is bundled with IntelliJ.
- Nothing is committed to Git yet.

## 6. The Java backend (in progress)

Folder `backend/` (Maven project, package `ro.cadastru`): `Main.java`, `config/ConnectionFactory.java`, empty packages `handler`, `model`, `repository`, `service`. `pom.xml` has JUnit 5 and the PostgreSQL driver 42.7.4 (HikariCP, Javalin, Jackson, BCrypt not added yet).

Planned layers: `handler` (Javalin routes) → `service` (rules, roles, transactions) → `repository` (interfaces + `jdbc/` implementations) → PostgreSQL; plus `model`, `dto`, `config`, `exception`, `util`. Patterns: Repository, Singleton (ConnectionFactory / pool), Factory (RepositoryFactory), Builder, DTO.

### ConnectionFactory – where we stopped
Thread-safe **holder-class Singleton** with `private final` fields set in the constructor. **Still to fix (compile/behaviour):**
1. `System.getenv("POSTGRES_PASS")` must be `"POSTGRES_PASSWORD"`.
2. URL must be `"jdbc:postgresql://localhost:5432/" + System.getenv("POSTGRES_DB")` (it was `DB + DB`).
3. `getConnection()` should be `public Connection getConnection() throws SQLException { return DriverManager.getConnection(url, user, pass); }` (argument order: **url, user, password**; missing semicolon; no `LOGGER`; do not return `null`).
4. Remove the unused logger imports.
5. Optional: a `requireEnv(name)` helper that fails early with a clear message; camelCase field names.

**First test** (in `Main`): get a connection in `try-with-resources`, run `SELECT count(*) FROM land_use`, print the number. Expected result: **6**.

### IntelliJ setup lessons
- Add `backend/pom.xml` as a **Maven project** (right-click → Add as Maven Project), otherwise "Java Class" is missing from the New menu.
- Run with an **Application** configuration (not Maven): JDK 21, module `cadastru-backend`, main class `ro.cadastru.Main`.
- **Environment variables**: load `.env` with the folder icon (in the macOS dialog press Cmd+Shift+. to show hidden files) or type `POSTGRES_DB=...;POSTGRES_USER=...;POSTGRES_PASSWORD=<real value>`. Never leave a placeholder like `<value from .env>`.

## 7. Documents and where they are

| File | What it is |
|---|---|
| `~/System_Requirements_Cadastru.docx` | Requirements (version 1 + a design chapter I added). **May be open in Word.** |
| `~/System_Requirements_Cadastru_v2.docx` | **Version 2**: Visitor/User actors added, use cases updated (Clerk 11, Owner 6, Visitor 3), glossary updated, design chapter removed. Rename over the old one after closing Word. |
| `docs/Analysis_Design_Cadastru.docx` | **Analysis & Design** document filled into the course template (10 sections, ~25 figures, UI mock-ups). Built from `T_SWDP_Analysis&Design_Template_Engl.doc`. |
| `docs/Cadastru_Design_Diagrams_1-5.docx` | Earlier standalone diagrams document (can be deleted). |
| `docs/diagrams/*.png` | All diagrams (2x PNG): architecture, flows, class, ER, object, sequence, use cases, activity, state, package, component, communication, UI mock-ups. |
| `docs/diagrams/src/` | Python sources (`gen_diagrams.py`, `gen_extra.py`, `build_ad.py`, `build_docx.py`, `lib.py`, `gen_sketch.py`). They generate the PNGs and the Word files without installing anything (macOS Quick Look + `sips`). |
| `docs/HANDOUT.md` | This file. |

**Pending on the documents**
- The user said they **did not like the hand-sketched mock-ups** and prefer the **first (clean) mock-ups**. `gen_sketch.py` produced the sketch version; do not use it. The `ui_*.png` in `docs/diagrams/` and in `Analysis_Design_Cadastru.docx` are the clean ones.
- The user asked to **add a "road map" (screen navigation map) showing how the screens connect** (public search, login/register, owner screens, clerk screens), drawn in the same style as the first mock-ups. Not done yet.
- Requirements doc: update the table of contents in Word (right-click → Update Field).
- Analysis & Design: the screenshots section still contains mock-ups; replace with real screenshots once Angular exists. Check the competing-software table and the date.

## 8. Next steps (suggested order)

1. Fix `ConnectionFactory` (section 6) and run the `SELECT count(*)` test.
2. Export the schema + lookup data to `docs/sql/` and make the first Git commit.
3. First vertical slice in Java: `Parcel` model + `ParcelRepository` (interface) + `JdbcParcelRepository` + a tiny test.
4. Add HikariCP (the Singleton then holds the pool), then Javalin and the first endpoint.
5. Add BCrypt + login, then the role checks.
6. Angular frontend, screen by screen (public search first).
7. Production hardening of the database: limited app role, seed clerk, timestamps/audit, backups, versioned migrations.
8. Finish the documents (screen map, screenshots).
