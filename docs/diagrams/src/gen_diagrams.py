import os, sys
from lib import *
BUILD = os.environ.get("BUILD", "/private/tmp/claude-501/-Users-dindiliganbogdan-Project-Cadastru/83778627-cef0-4add-bc92-88247cfbe8f3/scratchpad/build")

def box(S, x, y, w, h, fill, stroke, title, sub=None, tsize=13, ssize=11.5, rx=8):
    S.rect(x, y, w, h, fill, stroke, 1.5, rx)
    if sub:
        S.text(x+w/2, y+h/2-5, title, tsize, "middle", True, INK, maxw=w-12); S.text(x+w/2, y+h/2+13, sub, ssize, "middle", False, MUTED, maxw=w-12)
    else: S.text(x+w/2, y+h/2+4.5, title, tsize, "middle", True, INK, maxw=w-12)

# ======================= 1. architecture =======================
def d1():
    S = Svg(1050, 540)
    S.text(20, 36, "USERS", 12, "start", True, MUTED)
    users = [("Visitor", "no login, public view", 80), ("Owner", "linked account", 230), ("Clerk", "maintains the register", 380)]
    ush = []
    for t, sub, y in users:
        sh = Shape(20, y, 150, 76); ush.append(sh); box(S, sh.x, sh.y, sh.w, sh.h, C["act_f"], C["act_s"], t, sub, 14)
    S.text(210, 36, "FRONTEND", 12, "start", True, MUTED)
    S.rect(210, 50, 240, 470, C["fe_f"], C["fe_s"], 1.8, 12, op=0.55)
    S.text(330, 78, "Angular web application", 14, "middle", True, C["nav"]); S.text(330, 96, "TypeScript, runs in the browser", 11.5, "middle", False, MUTED)
    fe = [("Public search", "no login needed"), ("Login / Register", "account pages"), ("My properties", "owner: own details and history"),
          ("Clerk screens", "parcels, buildings, owners"), ("HTTP client service", "route guards, JWT / session")]
    fes = []
    for i, (t, sub) in enumerate(fe):
        sh = Shape(226, 118+i*76, 208, 60); fes.append(sh); box(S, sh.x, sh.y, sh.w, sh.h, "#FFFFFF", C["fe_s"], t, sub)
    S.text(550, 36, "BACKEND", 12, "start", True, MUTED)
    S.rect(550, 50, 270, 470, C["be_f"], C["be_s"], 1.8, 12, op=0.55)
    S.text(685, 78, "Java 21 application", 14, "middle", True, "#14532D"); S.text(685, 96, "plain Java + Javalin (no Spring)", 11.5, "middle", False, MUTED)
    layers = [("Handler layer", "REST routes, JSON, DTOs"), ("Service layer", "business rules, role checks"), ("Repository layer", "JDBC, PreparedStatement")]
    ls = []
    for i, (t, sub) in enumerate(layers):
        sh = Shape(566, 118+i*104, 238, 66); ls.append(sh); box(S, sh.x, sh.y, sh.w, sh.h, "#FFFFFF", C["be_s"], t, sub, 14)
    pool = Shape(566, 440, 238, 60); box(S, pool.x, pool.y, pool.w, pool.h, "#FFFFFF", C["be_s"], "Connection pool", "HikariCP  (Singleton)")
    for a, b in [(ls[0], ls[1]), (ls[1], ls[2]), (ls[2], pool)]: S.poly([a.a("b"), b.a("t")], end="arrow")
    S.label(ls[0].cx+8, ls[0].y+ls[0].h+22, "calls", 11); S.label(ls[1].cx+8, ls[1].y+ls[1].h+22, "calls", 11); S.label(ls[2].cx+8, ls[2].y+ls[2].h+26, "gets connection", 11)
    S.text(905, 36, "DATABASE", 12, "start", True, MUTED)
    S.rect(900, 50, 140, 470, C["db_f"], C["db_s"], 1.8, 12, dash="7 5", op=0.5)
    S.text(970, 74, "Docker container", 11.5, "middle", False, MUTED); S.text(970, 90, "cadastru-db", 11.5, "middle", True, MUTED)
    cx, cy, cw, ch = 915, 106, 110, 64
    S.add(f'<path d="M{cx},{cy+14} L{cx},{cy+ch-14} A{cw/2},14 0 0 0 {cx+cw},{cy+ch-14} L{cx+cw},{cy+14} A{cw/2},14 0 0 0 {cx},{cy+14} Z" fill="#FFFFFF" stroke="{C["db_s"]}" stroke-width="1.6"/>')
    S.add(f'<ellipse cx="{cx+cw/2}" cy="{cy+14}" rx="{cw/2}" ry="14" fill="#F8F2FC" stroke="{C["db_s"]}" stroke-width="1.6"/>')
    S.text(cx+cw/2, cy+42, "PostgreSQL 17", 12.5, "middle", True, INK, maxw=cw-8)
    S.rect(912, 186, 116, 318, "#FFFFFF", C["db_s"], 1.4, 8); S.text(970, 207, "Tables", 12, "middle", True, C["db_s"])
    tabs = ["account", "owner", "single_user", "company", "parcel", "land_use", "building", "building_type", "parcel_ownership", "building_ownership"]
    for i, t in enumerate(tabs): S.text(920, 231+i*26, t, 11, "start", False, INK, maxw=104)
    dbp = Shape(912, 186, 116, 318)
    for u, f in zip(ush, (fes[0], fes[2], fes[3])): S.poly([u.a("r"), (190, u.cy), (190, f.cy), (210, f.cy)], end="arrow")
    S.poly([ush[1].a("r"), (190, ush[1].cy), (190, fes[1].cy), (210, fes[1].cy)], end="arrow") if False else None
    S.label(180, ush[0].cy-8, "", 11)
    src, dst = fes[4], ls[0]
    S.poly([src.a("r"), (538, src.cy), (538, dst.cy), dst.a("l")], end="arrow2", start="arrow2", sw=2)
    S.text(530, src.cy-150, "HTTP + JSON", 12, "end", True, C["nav"]); S.text(530, src.cy-134, "(REST API)", 11.5, "end", False, MUTED)
    r = ls[2]; S.poly([r.a("r"), (dbp.x, r.cy)], end="arrow2", start="arrow2", sw=2)
    S.text(862, r.cy-9, "JDBC / SQL", 11.5, "middle", True, C["db_s"]); S.text(862, r.cy+19, "port 5432", 11, "middle", False, MUTED)
    return export(S, "d1_architecture", BUILD)

# ======================= 2. flow charts =======================
def d2a():
    F = Flow(920, 780); X = 410
    F.term("s", X, 34, "Start"); F.proc("open", X, 104, "Open the login page")
    F.proc("enter", X, 176, ["Enter email and password", "and press Log in"])
    F.dec("chk", X, 286, ["Account exists and", "password is correct?"], w=270, h=92)
    F.proc("err", 755, 286, ["Show error message", "(401 Unauthorized)"], kind="err", w=220)
    F.proc("sess", X, 398, ["Create session / token", "and load the account role"])
    F.dec("role", X, 510, "Is the account a clerk?", w=250, h=80)
    F.proc("clerk", 730, 510, ["Open the clerk", "home page"], w=190, kind="ok")
    F.dec("link", X, 630, ["Account is linked", "to an owner?"], w=240, h=84)
    F.proc("owner", 730, 630, ["Open the owner home page", "(own properties)"], w=200, kind="ok")
    F.proc("pub", 105, 630, ["Open the public view", "(owned / not owned)"], w=180, kind="ok")
    F.term("e", X, 740, "End")
    F.edge("s","b","open","t"); F.edge("open","b","enter","t"); F.edge("enter","b","chk","t")
    F.edge("chk","r","err","l","No"); F.edge("chk","b","sess","t","Yes")
    F.edge("err","t","enter","r", via=[(755,176)]); F.edge("sess","b","role","t")
    F.edge("role","r","clerk","l","Yes"); F.edge("role","b","link","t","No")
    F.edge("link","r","owner","l","Yes"); F.edge("link","l","pub","r","No")
    F.edge("clerk","r","e","r", via=[(875,510),(875,740)])
    F.edge("owner","b","e","r"); F.edge("pub","b","e","l")
    return export(F.S, "d2a_login", BUILD)

def d2b():
    F = Flow(920, 700); X = 410
    F.term("s", X, 34, "Start"); F.dec("login", X, 118, "Clerk logged in?", w=240, h=72)
    F.proc("redir", 690, 118, ["Redirect to", "the login page"], w=170, kind="err"); F.term("e2", 845, 118, "End", w=90)
    F.proc("form", X, 214, ["Fill in cadastral number, address,", "size and land use"], w=260)
    F.dec("valid", X, 312, "Data valid?", w=210, h=76); F.proc("verr", 760, 312, ["Show validation", "errors"], w=190, kind="err")
    F.dec("dup", X, 428, ["Cadastral number", "already registered?"], w=260, h=88)
    F.proc("derr", 760, 428, ["Show duplicate error", "(409 Conflict)"], w=190, kind="err")
    F.proc("save", X, 542, ["Save the parcel in", "the database"]); F.proc("conf", X, 610, "Show confirmation message", kind="ok"); F.term("e", X, 672, "End")
    F.edge("s","b","login","t"); F.edge("login","r","redir","l","No"); F.edge("redir","r","e2","l"); F.edge("login","b","form","t","Yes")
    F.edge("form","b","valid","t"); F.edge("valid","r","verr","l","No"); F.edge("verr","t","form","r", via=[(760,214)])
    F.edge("valid","b","dup","t","Yes"); F.edge("dup","r","derr","l","Yes"); F.edge("derr","r","form","r", via=[(880,428),(880,214)])
    F.edge("dup","b","save","t","No"); F.edge("save","b","conf","t"); F.edge("conf","b","e","t")
    return export(F.S, "d2b_register_parcel", BUILD)

def d2c():
    F = Flow(920, 860); X = 410
    F.term("s", X, 34, "Start")
    F.proc("crit", X, 104, ["Enter search criteria: number,", "address, owner or property type"], w=260)
    F.dec("d1", X, 210, "Logged in?", w=220, h=72)
    F.proc("A", 760, 210, ["Public view:", "owned / not owned only"], w=200)
    F.dec("d2", X, 320, "Is the account a clerk?", w=250, h=76)
    F.proc("Cc", 760, 320, ["Whole register,", "all details"], w=200)
    F.dec("d3", X, 430, ["Account is linked", "to an owner?"], w=240, h=80)
    F.proc("B", 760, 430, ["Own properties in full detail,", "others: public view"], w=220)
    F.proc("P", 105, 430, ["Public view:", "owned / not owned only"], w=170)
    F.proc("run", X, 545, "Run the search")
    F.dec("res", X, 645, "Any results found?", w=240, h=76)
    F.proc("none", 100, 645, ["Show 'no results'", "message"], w=170, kind="err")
    F.proc("list", X, 750, ["Show the matching parcels", "and buildings"], kind="ok", w=230)
    F.term("e", X, 822, "End")
    F.edge("s","b","crit","t"); F.edge("crit","b","d1","t")
    F.edge("d1","r","A","l","No"); F.edge("d1","b","d2","t","Yes")
    F.edge("d2","r","Cc","l","Yes"); F.edge("d2","b","d3","t","No")
    F.edge("d3","r","B","l","Yes"); F.edge("d3","l","P","r","No")
    F.edge("A","r","run","r", via=[(880,210),(880,545)]); F.edge("Cc","r","run","r", via=[(880,320),(880,545)]); F.edge("B","r","run","r", via=[(880,430),(880,545)])
    F.edge("P","b","run","l", via=[(105,545)])
    F.edge("run","b","res","t"); F.edge("res","l","none","r","No"); F.edge("res","b","list","t","Yes")
    F.edge("list","b","e","t"); F.edge("none","b","e","l", via=[(100,822)])
    return export(F.S, "d2c_search", BUILD)

def d2d():
    F = Flow(920, 990); X = 410
    F.term("s", X, 34, "Start")
    F.proc("sel", X, 104, ["Select the property and the", "owner whose period changes"], w=260)
    F.proc("inp", X, 180, ["Enter the new share, price", "and start date"], w=260)
    F.dec("d1", X, 288, ["New start date after the", "current period's start?"], w=280, h=92)
    F.proc("e1", 760, 288, ["Show date error"], w=170, kind="err")
    F.dec("d2", X, 410, ["Total of the current shares", "still 100% or less?"], w=280, h=92)
    F.proc("e2", 760, 410, ["Show share error"], w=170, kind="err")
    F.proc("tx", X, 520, "Start a transaction")
    F.proc("close", X, 592, ["Close the current row:", "end date = start date - 1 day"], w=260)
    F.proc("ins", X, 668, ["Insert the new row", "with the new share"], w=230)
    F.dec("d3", X, 780, ["Database accepts both", "changes?"], w=260, h=90)
    F.proc("rb", 760, 780, ["Roll back and", "show error"], w=170, kind="err"); F.term("e2e", 760, 868, "End", w=90)
    F.proc("commit", X, 892, ["Commit and show", "confirmation"], w=200, kind="ok"); F.term("e", X, 958, "End")
    F.edge("s","b","sel","t"); F.edge("sel","b","inp","t"); F.edge("inp","b","d1","t")
    F.edge("d1","r","e1","l","No"); F.edge("e1","t","inp","r", via=[(760,180)]); F.edge("d1","b","d2","t","Yes")
    F.edge("d2","r","e2","l","No"); F.edge("e2","r","inp","r", via=[(880,410),(880,180)]); F.edge("d2","b","tx","t","Yes")
    F.edge("tx","b","close","t"); F.edge("close","b","ins","t"); F.edge("ins","b","d3","t")
    F.edge("d3","r","rb","l","No"); F.edge("rb","b","e2e","t"); F.edge("d3","b","commit","t","Yes"); F.edge("commit","b","e","t")
    return export(F.S, "d2d_change_ownership", BUILD)

# ======================= 3. class + ER =======================
def d3a():
    S = Svg(1150, 700)
    acc = classbox(S, 20, 50, 230, "Account", ["id: int", "email: String", "passwordHash: String", "role: Role"], color="green")
    role = classbox(S, 20, 222, 150, "Role", ["user", "clerk"], stereo="enumeration", color="grey")
    own = classbox(S, 350, 59, 170, "Owner", ["id: int"], color="amber")
    su = classbox(S, 790, 20, 250, "SingleUser", ["id: int", "cnp: String", "firstName: String", "lastName: String", "phone: String"], color="blue")
    co = classbox(S, 790, 175, 250, "Company", ["id: int", "taxId: String", "name: String"], color="blue")
    po = classbox(S, 350, 330, 240, "ParcelOwnership", ["id: int", "share: decimal", "price: decimal", "startDate: LocalDate", "endDate: LocalDate"], color="purple")
    par = classbox(S, 700, 330, 250, "Parcel", ["id: int", "cadastralNumber: String", "address: String", "sizeSqm: decimal"], color="blue")
    lu = classbox(S, 1005, 347, 130, "LandUse", ["id: int", "name: String"], color="grey")
    bo = classbox(S, 350, 520, 240, "BuildingOwnership", ["id: int", "share: decimal", "price: decimal", "startDate: LocalDate", "endDate: LocalDate"], color="purple")
    bld = classbox(S, 700, 520, 250, "Building", ["id: int", "cadastralNumber: String", "sizeSqm: decimal", "usableAreaSqm: decimal", "floors: int", "yearBuilt: int"], color="blue")
    bt = classbox(S, 1005, 554, 130, "BuildingType", ["id: int", "name: String"], color="grey")
    assoc(S, [acc.a("r", .35), own.a("l", .5)], "0..1", "0..1"); S.label(300, 80, "logs in", 11.5, "middle", MUTED, False, True)
    assoc(S, [(95, acc.y+acc.h), (95, role.y)], end="open", dash="5 4"); S.label(103, 205, "role", 11.5, "start", MUTED, False, True)
    y1 = own.a("r", .3)[1]; y2 = own.a("r", .8)[1]
    assoc(S, [own.a("r", .3), (700, y1), (700, su.a("l", .5)[1]), su.a("l", .5)], "1", "0..1")
    assoc(S, [own.a("r", .8), (700, y2), (700, co.a("l", .5)[1]), co.a("l", .5)], "1", "0..1")
    S.label(712, 135, "{exactly one", 11.5, "start", "#B42318", False, True); S.label(712, 150, "of the two}", 11.5, "start", "#B42318", False, True)
    S.label(612, y1-8, "represents", 11.5, "middle", MUTED, False, True)
    x = (own.x+own.w/2); assoc(S, [(x, own.y+own.h), (x, po.y)], "1", "*"); S.label(x+10, 215, "holds", 11.5, "start", MUTED, False, True)
    yo = own.a("l", .85)[1]
    assoc(S, [bo.a("l", .5), (320, bo.a("l", .5)[1]), (320, yo), (own.x, yo)], "*", "1"); S.label(312, 322, "holds", 11.5, "end", MUTED, False, True)
    ypar = par.cy; assoc(S, [po.a("r", (ypar-po.y)/po.h), (par.x, ypar)], "*", "1", name="of")
    ybld = bld.cy; assoc(S, [bo.a("r", (ybld-bo.y)/bo.h), (bld.x, ybld)], "*", "1", name="of")
    assoc(S, [par.a("b", .5), bld.a("t", .5)], "1", "*"); S.label(815, 480, "located on", 11.5, "end", MUTED, False, True)
    assoc(S, [par.a("r", .5), (lu.x, par.cy)], "*", "1")
    assoc(S, [bld.a("r", .5), (bt.x, bld.cy)], "*", "1")
    S.rect(20, 340, 280, 215, "#FFFBEB", "#B7791F", 1.2, 6, dash="5 3")
    for i, t in enumerate(["Ownership classes record who holds", "a parcel or a building, and when.", "", "share: percentage of the property", "price: paid for this owner's share", "endDate = null: current period", "", "Periods of one owner on one", "property never overlap."]):
        S.text(32, 364+i*19, t, 12, "start", False, INK, maxw=250)
    return export(S, "d3a_class_domain", BUILD)

def d3b():
    S = Svg(1050, 650); A, B, Cc = 30, 385, 740; W = 280; R1, R2, R3 = 20, 200, 380
    hand = classbox(S, A, R1, W, "ParcelHandler", ["-service: ParcelService"], ["+registerParcel(ctx)", "+getParcel(ctx)", "+searchParcels(ctx)"], color="green")
    serv = classbox(S, B, R1, W, "ParcelService", ["-repository: ParcelRepository"], ["+register(dto, account): Parcel", "+findById(id): Parcel", "+search(criteria): List<Parcel>"], color="green")
    repo = classbox(S, Cc, R1, W, "ParcelRepository", [], ["+save(p): Parcel", "+findById(id): Optional<Parcel>", "+existsByCadastralNumber(nr): boolean", "+search(criteria): List<Parcel>"], stereo="interface", color="green")
    dto = classbox(S, A, R2, W, "ParcelDto", ["+id: int", "+cadastralNumber: String", "+address: String", "+sizeSqm: decimal"], None, stereo="DTO", color="amber")
    par = classbox(S, B, R2, W, "Parcel", ["-id: int", "-cadastralNumber: String", "-address: String", "-sizeSqm: decimal"], ["+builder(): ParcelBuilder"], color="blue")
    jdbc = classbox(S, Cc, R2, W, "JdbcParcelRepository", ["-pool: ConnectionPool"], ["+save(p): Parcel", "+findById(id)", "+existsByCadastralNumber(nr)", "+search(criteria)"], color="green")
    fac = classbox(S, A, R3, 296, "RepositoryFactory", [], ["+createParcelRepository(): ParcelRepository", "+createOwnerRepository(): OwnerRepository", "+createAccountRepository(): AccountRepository"], stereo="Factory", color="amber")
    bld = classbox(S, B, R3, W, "ParcelBuilder", ["-cadastralNumber: String", "-address: String", "-sizeSqm: decimal"], ["+cadastralNumber(nr): ParcelBuilder", "+address(a): ParcelBuilder", "+sizeSqm(s): ParcelBuilder", "+build(): Parcel"], stereo="Builder", color="amber")
    pool = classbox(S, Cc, R3, W, "ConnectionPool", ["-instance: ConnectionPool {static}", "-dataSource: HikariDataSource"], ["+getInstance(): ConnectionPool", "+getConnection(): Connection"], stereo="Singleton", color="amber")
    yh = R1 + 60
    S.poly([(hand.x+hand.w, yh), (serv.x, yh)], end="arrow"); S.label(352, yh-7, "calls", 11.5, "middle", MUTED, False, True)
    S.poly([(serv.x+serv.w, yh), (repo.x, yh)], end="arrow"); S.label(702, yh-7, "depends on", 11.5, "middle", MUTED, False, True)
    S.poly([hand.a("b"), dto.a("t")], end="open", dash="5 4"); S.label(hand.cx+8, 178, "«uses»", 11.5, "start", MUTED, False, True)
    S.poly([serv.a("b"), par.a("t")], end="open", dash="5 4"); S.label(serv.cx+8, 178, "«uses»", 11.5, "start", MUTED, False, True)
    S.poly([jdbc.a("t"), repo.a("b")], end="tri", dash="6 4"); S.label(jdbc.cx+8, 188, "implements", 11.5, "start", MUTED, False, True)
    S.poly([jdbc.a("b"), pool.a("t")], end="arrow"); S.label(pool.cx+8, 360, "getConnection()", 11.5, "start", MUTED, False, True)
    yj = jdbc.a("l", .3)[1]; S.poly([jdbc.a("l", .3), (par.x+par.w, yj)], end="open", dash="5 4"); S.label(700, yj-7, "«uses»", 11.5, "middle", MUTED, False, True)
    S.poly([bld.a("t"), par.a("b")], end="open", dash="5 4"); S.label(bld.cx+8, 372, "«creates»", 11.5, "start", MUTED, False, True)
    yb = R3 + 205; yj2 = jdbc.a("l", .8)[1]
    S.poly([fac.a("b"), (fac.cx, yb), (700, yb), (700, yj2), jdbc.a("l", .8)], end="open", dash="5 4"); S.label(fac.cx+10, yb-7, "«creates»", 11.5, "start", MUTED, False, True)
    S.text(30, 604, "Same structure for Building, Owner and Account.", 12, "start", False, MUTED, True)
    lx = 30
    for col, lab in (("green", "Layer classes"), ("blue", "Domain entity"), ("amber", "Design pattern")):
        S.rect(lx, 613, 14, 14, HDR[col], EDG[col], 1.4, 2); S.text(lx+20, 624, lab, 11.5, "start", False, INK); lx += 150
    return export(S, "d3b_class_patterns", BUILD)

def d3c():
    S = Svg(1300, 755)
    T = {
     "account": [("PK","id","integer"),("UQ","email","varchar(255)"),("","password_hash","varchar(60)"),("","role","role (user, clerk)"),("FK UQ","owner_id","integer, NULL")],
     "owner": [("PK","id","integer"),("FK UQ","single_user_id","integer, NULL"),("FK UQ","company_id","integer, NULL")],
     "single_user": [("PK","id","integer"),("UQ","cnp","varchar(13)"),("","first_name","varchar(50)"),("","last_name","varchar(50)"),("","phone","varchar(20), NULL")],
     "company": [("PK","id","integer"),("UQ","tax_id","varchar(50)"),("","name","varchar(50)")],
     "parcel": [("PK","id","integer"),("UQ","cadastral_number","varchar(50)"),("","address","varchar(50)"),("","size_sqm","numeric(10,2)"),("FK","land_use_id","integer")],
     "land_use": [("PK","id","integer"),("UQ","name","varchar(60)")],
     "building": [("PK","id","integer"),("UQ","cadastral_number","varchar(50)"),("FK","parcel_id","integer"),("FK","building_type_id","integer"),("","size_sqm","numeric(10,2)"),("","usable_area_sqm","numeric(10,2)"),("","floors","smallint"),("","year_built","smallint")],
     "building_type": [("PK","id","integer"),("UQ","name","varchar(255)")],
     "parcel_ownership": [("PK","id","integer"),("FK","owner_id","integer"),("FK","parcel_id","integer"),("","share","numeric(5,2)"),("","price","numeric(14,2)"),("","start_date","date"),("","end_date","date, NULL")],
     "building_ownership": [("PK","id","integer"),("FK","owner_id","integer"),("FK","building_id","integer"),("","share","numeric(5,2)"),("","price","numeric(14,2)"),("","start_date","date"),("","end_date","date, NULL")],
    }
    acc = tablebox(S, 20, 30, 290, "account", T["account"], "green")
    own = tablebox(S, 380, 49, 270, "owner", T["owner"], "amber")
    su = tablebox(S, 730, 20, 290, "single_user", T["single_user"], "blue")
    co = tablebox(S, 730, 180, 290, "company", T["company"], "blue")
    po = tablebox(S, 380, 330, 290, "parcel_ownership", T["parcel_ownership"], "purple")
    par = tablebox(S, 740, 340, 280, "parcel", T["parcel"], "blue")
    lu = tablebox(S, 1080, 370, 200, "land_use", T["land_use"], "grey")
    bo = tablebox(S, 380, 560, 290, "building_ownership", T["building_ownership"], "purple")
    bld = tablebox(S, 740, 550, 280, "building", T["building"], "blue")
    bt = tablebox(S, 1080, 600, 200, "building_type", T["building_type"], "grey")
    assoc(S, [acc.a("r", .5), own.a("l", .5)], "0..1", "0..1")
    y1 = own.a("r", .35)[1]; y2 = own.a("r", .75)[1]
    assoc(S, [own.a("r", .35), (690, y1), (690, su.a("l", .5)[1]), su.a("l", .5)], "0..1", "0..1")
    assoc(S, [own.a("r", .75), (690, y2), (690, co.a("l", .5)[1]), co.a("l", .5)], "0..1", "0..1")
    S.label(686, 176, "{exactly one}", 11.5, "end", "#B42318", False, True)
    x = own.cx; xp = x if po.x <= x <= po.x+po.w else po.cx
    assoc(S, [(x, own.y+own.h), (x, po.y)], "1", "*")
    yo = own.a("l", .85)[1]
    assoc(S, [bo.a("l", .5), (340, bo.a("l", .5)[1]), (340, yo), (own.x, yo)], "*", "1")
    assoc(S, [po.a("r", (par.cy-po.y)/po.h), (par.x, par.cy)], "*", "1")
    assoc(S, [bo.a("r", (bld.cy-bo.y)/bo.h), (bld.x, bld.cy)], "*", "1")
    assoc(S, [par.a("b", .5), bld.a("t", .5)], "1", "*")
    assoc(S, [par.a("r", (lu.cy-par.y)/par.h), (lu.x, lu.cy)], "*", "1")
    assoc(S, [bld.a("r", (bt.cy-bld.y)/bld.h), (bt.x, bt.cy)], "*", "1")
    S.rect(20, 215, 310, 250, "#FFFBEB", "#B7791F", 1.2, 6, dash="5 3")
    S.text(32, 238, "Rules enforced by the database", 12.5, "start", True, INK)
    rules = ["owner: a person or a company, never both", "account.owner_id: one login per owner", "share: more than 0, up to 100", "end_date is not before start_date", "same owner and property: periods never", "   overlap (exclusion constraint)", "building: usable area <= size, floors >= 1", "deleting an owner or a property with", "   history is refused (RESTRICT)"]
    for i, t in enumerate(rules): S.text(32, 262+i*21, t, 11.5, "start", False, INK, maxw=280)
    S.rect(20, 500, 310, 118, "#FFFFFF", "#9CA3AF", 1.2, 6)
    S.text(32, 522, "Legend", 12, "start", True, INK)
    for i, (b, t) in enumerate([("PK", "primary key"), ("FK", "foreign key"), ("UQ", "unique"), ("NULL", "the value may be empty")]):
        S.text(32, 545+i*19, b, 10.5, "start", True, EDG["blue"]); S.text(76, 545+i*19, t, 11.5, "start", False, INK)
    S.text(20, 645, "Line ends: 1 = exactly one, * = many, 0..1 = at most one.", 11.5, "start", False, MUTED, True)
    return export(S, "d3c_database_er", BUILD)

# ======================= 4. object diagram =======================
def d4():
    S = Svg(1090, 700); C1, C2, C3, C4 = 20, 270, 540, 830
    acc1 = objbox(S, C1, 30, 200, "acc1", "Account", ['id = 1', 'email = "ion@example.com"', 'role = user'], "green")
    clerk = objbox(S, C1, 200, 200, "clerk1", "Account", ['id = 2', 'email = "clerk@example.com"', 'role = clerk'], "green")
    o1 = objbox(S, C2, 47, 200, "owner1", "Owner", ['id = 1'], "amber")
    ion = objbox(S, C2, 170, 200, "ion", "SingleUser", ['id = 1', 'cnp = "1900101000001"', 'firstName = "Ion"', 'lastName = "Popescu"', 'phone = "0700 000 001"'], "blue")
    o2 = objbox(S, C2, 400, 200, "owner2", "Owner", ['id = 2'], "amber")
    dl = objbox(S, C2, 530, 200, "delta", "Company", ['id = 1', 'taxId = "RO1234567"', 'name = "Delta Build SRL"'], "blue")
    po1 = objbox(S, C3, 20, 230, "po1", "ParcelOwnership", ['share = 100', 'price = 40000', 'startDate = 2019-05-10', 'endDate = 2024-02-29'], "purple")
    po2 = objbox(S, C3, 150, 230, "po2", "ParcelOwnership", ['share = 40', 'price = 16000', 'startDate = 2024-03-01', 'endDate = null'], "purple")
    po3 = objbox(S, C3, 280, 230, "po3", "ParcelOwnership", ['share = 60', 'price = 39000', 'startDate = 2024-03-01', 'endDate = null'], "purple")
    bo1 = objbox(S, C3, 520, 230, "bo1", "BuildingOwnership", ['share = 100', 'price = 120000', 'startDate = 2024-03-01', 'endDate = null'], "purple")
    lu = objbox(S, C4, 20, 230, "land1", "LandUse", ['id = 1', 'name = "Residential"'], "grey")
    p1 = objbox(S, C4, 130, 230, "parcel1", "Parcel", ['id = 1', 'cadastralNumber = "100234"', 'address = "Str. Florilor 5"', 'sizeSqm = 450.00'], "blue")
    b1 = objbox(S, C4, 390, 230, "building1", "Building", ['id = 1', 'cadastralNumber = "100234-C1"', 'sizeSqm = 120.00', 'usableAreaSqm = 95.00', 'floors = 2', 'yearBuilt = 2008'], "blue")
    bt = objbox(S, C4, 580, 230, "type1", "BuildingType", ['id = 1', 'name = "House"'], "grey")
    L = lambda pts: S.poly(pts)
    L([acc1.a("r"), o1.a("l")]); S.label(253, acc1.cy-8, "account", 11.5, "middle", MUTED, False, True)
    L([o1.a("b"), ion.a("t")]); S.label(378, 150, "identity", 11.5, "start", MUTED, False, True)
    L([o2.a("b"), dl.a("t")]); S.label(378, 508, "identity", 11.5, "start", MUTED, False, True)
    ya = o1.y + o1.h*0.3; yb = o1.y + o1.h*0.8
    L([(o1.x+o1.w, ya), (505, ya), (505, po1.cy), po1.a("l")]); L([(o1.x+o1.w, yb), (515, yb), (515, po2.cy), po2.a("l")])
    S.label(512, ya-9, "holder", 11.5, "middle", MUTED, False, True)
    yc = o2.y + o2.h*0.3; yd = o2.y + o2.h*0.8
    L([(o2.x+o2.w, yc), (505, yc), (505, po3.cy), po3.a("l")]); L([(o2.x+o2.w, yd), (515, yd), (515, bo1.cy), bo1.a("l")])
    for po, f in ((po1, .22), (po2, .5), (po3, .85)):
        yy = p1.y + p1.h*f; L([po.a("r"), (800, po.cy), (800, yy), (p1.x, yy)])
    S.label(808, 120, "parcel", 11.5, "start", MUTED, False, True)
    L([bo1.a("r"), (800, bo1.cy), (800, b1.y+b1.h*0.4), (b1.x, b1.y+b1.h*0.4)]); S.label(800, bo1.cy+22, "building", 11.5, "middle", MUTED, False, True)
    L([lu.a("b"), p1.a("t")]); S.label(C4+112, 108, "land use", 11.5, "start", MUTED, False, True)
    L([p1.a("b"), b1.a("t")]); S.label(C4+112, 358, "located on", 11.5, "start", MUTED, False, True)
    L([b1.a("b"), bt.a("t")]); S.label(C4+112, 560, "type", 11.5, "start", MUTED, False, True)
    S.label(C1+100, 312, "(no owner linked)", 11.5, "middle", MUTED, False, True)
    S.rect(20, 380, 235, 290, "#FFFBEB", "#B7791F", 1.2, 6, dash="5 3")
    for i, t in enumerate(["Scenario", "Ion Popescu owned 100% of", "parcel 100234 until 2024-02-29.", "From 2024-03-01 Delta Build SRL", "holds 60% and Ion keeps 40%:", "two co-owners, 100% in total.", "Delta Build SRL also owns the", "house 100234-C1.", "", "endDate = null: current period."]):
        S.text(32, 404+i*19.5, t, 12, "start", i == 0, INK, maxw=215)
    return export(S, "d4_object", BUILD)

# ======================= 5. sequence diagrams =======================
M = lambda num, f, t, label, kind="sync": dict(num=num, f=f, t=t, label=label, kind=kind)
def d5a():
    parts = [("User\n(clerk / owner)", "actor"), ("Angular UI", "ui"), ("AuthHandler", "handler"), ("AuthService", "service"), ("Account\nRepository", "repo"), ("PostgreSQL", "db")]
    m = [M(1,0,1,"enter email + password"), M(2,1,2,"POST /api/login"), M(3,2,3,"login(email, password)"), M(4,3,4,"findByEmail(email)"), M(5,4,5,"SELECT FROM account"), M(6,5,4,"account row","ret"), M(7,4,3,"Account","ret"), M(8,3,3,"verify BCrypt hash","self"),
         M(9,3,2,"token + role","ret"), M(10,2,1,"200 OK (JSON)","ret"), M(11,1,0,"open home page","ret"), M(12,3,2,"AuthException","ret"), M(13,2,1,"401 Unauthorized","ret"), M(14,1,0,"show error message","ret")]
    fr = [dict(kind="alt", start=8, end=13, cond="credentials are valid", else_at=11, else_cond="wrong email or password", x1=0, x2=3)]
    return export(sequence(parts, m, fr), "d5a_seq_login", BUILD)
def d5b():
    parts = [("Clerk", "actor"), ("Angular UI", "ui"), ("ParcelHandler", "handler"), ("ParcelService", "service"), ("Parcel\nRepository", "repo"), ("PostgreSQL", "db")]
    m = [M(1,0,1,"submit parcel form"), M(2,1,2,"POST /api/parcels"), M(3,2,3,"register(dto, account)"), M(4,3,3,"check role = clerk, validate","self"), M(5,3,4,"existsByCadastralNumber"), M(6,4,5,"SELECT count(*)"), M(7,5,4,"count","ret"), M(8,4,3,"exists = true / false","ret"),
         M(9,3,4,"save(parcel)"), M(10,4,5,"INSERT INTO parcel"), M(11,5,4,"generated id","ret"), M(12,4,3,"Parcel","ret"), M(13,3,2,"Parcel","ret"), M(14,2,1,"201 Created","ret"), M(15,1,0,"show confirmation","ret"),
         M(16,3,2,"DuplicateException","ret"), M(17,2,1,"409 Conflict","ret"), M(18,1,0,"show error message","ret")]
    fr = [dict(kind="alt", start=8, end=17, cond="number is new", else_at=15, else_cond="number already registered", x1=0, x2=5)]
    return export(sequence(parts, m, fr), "d5b_seq_register_parcel", BUILD)
def d5c():
    parts = [("Owner", "actor"), ("Angular UI", "ui"), ("ParcelHandler", "handler"), ("ParcelService", "service"), ("Ownership\nRepository", "repo"), ("PostgreSQL", "db")]
    m = [M(1,0,1,"open ownership history"), M(2,1,2,"GET .../{id}/ownership"), M(3,2,3,"getHistory(id, account)"), M(4,3,3,"load the owner of the account","self"), M(5,3,4,"findByParcelId(id)"), M(6,4,5,"SELECT history rows"), M(7,5,4,"rows","ret"), M(8,4,3,"List<ParcelOwnership>","ret"),
         M(9,3,3,"check the parcel belongs to the owner","self"), M(10,3,2,"List<OwnershipDto>","ret"), M(11,2,1,"200 OK (JSON)","ret"), M(12,1,0,"show history by date","ret"), M(13,3,2,"AccessDenied","ret"), M(14,2,1,"403 Forbidden","ret"), M(15,1,0,"show error message","ret")]
    fr = [dict(kind="alt", start=9, end=14, cond="parcel belongs to this owner", else_at=12, else_cond="parcel belongs to someone else", x1=0, x2=3)]
    return export(sequence(parts, m, fr), "d5c_seq_ownership_history", BUILD)
def d5d():
    parts = [("Clerk", "actor"), ("Angular UI", "ui"), ("OwnershipHandler", "handler"), ("OwnershipService", "service"), ("Ownership\nRepository", "repo"), ("PostgreSQL", "db")]
    m = [M(1,0,1,"submit new share"), M(2,1,2,"POST /api/ownership"), M(3,2,3,"changeShare(request)"), M(4,3,3,"check role, dates, shares","self"),
         M(5,3,4,"closeCurrent(period)"), M(6,4,5,"UPDATE end_date"), M(7,5,4,"1 row updated","ret"), M(8,3,4,"insertNew(request)"), M(9,4,5,"INSERT new row"),
         M(10,3,4,"commit"), M(11,4,5,"COMMIT"), M(12,3,2,"OwnershipDto","ret"), M(13,2,1,"200 OK (JSON)","ret"), M(14,1,0,"show confirmation","ret"),
         M(15,3,4,"rollback"), M(16,4,5,"ROLLBACK"), M(17,3,2,"ConflictException","ret"), M(18,2,1,"409 Conflict","ret"), M(19,1,0,"show error message","ret")]
    fr = [dict(kind="alt", start=9, end=18, cond="both statements accepted", else_at=14, else_cond="rule violated: overlap or dates", x1=0, x2=5)]
    return export(sequence(parts, m, fr), "d5d_seq_change_ownership", BUILD)

if __name__ == "__main__":
    for f in (d1, d2a, d2b, d2c, d2d, d3a, d3b, d3c, d4, d5a, d5b, d5c, d5d):
        print(os.path.basename(f()))
