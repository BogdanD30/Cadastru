"""Builds docs/Analysis_Design_Cadastru.docx following the structure of T_SWDP_Analysis&Design_Template_Engl."""
import zipfile, struct, os
from xml.sax.saxutils import escape as esc
BUILD = os.environ.get("BUILD", "/private/tmp/claude-501/-Users-dindiliganbogdan-Project-Cadastru/83778627-cef0-4add-bc92-88247cfbe8f3/scratchpad/build")
OUT = os.environ.get("OUT", "/Users/dindiliganbogdan/Project_Cadastru/docs/Analysis_Design_Cadastru.docx")
EMU = 914400; STUDENT = "Dindiligan Bogdan"; PROJECT = "Cadastru"; DATE = "11.11.2026"
body, rels, media = [], [], []; nfig = [0]; did = [200]

def png_size(p):
    d = open(p, "rb").read(32); return struct.unpack(">II", d[16:24])
def run(t, b=False, i=False, u=False, sz=None):
    pr = ("<w:b/>" if b else "") + ("<w:i/>" if i else "") + ('<w:u w:val="single"/>' if u else "") + (f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>' if sz else "")
    return f'<w:r>{"<w:rPr>"+pr+"</w:rPr>" if pr else ""}<w:t xml:space="preserve">{esc(t)}</w:t></w:r>'
def para(t="", style=None, align=None, keep=False, pbb=False, before=None, after=None, b=False, i=False, runs=None):
    ppr = (f'<w:pStyle w:val="{style}"/>' if style else '') + ('<w:keepNext/>' if keep else '') + ('<w:pageBreakBefore/>' if pbb else '')
    if before is not None or after is not None: ppr += '<w:spacing' + (f' w:before="{before}"' if before is not None else '') + (f' w:after="{after}"' if after is not None else '') + '/>'
    if align: ppr += f'<w:jc w:val="{align}"/>'
    return f'<w:p>{"<w:pPr>"+ppr+"</w:pPr>" if ppr else ""}{runs if runs is not None else run(t, b=b, i=i)}</w:p>'
def P(t, **k): body.append(para(t, **k))
def H1(t, pbb=False): body.append(para(t, style="Heading1", pbb=pbb, keep=True))
def H2(t, pbb=False): body.append(para(t, style="Heading2", pbb=pbb, keep=True))
def H3(t, pbb=False): body.append(para(t, style="Heading3", pbb=pbb, keep=True))
def bullets(items):
    for t in items:
        body.append('<w:p><w:pPr><w:pStyle w:val="ListBullet"/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr></w:pPr>' + (run(t) if isinstance(t, str) else run(t[0], b=True) + run(t[1])) + '</w:p>')
def numbered(items):
    for n, t in enumerate(items, 1):
        body.append(f'<w:p><w:pPr><w:pStyle w:val="ListNumber"/><w:ind w:left="500" w:hanging="360"/></w:pPr>{run(str(n)+".  ")}{run(t)}</w:p>')

def table(widths, rows, header=True, sz=19, align_first=None):
    tw = sum(widths)
    x = f'<w:tbl><w:tblPr><w:tblW w:w="{tw}" w:type="dxa"/><w:tblBorders>' + "".join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="808080"/>' for s in ("top","left","bottom","right","insideH","insideV")) + '</w:tblBorders><w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="40" w:type="dxa"/><w:left w:w="80" w:type="dxa"/><w:bottom w:w="40" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tblGrid>' + "".join(f'<w:gridCol w:w="{w}"/>' for w in widths) + '</w:tblGrid>'
    for ri, r in enumerate(rows):
        hd = header and ri == 0
        x += '<w:tr>' + ('<w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>' if hd else '<w:trPr><w:cantSplit/></w:trPr>')
        for ci, (c, w) in enumerate(zip(r, widths)):
            shade = '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>' if hd else ''
            x += f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{shade}</w:tcPr><w:p><w:pPr><w:spacing w:after="0"/></w:pPr>{run(c, b=hd or (ci == 0 and align_first), sz=sz)}</w:p></w:tc>'
        x += '</w:tr>'
    body.append(x + '</w:tbl>'); body.append(para("", after=60))

def fig(file, caption, max_w, max_h):
    nfig[0] += 1; path = os.path.join(BUILD, file); w, h = png_size(path); r = w / h
    hi = max_h; wi = hi * r
    if wi > max_w: wi = max_w; hi = wi / r
    cx, cy = int(wi*EMU), int(hi*EMU); rid = f"rIdAd{nfig[0]}"; name = f"ad_{nfig[0]:02d}.png"
    rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{name}"/>')
    media.append((name, path)); did[0] += 1
    dr = (f'<w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:docPr id="{did[0]}" name="Figure {nfig[0]}" descr="{esc(caption)}"/>'
          f'<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
          f'<pic:nvPicPr><pic:cNvPr id="{did[0]}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing>')
    body.append(f'<w:p><w:pPr><w:keepNext/><w:spacing w:before="60" w:after="30"/><w:jc w:val="center"/></w:pPr><w:r>{dr}</w:r></w:p>')
    body.append(para(f"Figure {nfig[0]} – {caption}", style="Caption", align="center"))

MARP = '<w:pgMar w:top="1600" w:right="1134" w:bottom="1300" w:left="1134" w:header="400" w:footer="300" w:gutter="0"/>'
def sect(o):
    pg = '<w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/>' if o == "L" else '<w:pgSz w:w="11906" w:h="16838"/>'
    return f'<w:sectPr><w:headerReference w:type="default" r:id="rIdHdr"/><w:footerReference w:type="default" r:id="rIdFtr"/>{pg}{MARP}</w:sectPr>'
def end_section(o): body.append(f'<w:p><w:pPr><w:spacing w:after="0"/>{sect(o)}</w:pPr></w:p>')
PW, PH = 6.6, 6.9       # portrait image box (inches)
LW, LH = 10.0, 4.5      # landscape image box

# ================= front page =================
P("Versions:", b=True, after=60)
table([1500, 1300, 2200, 3600], [["Date", "Versiune", "Autor", "Comentarii"], [DATE, "0.1", STUDENT, "Initial draft: all sections filled in"], ["", "", "", ""]])
body.append(para("", runs=run(f"Analysis & Design for {PROJECT}", b=True, u=True, sz=40), align="center", before=240, after=200))
P("Continut:", b=True, after=80)
for n, t in enumerate(["General Presentation", "Theoretical Fundamentals", "IT Technology (which will be implemented)", "Functionalities", "Actors and related access rights", "Use Case Diagrams", "System Architecture", "Design (UML Diagrams)", "Operation Mode (Operation Guide, including screen-shots)", "Portability"], 1):
    body.append(f'<w:p><w:pPr><w:spacing w:after="80"/><w:ind w:left="500" w:hanging="360"/></w:pPr>{run(str(n)+".", b=True, sz=26)}{run("  "+t, b=True)}</w:p>')

# ================= 1 =================
H1("1. General Presentation", pbb=True)
H2("1.1 What Cadastru is")
P("Cadastru is a web application for registering and managing land parcels, the buildings located on them and their owners. It replaces paper records and spreadsheets with one searchable register in which every parcel, building and owner is stored once and linked correctly. Ownership is recorded over time, with the share of each owner, the price paid and the period of ownership, so the full history of a property is kept.")
H2("1.2 Goals")
bullets(["Keep one consistent, searchable register of parcels, buildings and owners (persons and companies).",
         "Record ownership with shares, prices and periods, including co-owners, and keep the history.",
         "Give each kind of user exactly the access they need: public view, owner view and clerk view.",
         "Protect the data: the database refuses invalid data even if the application has a bug.",
         "Build the system with plain Java, Angular and PostgreSQL, so that the design patterns and the SQL stay visible."])
H2("1.3 Users")
P("Three kinds of users work with the system: visitors, who can search the register without logging in and see only whether a parcel or building is owned; owners, who have an account linked to an owner record and see their own properties in detail; and clerks, who maintain the register. They are described in section 5.")
H2("1.4 Current status")
table([2800, 6800], [["Part", "Status"],
    ["Requirements and use cases", "Written (System Requirements document: actors, use cases, glossary)."],
    ["Database", "Designed, created and tested in PostgreSQL 17 (10 tables, constraints, indexes, sample lookup data)."],
    ["Design documentation", "This document: architecture, UML diagrams and UI mock-ups."],
    ["Backend (Java)", "Project skeleton only. Handlers, services and repositories are still to be implemented."],
    ["Frontend (Angular)", "Not started. Screens are designed as mock-ups (section 9)."]])

# ================= 2 =================
H1("2. Theoretical Fundamentals", pbb=True)
H2("2.1 Cadastre and land register")
P("A cadastre is an official register of land parcels and the buildings on them. Each parcel and building has a unique cadastral number, an address and a size. Ownership is recorded separately from the property because it changes over time: a property can be sold, inherited or shared between co-owners. A register therefore needs the history of ownership, not only the current owner.")
H2("2.2 Relational data model")
bullets([("Keys and constraints. ", "Primary keys identify rows, foreign keys link tables, and UNIQUE, NOT NULL and CHECK constraints make the database refuse invalid data."),
         ("Normalization. ", "The tables follow the normal forms up to 3NF: no lists inside a column, and no value stored twice. A many-to-many relationship (owners and properties) is resolved with an association table that also carries its own data (share, price, dates)."),
         ("Time-dependent data. ", "Each ownership row has a start and an end date. The current owner is the row with an empty end date. An exclusion constraint on the date range forbids overlapping periods for the same owner and property."),
         ("Lookup tables. ", "Land use and building type are separate tables so that values are consistent and can be searched."),
         ("Transactions (ACID). ", "A change of ownership closes one row and inserts another in one transaction, so the history is never left half changed.")])
H2("2.3 Layered architecture and REST")
P("The backend is split into handler, service and repository layers. Handlers translate HTTP requests into calls, services contain the business rules, and repositories talk to the database. The frontend communicates with the backend through a REST API that exchanges JSON. Each layer depends only on the layer below it, which keeps the code testable and easy to change.")
H2("2.4 Object-oriented design and design patterns")
bullets([("SOLID. ", "Single responsibility per class, services depend on interfaces and not on JDBC classes, and new behaviour is added by extension."),
         ("Repository. ", "An interface per entity hides how the data is stored (ParcelRepository, implemented by JdbcParcelRepository)."),
         ("Singleton. ", "One shared connection pool for the whole application (ConnectionPool)."),
         ("Factory. ", "One place that creates and wires the repositories (RepositoryFactory)."),
         ("Builder. ", "Step-by-step construction of objects with many fields (ParcelBuilder)."),
         ("DTO. ", "Separate objects for the API so that internal classes are not exposed (ParcelDto).")])
H2("2.5 Security fundamentals")
bullets(["Authentication with an email and a password. Passwords are stored only as BCrypt hashes.",
         "Role-based access control. The role comes from the server and never from the registration request. Access to data is checked in the service layer, not only in the interface.",
         "All SQL goes through PreparedStatement to prevent SQL injection.",
         "Validation in two places (defense in depth): the service gives clear messages, and the database refuses bad data as a safety net."])
H2("2.6 UML")
P("The design uses these UML diagrams: use case, class, object, sequence, activity, state machine, package, component and communication diagrams. They are complemented by flow charts, an architecture diagram and an entity-relationship (ER) diagram of the database.")

# ================= 3 =================
H1("3. IT Technology (which will be implemented)", pbb=True)
table([1500, 2600, 3900, 1600], [["Layer", "Technology", "Role", "Status"],
    ["Database", "PostgreSQL 17", "Stores the register; enforces keys, checks and the no-overlap rule.", "Implemented"],
    ["Database", "btree_gist extension", "Exclusion constraint on ownership date ranges.", "Implemented"],
    ["Infrastructure", "Docker, Docker Compose", "Runs the database and pgAdmin the same way on every machine.", "Implemented"],
    ["Tools", "pgAdmin", "Browser tool for tables, queries and ER diagrams.", "Implemented"],
    ["Backend", "Java 21 (plain Java)", "Application language; no Spring framework.", "Skeleton"],
    ["Backend", "Javalin", "Small HTTP and routing library on top of Jetty.", "Planned"],
    ["Backend", "JDBC + PostgreSQL driver", "Data access with PreparedStatement.", "Planned"],
    ["Backend", "HikariCP", "Connection pool (Singleton).", "Planned"],
    ["Backend", "Jackson", "JSON for the REST API.", "Planned"],
    ["Backend", "BCrypt library", "Password hashing.", "Planned"],
    ["Backend", "JUnit 5, Mockito", "Unit tests of the service layer.", "Planned"],
    ["Frontend", "Angular, TypeScript, HTML, CSS", "Single-page web application.", "Planned"],
    ["Build and tools", "Maven, Git, IntelliJ IDEA", "Build, version control and IDE.", "In use"]], sz=18)
P("Plain Java with a small HTTP library was chosen over a full framework so that the architecture, the design patterns and the SQL are written and understood by hand. The database is the central part of the design: it carries the rules that must always hold.")

# ================= 4 =================
H1("4. Functionalities", pbb=True)
table([700, 4500, 2000, 1500], [["ID", "Functionality", "Actor", "Priority"],
    ["F1", "Public search of parcels and buildings; the result shows only owned or not owned.", "Visitor", "MVP"],
    ["F2", "Register an account (email and password).", "Visitor", "MVP"],
    ["F3", "Log in and log out.", "User, Owner, Clerk", "MVP"],
    ["F4", "View my properties, their details and their ownership history.", "Owner", "MVP"],
    ["F5", "Register and edit parcels (with land use).", "Clerk", "MVP"],
    ["F6", "Register and edit buildings on a parcel (with type, areas, floors, year).", "Clerk", "MVP"],
    ["F7", "Manage owners: persons and companies.", "Clerk", "MVP"],
    ["F8", "Link an account to an owner record.", "Clerk", "MVP"],
    ["F9", "Assign and change ownership: share, price, start date, co-owners, history.", "Clerk", "MVP"],
    ["F10", "Search the whole register with all details.", "Clerk", "MVP"],
    ["F11", "Data integrity rules in the database and in the service.", "System", "MVP"]], sz=18)
P("Planned for later: a map view of the parcels (PostGIS and Leaflet), a request workflow where an owner asks a clerk to register a building, meters and readings for buildings, an audit log of who changed what, email confirmation and password reset, extracts and reports, versioned database migrations and backups.", before=80)
P("Out of scope: the application has no legal value and does not replace an official land register.")

# ================= 5 =================
H1("5. Actors and related access rights", pbb=True)
bullets([("Visitor. ", "Anyone without a login. Searches the register and sees only whether a parcel or building is owned."),
         ("User. ", "A registered account that is not yet linked to an owner. Sees the same as a visitor."),
         ("Owner. ", "An account linked to an owner record (a person or a company). Sees the details and the ownership history of their own properties. Read-only."),
         ("Clerk. ", "An employee who maintains the register. Has full access. Clerk accounts are created in the database, never through public registration.")])
P("“Owner” is not a role. The role of an account is user or clerk, and an account is an owner when it is linked to an owner record. A person or a company can own property without having an account.", before=60)
table([3600, 1400, 1400, 1400, 1400], [["Capability", "Visitor", "User", "Owner", "Clerk"],
    ["Search: owned / not owned (public view)", "Yes", "Yes", "Yes", "Yes"],
    ["See owner names, shares, prices, history", "No", "No", "Own properties", "All"],
    ["Register an account", "Yes", "No", "No", "No"],
    ["Log in and log out", "No", "Yes", "Yes", "Yes"],
    ["View my properties and details", "No", "No", "Yes", "No"],
    ["Register and edit parcels and buildings", "No", "No", "No", "Yes"],
    ["Manage owners", "No", "No", "No", "Yes"],
    ["Link accounts to owners", "No", "No", "No", "Yes"],
    ["Assign and change ownership", "No", "No", "No", "Yes"]], sz=18)
P("Access is enforced on the server. Hiding a menu item in the interface is not security: every endpoint checks the role and, for owners, that the data belongs to them.")

# ================= 6 =================
H1("6. Use Case Diagrams", pbb=True)
P("The use cases are described in detail in the System Requirements document (preconditions, postconditions and behaviour). This section gives the diagrams and a summary.", keep=True)
fig("uc_visitor.png", "Use case diagram: Visitor", 5.0, 2.4)
fig("uc_owner.png", "Use case diagram: Owner", 5.0, 3.7)
fig("uc_clerk.png", "Use case diagram: Clerk", 5.0, 6.4)
table([700, 3200, 1500, 4200], [["ID", "Use case", "Actor", "Short description"],
    ["UC1", "Search parcels and buildings", "Visitor", "Public search; shows only owned or not owned."],
    ["UC2", "Register account", "Visitor", "Creates an account with the role user and no owner link."],
    ["UC3", "Log in", "All accounts", "Authenticates with email and password."],
    ["UC4", "Log out", "All accounts", "Ends the session."],
    ["UC5", "Search register (own details)", "Owner", "Search with details for the owner's own properties."],
    ["UC6", "View my properties", "Owner", "Lists the parcels and buildings of the owner."],
    ["UC7", "View property details", "Owner", "Shows the details of one of the owner's properties."],
    ["UC8", "View ownership history", "Owner, Clerk", "Shows owners, shares, prices and dates of a property."],
    ["UC9", "Register parcel", "Clerk", "Adds a parcel with cadastral number, address, size and land use."],
    ["UC10", "Edit parcel", "Clerk", "Changes the data of a parcel."],
    ["UC11", "Register building", "Clerk", "Adds a building on an existing parcel."],
    ["UC12", "Edit building", "Clerk", "Changes the data of a building."],
    ["UC13", "Manage owner", "Clerk", "Creates or updates a person or a company as an owner."],
    ["UC14", "Link account to owner", "Clerk", "Links a registered account to an owner record."],
    ["UC15", "Assign / change ownership", "Clerk", "Records a new owner or share and closes the previous period."],
    ["UC16", "Search register", "Clerk", "Searches the whole register with all details."]], sz=18)
end_section("P")

# ================= 7 (landscape) =================
H1("7. System Architecture")
P("The system is a three-tier web application. The Angular frontend runs in the browser and talks to the Java backend through a REST API with JSON. The backend is split into handler, service and repository layers and reaches PostgreSQL, which runs in Docker, through JDBC and a HikariCP connection pool.", keep=True)
fig("d1_architecture.png", "General system architecture", LW, LH-0.6)
body.append(para("", pbb=True, after=0))
H2("7.1 Deployment and responsibilities")
table([2600, 3300, 2200, 6000], [["Component", "Runs as", "Port", "Responsibility"],
    ["Angular application", "Static files in the browser (dev server during development)", "4200 (dev)", "Screens, forms, calls to the REST API, route guards by role."],
    ["Java application", "One JVM process", "8080 (configurable)", "REST API, business rules, role checks, transactions."],
    ["PostgreSQL 17", "Docker container cadastru-db", "5432", "Data, constraints, indexes, no-overlap rule."],
    ["pgAdmin", "Docker container cadastru-pgadmin", "5050 (localhost only)", "Administration and ER diagrams for developers."]], sz=18)
bullets(["Errors are mapped to HTTP codes: 401 for a failed login, 403 when access is not allowed, 409 for a conflict such as a duplicate cadastral number or an overlapping ownership period.",
         "The database is configured through environment variables and the files docker-compose.yml and .env, so it can be recreated on any machine."])

# ================= 8 (landscape part) =================
H1("8. Design (UML Diagrams)", pbb=True)
P("The diagrams below are based on the implemented PostgreSQL schema.", keep=True)
H2("8.1 Class diagrams")
P("An Account has a role and may be linked to one Owner, who is a person or a company. Ownership classes connect an owner to a parcel or a building over time.", keep=True)
fig("d3a_class_domain.png", "Class diagram: domain model", LW, LH-0.4)
H3("Backend structure and design patterns", pbb=True)
P("Handler → Service → Repository, with the patterns Repository, DTO, Builder, Factory and Singleton (shown for Parcel).", keep=True)
fig("d3b_class_patterns.png", "Class diagram: backend structure and design patterns", LW, LH-0.2)
H2("8.2 Database schema (ER diagram)", pbb=True)
P("The ten tables as created in PostgreSQL, with keys, unique and optional columns and the rules enforced by the database.", keep=True)
fig("d3c_database_er.png", "Database schema (ER diagram)", LW, LH)
H2("8.3 Object diagram", pbb=True)
P("A snapshot of real data: Ion Popescu owned 100% of parcel 100234 until 2024-02-29. Since 2024-03-01 Delta Build SRL holds 60% and Ion keeps 40%. Delta Build SRL also owns the building.", keep=True)
fig("d4_object.png", "Object diagram: ownership of parcel 100234", LW, LH-0.2)
H2("8.4 Sequence diagrams", pbb=True)
H3("Log in")
P("The service loads the account, verifies the password hash and returns a token and the role, or a 401 error.", keep=True)
fig("d5a_seq_login.png", "Sequence diagram: log in", LW, LH-0.5)
H3("Register a parcel", pbb=True)
P("The service checks the role, validates the data and checks that the cadastral number is new before saving. A duplicate ends with a 409 Conflict.", keep=True)
fig("d5b_seq_register_parcel.png", "Sequence diagram: register a parcel", LW, LH-0.1)
H3("View the ownership history", pbb=True)
P("The service checks that the parcel belongs to the logged-in owner before returning its history; otherwise it answers 403 Forbidden.", keep=True)
fig("d5c_seq_ownership_history.png", "Sequence diagram: view the ownership history", LW, LH-0.1)
H3("Change ownership", pbb=True)
P("The service closes the current row, inserts the new one and commits. If the database refuses either statement, everything is rolled back and the clerk sees a 409 Conflict.", keep=True)
fig("d5d_seq_change_ownership.png", "Sequence diagram: change ownership", LW, LH-0.2)
H2("8.5 State machine diagrams", pbb=True)
P("The life of an account, from registration to the link with an owner, and the life of one ownership period.", keep=True)
fig("state_account_ownership.png", "State machine diagrams: account and ownership period", LW, LH-0.2)
H2("8.6 Package diagram", pbb=True)
P("The Java packages of the backend, the Angular modules of the frontend and the dependencies between them.", keep=True)
fig("pkg_packages.png", "Package diagram", LW, LH)
H2("8.7 Component diagram", pbb=True)
P("The deployable components and the interfaces between them: REST/JSON between the browser and the backend, and JDBC between the backend and PostgreSQL.", keep=True)
fig("cmp_components.png", "Component diagram", LW, LH-0.5)
H2("8.8 Communication diagram", pbb=True)
P("The same scenario as the sequence diagram “Register a parcel”, shown as objects with numbered messages.", keep=True)
fig("com_register_parcel.png", "Communication diagram: a clerk registers a parcel", LW, LH-0.6)
end_section("L")

# ================= 8.9 + 9 + 10 (portrait) =================
H2("8.9 Activity diagram and flow charts")
P("The activity diagram shows who does what when a visitor becomes an owner. The flow charts show the logic of four operations. Diamonds are decisions, red boxes are error paths and green boxes are successful results.", keep=True)
fig("act_become_owner.png", "Activity diagram with swimlanes: a visitor becomes an owner", PW, PH-0.5)
H3("Flow chart: log in", pbb=True)
fig("d2a_login.png", "Flow chart: log in", PW, PH)
H3("Flow chart: register a parcel", pbb=True)
fig("d2b_register_parcel.png", "Flow chart: register a parcel", PW, PH)
H3("Flow chart: search the register", pbb=True)
fig("d2c_search.png", "Flow chart: search the register", PW, PH)
H3("Flow chart: change ownership", pbb=True)
fig("d2d_change_ownership.png", "Flow chart: change ownership", PW, PH)

# ================= 9 =================
H1("9. Operation Mode (Operation Guide, including screen-shots)", pbb=True)
H2("9.1 Operation guide")
H3("Visitor")
numbered(["Open the application and go to Search.", "Enter a cadastral number, an address or a property type and press Search.", "The result lists parcels and buildings with the status Owned or Not owned. Names and prices are not shown.", "To see more, choose Register and create an account."])
H3("Becoming an owner")
numbered(["Register an account with an email and a password.", "Visit the clerk with an identity document and the documents about the property.", "The clerk verifies them, creates the owner record if needed and links the account to it.", "Log in again: My properties now lists the properties of the owner."])
H3("Owner")
numbered(["Log in and open My properties.", "Select a parcel or a building to see its details.", "Open the ownership history to see owners, shares, prices and dates. The data is read-only."])
H3("Clerk")
numbered(["Log in with a clerk account.", "Register a parcel: cadastral number, address, size and land use. Then register the buildings on it.", "Create the owners (person or company) and link an account to an owner when the owner asks for access.", "Assign ownership: choose the property and the owner, enter the share, the price and the start date. To change an owner or a share, enter the new values with the new start date: the current period is closed the day before.", "Use Search to find any parcel or building with all its details."])
H2("9.2 User interface design", pbb=True)
P("The Angular application is not implemented yet. The screens below are mock-ups that show the intended interface. Screen-shots of the running application will replace them when the frontend is ready.", keep=True)
fig("ui_public_search.png", "Mock-up: public search", 5.6, 3.9)
fig("ui_login.png", "Mock-up: log in", 5.6, 3.0)
fig("ui_owner.png", "Mock-up: owner, my properties and ownership history", 5.6, 4.4)
fig("ui_clerk_parcel.png", "Mock-up: clerk, register a parcel", 5.6, 4.3)

# ================= 10 =================
H1("10. Portability", pbb=True)
bullets(["The backend runs on any system with Java 21 (Windows, macOS, Linux). The frontend runs in current browsers and needs no installation.",
         "The database runs in a Docker container, so it behaves the same on every machine. Configuration is read from environment variables.",
         "The SQL is standard apart from a few PostgreSQL features: identity columns, the exclusion constraint with btree_gist, and the role type. Moving to another database would mean replacing the no-overlap rule with a trigger or a check in the service.",
         "The Repository pattern keeps all SQL in one layer, so a change of database affects only the repository implementations.",
         "The schema and the seed data are kept as scripts, so the database can be rebuilt from scratch."])
H2("Competing software")
table([2400, 3300, 3900], [["Software", "What it is", "Difference from Cadastru"],
    ["eTerra (ANCPI, Romania)", "National platform for cadastre and land book information.", "Official and legally valid; Cadastru is a small educational system without legal value."],
    ["ArcGIS (Esri)", "Commercial GIS suite, used for parcel and land administration.", "Map-centred and much larger; Cadastru starts with the register and the ownership history."],
    ["QGIS", "Open-source GIS application for viewing and editing spatial data.", "A desktop GIS tool; Cadastru is a web application with roles and a focus on ownership records."]], sz=18)
P("A map view is planned for a later stage (PostGIS in the database and Leaflet in the frontend), which would bring Cadastru closer to these tools.", before=60)

NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"')
document = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS}><w:body>{"".join(body)}{sect("P")}</w:body></w:document>'

def cell(w, inner, borders=True, span=None):
    return f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{f"<w:gridSpan w:val=\"{span}\"/>" if span else ""}</w:tcPr>{inner}</w:tc>'
def cp(t, sz=18, b=False, i=False, align=None, size=None):
    return f'<w:p><w:pPr><w:spacing w:after="0"/>{f"<w:jc w:val=\"{align}\"/>" if align else ""}</w:pPr>{run(t, b=b, i=i, sz=sz)}</w:p>'
BT = '<w:tblBorders>' + "".join(f'<w:{s} w:val="single" w:sz="6" w:space="0" w:color="000000"/>' for s in ("top","left","bottom","right","insideH","insideV")) + '</w:tblBorders>'
header = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr {NS}><w:tbl><w:tblPr><w:tblW w:w="9638" w:type="dxa"/>{BT}<w:tblLayout w:type="fixed"/></w:tblPr><w:tblGrid><w:gridCol w:w="2200"/><w:gridCol w:w="5438"/><w:gridCol w:w="2000"/></w:tblGrid>'
    f'<w:tr><w:trPr><w:trHeight w:val="760"/></w:trPr>{cell(2200, cp("Student:", 16)+cp(STUDENT, 18, True))}{cell(5438, cp(f"Analysis & Design for {PROJECT}", 28, align="center"))}{cell(2000, cp("", 16))}</w:tr>'
    f'<w:tr><w:trPr><w:trHeight w:val="300"/></w:trPr>{cell(2200, cp("", 16))}{cell(5438, cp("Code: T_SWDP_Analysis&Design", 18, i=True))}{cell(2000, cp("", 16))}</w:tr></w:tbl><w:p><w:pPr><w:spacing w:after="0"/></w:pPr></w:p></w:hdr>')
def fld(instr): return f'<w:r><w:rPr><w:sz w:val="16"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:rPr><w:sz w:val="16"/></w:rPr><w:instrText xml:space="preserve"> {instr} </w:instrText></w:r><w:r><w:rPr><w:sz w:val="16"/></w:rPr><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:rPr><w:sz w:val="16"/></w:rPr><w:t>1</w:t></w:r><w:r><w:rPr><w:sz w:val="16"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>'
footer = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr {NS}><w:tbl><w:tblPr><w:tblW w:w="9638" w:type="dxa"/>{BT}<w:tblLayout w:type="fixed"/></w:tblPr><w:tblGrid><w:gridCol w:w="2400"/><w:gridCol w:w="4638"/><w:gridCol w:w="2600"/></w:tblGrid>'
    f'<w:tr>{cell(2400, "<w:p><w:pPr><w:spacing w:after=\"0\"/></w:pPr>"+run("Page ", sz=16)+fld("PAGE")+run("/ ", sz=16)+fld("NUMPAGES")+"</w:p>")}{cell(4638, cp("Company/University Name: Universitatea Tehnica Cluj-Napoca, Romania", 16))}{cell(2600, cp("Format: T_GENERAL, Version: 1", 16))}</w:tr>'
    f'<w:tr>{cell(2400, cp("Recommended: 20.11.2017", 16))}{cell(4638, cp("Approved:", 16))}{cell(2600, cp("Code: T_SWDP_Analysis&Design", 16))}</w:tr></w:tbl><w:p><w:pPr><w:spacing w:after="0"/></w:pPr></w:p></w:ftr>')
FONT = '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Times New Roman" w:cs="Times New Roman"/>'
styles = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr>{FONT}<w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="en-GB"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="100" w:line="259" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="160" w:after="80"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="120" w:after="60"/><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:b/><w:i/><w:sz w:val="23"/><w:szCs w:val="23"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="caption"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="20" w:after="120"/></w:pPr><w:rPr><w:i/><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListBullet"><w:name w:val="List Bullet"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="60"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="ListNumber"><w:name w:val="List Number"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="60"/></w:pPr></w:style>
</w:styles>'''
numbering = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="hybridMultilevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="540" w:hanging="270"/></w:pPr><w:rPr>{FONT}</w:rPr></w:lvl></w:abstractNum><w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>'''
ctypes = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/><Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/><Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>'''
root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>'''
core = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>Analysis &amp; Design for {PROJECT}</dc:title><dc:creator>{STUDENT}</dc:creator></cp:coreProperties>'''
doc_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
 '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rIdNum" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
 '<Relationship Id="rIdHdr" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/><Relationship Id="rIdFtr" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>' + "".join(rels) + '</Relationships>')
import xml.dom.minidom as md
for x in (document, header, footer, styles, numbering, ctypes, doc_rels, root_rels, core): md.parseString(x.encode("utf8"))
if os.path.exists(OUT): os.remove(OUT)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", ctypes); z.writestr("_rels/.rels", root_rels); z.writestr("word/document.xml", document); z.writestr("word/styles.xml", styles)
    z.writestr("word/numbering.xml", numbering); z.writestr("word/header1.xml", header); z.writestr("word/footer1.xml", footer); z.writestr("word/_rels/document.xml.rels", doc_rels); z.writestr("docProps/core.xml", core)
    for n, p in media: z.write(p, "word/media/" + n)
print("written", OUT, os.path.getsize(OUT)//1024, "KB;", len(media), "figures")
