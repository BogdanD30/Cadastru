"""Extra diagrams for the Analysis & Design document: use cases, activity, state, package, component, communication, UI mock-ups."""
import os
from lib import *
BUILD = os.environ.get("BUILD", "/private/tmp/claude-501/-Users-dindiliganbogdan-Project-Cadastru/83778627-cef0-4add-bc92-88247cfbe8f3/scratchpad/build")

# ---------------------------------------------------------------- use cases
def stick(S, x, y, label):
    S.add(f'<circle cx="{x}" cy="{y-34}" r="13" fill="#FFF4DC" stroke="{LINE}" stroke-width="1.6"/>')
    S.line(x, y-21, x, y+14, LINE, 1.6); S.line(x-24, y-10, x+24, y-10, LINE, 1.6); S.line(x, y+14, x-18, y+42, LINE, 1.6); S.line(x, y+14, x+18, y+42, LINE, 1.6)
    S.text(x, y+62, label, 13, "middle", True, INK)

def usecase_diagram(name, actor, ucs, sub=None):
    n = len(ucs); pitch = 56; top = 70; H = top + n*pitch + 30
    S = Svg(600, H)
    S.rect(215, 14, 375, H-28, "#FFFFFF", C["nav"], 1.6, 6); S.text(402, 40, "Cadastru", 14, "middle", True, C["nav"])
    ys = [top + i*pitch + 6 for i in range(n)]
    yc = (ys[0] + ys[-1]) / 2
    for y in ys:
        S.line(95, yc-8, 245, y, LINE, 1.3)
    for u, y in zip(ucs, ys):
        S.add(f'<ellipse cx="402" cy="{y}" rx="158" ry="21" fill="#EAF1FB" stroke="{C["proc_s"]}" stroke-width="1.5"/>')
        S.text(402, y+4.5, u, 12.5, "middle", False, INK, maxw=290)
    stick(S, 62, yc, actor)
    if sub: S.text(62, yc+80, sub, 11, "middle", False, MUTED, True)
    return export(S, name, BUILD)

def usecases():
    usecase_diagram("uc_visitor", "Visitor", ["Search parcels and buildings (public view)", "Register account", "Log in"])
    usecase_diagram("uc_owner", "Owner", ["Log in", "Log out", "Search register (own details)", "View my properties", "View property details", "View ownership history"], "(account linked to an owner)")
    usecase_diagram("uc_clerk", "Clerk", ["Log in", "Log out", "Register parcel", "Edit parcel", "Register building", "Edit building", "Manage owner", "Link account to owner", "Assign / change ownership", "Search register", "View ownership history"])

# ---------------------------------------------------------------- activity (swimlanes)
def activity():
    S = Svg(920, 890); lanes = [("Visitor / user", 10, 150), ("Clerk", 310, 460), ("System", 610, 770)]
    for t, x, cx in lanes:
        S.rect(x, 10, 300, 860, "#FFFFFF", "#9CA3AF", 1.3, 0); S.rect(x, 10, 300, 34, "#E5E7EB", "#9CA3AF", 1.3, 0); S.text(x+150, 33, t, 13.5, "middle", True, INK)
    nodes = {}
    def act(k, cx, cy, lines, kind="proc", w=230):
        h = max(46, 18*len(lines)+16); sh = Shape(cx-w/2, cy-h/2, w, h); nodes[k] = sh
        f, st = {"proc": (C["proc_f"], C["proc_s"]), "ok": (C["ok_f"], C["ok_s"]), "err": (C["err_f"], C["err_s"])}[kind]
        S.rect(sh.x, sh.y, w, h, f, st, 1.5, 14); S.lines(cx, cy, lines, 12.5, False, INK, maxw=w-12)
    def dec(k, cx, cy, lines, w=200, h=80):
        sh = Shape(cx-w/2, cy-h/2, w, h, "diamond"); nodes[k] = sh; S.diamond(sh, C["dec_f"], C["dec_s"]); S.lines(cx, cy, lines, 12, False, INK, maxw=w*0.6)
    def dot(k, cx, cy, final=False):
        sh = Shape(cx-11, cy-11, 22, 22); nodes[k] = sh
        if final:
            S.add(f'<circle cx="{cx}" cy="{cy}" r="12" fill="#FFFFFF" stroke="{LINE}" stroke-width="1.6"/><circle cx="{cx}" cy="{cy}" r="7" fill="{LINE}"/>')
        else: S.add(f'<circle cx="{cx}" cy="{cy}" r="10" fill="{LINE}"/>')
    def e(a, sa, b, sb, label=None, via=None):
        p, q = nodes[a].a(sa), nodes[b].a(sb); pts = [p] + (via or []) + [q] if via else route(p, q, sa, sb)
        S.poly(pts, end="arrow")
        if label: S.label(p[0]+8, p[1]-7 if sa in "lr" else p[1]+18, label, 12, "start", INK, True)
    dot("s", 150, 80); act("a1", 150, 150, ["Register an account", "(email, password)"])
    act("a2", 770, 150, ["Create the account", "(role user, no owner)"])
    act("a3", 150, 265, ["Visit the clerk with an ID", "and the documents"])
    act("a4", 460, 340, ["Check identity", "and documents"])
    dec("d1", 460, 450, ["Documents", "valid?"], 190, 84)
    act("rej", 150, 450, ["Request rejected"], "err", 200)
    dot("e1", 150, 540, True)
    act("a5", 460, 560, ["Create or find the owner", "record (person or company)"])
    act("a6", 460, 650, ["Link the account", "to the owner"])
    act("a7", 770, 650, ["Save the link", "(account.owner_id)"])
    act("a8", 150, 770, ["Log in again and see", "own properties"], "ok")
    dot("e2", 150, 850, True)
    e("s","b","a1","t"); e("a1","r","a2","l"); e("a2","b","a3","r"); e("a3","b","a4","l"); e("a4","b","d1","t")
    e("d1","l","rej","r","No"); e("rej","b","e1","t"); e("d1","b","a5","t","Yes"); e("a5","b","a6","t"); e("a6","r","a7","l"); e("a7","b","a8","r"); e("a8","b","e2","t")
    return export(S, "act_become_owner", BUILD)

# ---------------------------------------------------------------- state diagrams
def state_box(S, x, y, w, h, title, sub=None, fill="#EAF1FB", stroke=None):
    S.rect(x, y, w, h, fill, stroke or C["proc_s"], 1.6, 18)
    if sub: S.text(x+w/2, y+h/2-4, title, 13, "middle", True, INK, maxw=w-12); S.text(x+w/2, y+h/2+14, sub, 11, "middle", False, MUTED, maxw=w-12)
    else: S.text(x+w/2, y+h/2+4.5, title, 13, "middle", True, INK, maxw=w-12)
    return Shape(x, y, w, h)

def states():
    S = Svg(1050, 560)
    S.rect(10, 10, 500, 540, "none", "#9CA3AF", 1.3, 8); S.text(30, 34, "Account", 14, "start", True, C["nav"])
    S.rect(540, 10, 500, 540, "none", "#9CA3AF", 1.3, 8); S.text(560, 34, "Ownership period (a row in parcel_ownership / building_ownership)", 13, "start", True, C["nav"], maxw=470)
    # account machine
    S.add(f'<circle cx="90" cy="110" r="10" fill="{LINE}"/>')
    reg = state_box(S, 40, 200, 220, 64, "Registered", "role user, no owner link")
    lnk = state_box(S, 270, 340, 220, 64, "Linked to an owner", "role user, owner_id set", "#E7F5EC", C["ok_s"])
    clk = state_box(S, 300, 90, 180, 64, "Clerk", "role clerk", "#FFF4DC", C["act_s"])
    S.poly([(90, 120), (90, 200)], end="arrow"); S.label(100, 168, "register (public form)", 11.5, "start", INK, False, True)
    S.poly([reg.a("r", .7), (380, reg.a("r", .7)[1]), lnk.a("t", .5)], end="arrow"); S.label(272, 232, "clerk links the account", 11.5, "start", INK, False, True)
    S.poly([lnk.a("l", .5), (150, lnk.a("l", .5)[1]), reg.a("b", .5)], end="arrow"); S.label(60, 405, "owner deleted or clerk unlinks", 11.5, "start", INK, False, True)
    S.add(f'<circle cx="390" cy="60" r="10" fill="{LINE}"/>'); S.poly([(390, 70), (390, 90)], end="arrow"); S.label(402, 82, "", 11)
    S.text(30, 520, "A clerk account is created only in the database, never through the public registration.", 11.5, "start", False, MUTED, True)
    # ownership machine
    S.add(f'<circle cx="640" cy="110" r="10" fill="{LINE}"/>')
    cur = state_box(S, 600, 200, 260, 70, "Current", "end_date is empty", "#E7F5EC", C["ok_s"])
    end = state_box(S, 600, 380, 260, 70, "Ended", "end_date = last day owned", "#EAF1FB")
    S.add(f'<circle cx="730" cy="505" r="13" fill="#FFFFFF" stroke="{LINE}" stroke-width="1.6"/><circle cx="730" cy="505" r="7.5" fill="{LINE}"/>')
    S.poly([(640, 120), (640, 200)], end="arrow"); S.label(652, 166, "clerk assigns ownership", 11.5, "start", INK, False, True)
    S.poly([cur.a("b"), end.a("t")], end="arrow"); S.label(744, 322, "owner or share changes:", 11.5, "start", INK, False, True); S.label(744, 338, "end_date = new start - 1 day", 11.5, "start", INK, False, True)
    S.poly([end.a("b"), (730, 492)], end="arrow")
    S.text(560, 532, "Ended rows are kept as history and are never deleted.", 11.5, "start", False, MUTED, True)
    S.text(884, 235, "overlap or invalid dates:", 11, "start", False, "#B42318", True); S.text(884, 250, "change refused", 11, "start", False, "#B42318", True)
    return export(S, "state_account_ownership", BUILD)

# ---------------------------------------------------------------- package diagram
def pkg(S, x, y, w, h, name, fill="#FFFFFF", stroke=C["proc_s"], items=None):
    S.rect(x, y+16, w, h-16, fill, stroke, 1.6, 2); S.rect(x, y, min(w*0.5, 130), 18, fill, stroke, 1.6, 2)
    S.text(x+8, y+13.5, name, 11.5, "start", True, INK, maxw=min(w*0.5, 130)-8)
    for i, t in enumerate(items or []): S.text(x+10, y+38+i*16, t, 11, "start", False, INK, maxw=w-16)
    return Shape(x, y, w, h)

def packages():
    S = Svg(1100, 600)
    S.rect(10, 10, 280, 580, "#F4F8FD", C["fe_s"], 1.6, 4); S.text(24, 34, "Angular application (frontend)", 12.5, "start", True, C["nav"])
    fe = {}
    for i, (n, it) in enumerate([("core", ["auth, http client, guards"]), ("shared", ["table, form, models"]), ("public", ["search page"]), ("owner", ["my properties, history"]), ("clerk", ["parcels, buildings,", "owners, ownership"])]):
        fe[n] = pkg(S, 30, 56+i*104, 240, 84, n, items=it)
    S.text(150, 574, "feature modules use core and shared", 11, "middle", False, MUTED, True)
    S.rect(330, 10, 760, 580, "#F3FAF5", C["be_s"], 1.6, 4); S.text(344, 34, "ro.cadastru (backend)", 12.5, "start", True, "#14532D")
    A, B, Cc = 370, 640, 890; W = 190; R1, R2, R3 = 70, 250, 430
    h = pkg(S, A, R1, W, 96, "handler", items=["Javalin routes, filters", "request / response"])
    ser = pkg(S, B, R1, W, 96, "service", items=["business rules,", "role checks, transactions"])
    rep = pkg(S, Cc, R1, 180, 96, "repository", items=["interfaces", "+ jdbc implementations"])
    dto = pkg(S, A, R2, W, 86, "dto", items=["ParcelDto, OwnerDto ...", "(API objects)"])
    mod = pkg(S, B, R2, W, 86, "model", items=["Parcel, Building, Owner,", "Account, ownership"])
    utl = pkg(S, A, R3, W, 86, "util", items=["validators, helpers", "(CNP, dates)"])
    exc = pkg(S, B, R3, W, 86, "exception", items=["custom exceptions"])
    cfg = pkg(S, Cc, R3, 180, 86, "config", items=["ConnectionPool", "settings"])
    dep = lambda pts: S.poly(pts, end="open", dash="6 4")
    ym = R1 + 56
    dep([(A+W, ym), (B, ym)]); S.label(A+W+40, ym-7, "uses", 11, "middle", MUTED, False, True)
    dep([(B+W, ym), (Cc, ym)]); S.label(B+W+30, ym-7, "uses", 11, "middle", MUTED, False, True)
    dep([(A+W/2, R1+96), (A+W/2, R2)])                       # handler -> dto
    dep([(B+W/2, R1+96), (B+W/2, R2)])                       # service -> model
    dep([(Cc+30, R1+96), (Cc+30, R2+43), (B+W, R2+43)])      # repository -> model
    dep([(Cc+150, R1+96), (Cc+150, R3)])                     # repository -> config
    ch = 605
    dep([(B, R1+80), (ch, R1+80), (ch, R3+43), (B, R3+43)])  # service -> exception
    dep([(ch, R3+43), (A+W, R3+43)])                         # service -> util
    # frontend -> backend
    S.poly([(270, ym), (A, ym)], end="open", dash="6 4"); S.text(300, ym-10, "REST", 11.5, "middle", True, C["nav"])
    return export(S, "pkg_packages", BUILD)

# ---------------------------------------------------------------- component diagram
def comp(S, x, y, w, h, name, sub=None, fill="#FFFFFF", stroke=C["proc_s"]):
    S.rect(x, y, w, h, fill, stroke, 1.7, 4)
    S.rect(x-9, y+12, 18, 8, fill, stroke, 1.4, 1); S.rect(x-9, y+26, 18, 8, fill, stroke, 1.4, 1)
    S.text(x+w/2, y+h/2-(2 if sub else -4), name, 13, "middle", True, INK, maxw=w-30)
    if sub: S.text(x+w/2, y+h/2+15, sub, 11, "middle", False, MUTED, maxw=w-20)
    return Shape(x, y, w, h)

def lollipop(S, x, y, label, left=True):
    S.add(f'<circle cx="{x}" cy="{y}" r="8" fill="#FFFFFF" stroke="{LINE}" stroke-width="1.5"/>')
    S.text(x, y-14, label, 11.5, "middle", True, C["nav"], halo=True)

def components():
    S = Svg(1100, 440)
    S.rect(20, 40, 210, 370, "#F4F8FD", C["fe_s"], 1.5, 6); S.text(125, 62, "Browser", 12.5, "middle", True, C["fe_s"])
    spa = comp(S, 50, 110, 150, 90, "Angular SPA", "pages, services")
    S.rect(260, 40, 560, 370, "#F3FAF5", C["be_s"], 1.5, 6); S.text(540, 62, "Java 21 application (Javalin)", 12.5, "middle", True, "#14532D")
    hnd = comp(S, 300, 110, 140, 90, "Handlers", "REST routes")
    srv = comp(S, 480, 110, 140, 90, "Services", "business rules")
    rep = comp(S, 660, 110, 140, 90, "Repositories", "JDBC")
    aut = comp(S, 300, 270, 140, 90, "Security", "BCrypt, roles")
    val = comp(S, 480, 270, 140, 90, "Validation", "CNP, dates, shares")
    pol = comp(S, 660, 270, 140, 90, "Connection pool", "HikariCP")
    S.rect(860, 40, 220, 370, "#F8F2FC", C["db_s"], 1.5, 6); S.text(970, 62, "Docker (docker-compose)", 12.5, "middle", True, C["db_s"])
    db = comp(S, 890, 110, 160, 90, "PostgreSQL 17", "container cadastru-db", stroke=C["db_s"])
    pga = comp(S, 890, 270, 160, 90, "pgAdmin", "browser DB tool", stroke=C["db_s"])
    S.poly([(200, 155), (300, 155)], end="arrow2", start="arrow2"); lollipop(S, 250, 155, "REST / JSON")
    S.poly([hnd.a("r"), srv.a("l")], end="arrow"); S.poly([srv.a("r"), rep.a("l")], end="arrow")
    S.poly([hnd.a("b"), aut.a("t")], end="arrow"); S.poly([srv.a("b"), val.a("t")], end="arrow"); S.poly([rep.a("b"), pol.a("t")], end="arrow")
    S.poly([(srv.x+20, srv.y+srv.h), (srv.x+20, 232), (aut.x+aut.w-20, 232), (aut.x+aut.w-20, aut.y)], end="arrow")
    S.poly([pol.a("r"), (840, pol.cy), (840, db.cy), db.a("l")], end="arrow2", start="arrow2"); lollipop(S, 840, 215, "JDBC")
    S.poly([pga.a("t"), db.a("b")], end="arrow2", start="arrow2"); S.label(978, 244, "SQL", 11.5, "start", C["db_s"], True)
    S.text(540, 430, "Services call Security (login, roles) and Validation, then the repositories.", 11.5, "middle", False, MUTED, True)
    return export(S, "cmp_components", BUILD)

# ---------------------------------------------------------------- communication diagram
def communication():
    S = Svg(1120, 380); S.add('<g transform="translate(0,-150)">')
    def obj(x, y, w, label, kind="be"):
        f, st = (C["act_f"], C["act_s"]) if kind == "act" else (C[f"{kind}_f"], C[f"{kind}_s"])
        S.rect(x, y, w, 44, f, st, 1.6, 4); S.text(x+w/2, y+27, label, 12.5, "middle", True, INK, under=True, maxw=w-8); return Shape(x, y, w, 44)
    clerk = obj(20, 200, 130, "clerk : Clerk", "act"); ui = obj(240, 200, 150, ":Angular UI", "fe")
    hnd = obj(480, 200, 170, ":ParcelHandler"); srv = obj(740, 200, 170, ":ParcelService")
    rep = obj(740, 400, 170, ":ParcelRepository"); db = obj(1000, 400, 90, ":PostgreSQL", "db")
    ly = 222
    for a, b in [(clerk, ui), (ui, hnd), (hnd, srv)]: S.line(a.x+a.w, ly, b.x, ly, "#9CA3AF", 2)
    S.line(825, 244, 825, 400, "#9CA3AF", 2); S.line(910, 422, 1000, 422, "#9CA3AF", 2)
    def fwd(a, b, text):
        x1, x2 = a.x+a.w+10, b.x-10; S.poly([(x1, 210), (x2, 210)], end="arrow"); S.label((x1+x2)/2, 186, text, 12, "middle", INK, True)
    def ret(a, b, text):
        x1, x2 = b.x-10, a.x+a.w+10; S.poly([(x1, 234), (x2, 234)], end="open", dash="6 4"); S.label((x1+x2)/2, 262, text, 12, "middle", MUTED, False, True)
    fwd(clerk, ui, "1: submit form"); fwd(ui, hnd, "2: POST /api/parcels"); fwd(hnd, srv, "3: register(dto, account)")
    ret(clerk, ui, "9: confirmation"); ret(ui, hnd, "8: 201 / 409"); ret(hnd, srv, "7: Parcel / error")
    S.poly([(808, 256), (808, 392)], end="arrow"); S.label(800, 316, "4: existsByCadastralNumber(nr)", 12, "end", INK, True)
    S.poly([(842, 256), (842, 392)], end="arrow"); S.label(850, 316, "5: save(parcel)", 12, "start", INK, True)
    S.poly([(915, 410), (995, 410)], end="arrow"); S.label(955, 384, "4.1 / 5.1: SELECT / INSERT", 12, "middle", INK, True)
    S.poly([(995, 434), (915, 434)], end="open", dash="6 4"); S.label(955, 462, "6: result", 12, "middle", MUTED, False, True)
    S.text(20, 500, "Numbers show the order of the messages and dashed arrows are returns. Scenario: a clerk registers a parcel.", 11.5, "start", False, MUTED, True)
    S.add('</g>')
    return export(S, "com_register_parcel", BUILD)

# ---------------------------------------------------------------- UI mock-ups
def window(S, title, url):
    S.rect(10, 10, 580, 440, "#FFFFFF", "#6B7280", 1.6, 8); S.rect(10, 10, 580, 34, "#E5E7EB", "#6B7280", 1.6, 8)
    for i, c in enumerate(("#F87171", "#FBBF24", "#34D399")): S.add(f'<circle cx="{30+i*18}" cy="27" r="5" fill="{c}"/>')
    S.rect(110, 17, 440, 20, "#FFFFFF", "#9CA3AF", 1, 10); S.text(122, 31, url, 11, "start", False, MUTED)
def navbar(S, items, active=None, role=None):
    S.rect(10, 44, 580, 38, C["nav"], C["nav"], 1, 0); S.text(26, 68, "Cadastru", 15, "start", True, "#FFFFFF")
    x = 580
    for t in reversed(items):
        w = tw(t, 12.5) + 18; x -= w; S.text(x+w/2, 68, t, 12.5, "middle", t == active, "#FFFFFF"); x -= 4
    if role: S.text(150, 68, role, 11, "start", False, "#BFD4EE")
def field(S, x, y, w, label, value="", dd=False):
    S.text(x, y, label, 11.5, "start", True, INK); S.rect(x, y+6, w, 26, "#FFFFFF", "#9CA3AF", 1.2, 4)
    if value: S.text(x+8, y+24, value, 12, "start", False, MUTED)
    if dd: S.text(x+w-16, y+24, "v", 11, "middle", False, MUTED)
def button(S, x, y, w, label, primary=True):
    S.rect(x, y, w, 30, C["nav"] if primary else "#FFFFFF", C["nav"], 1.4, 5); S.text(x+w/2, y+20, label, 12.5, "middle", True, "#FFFFFF" if primary else C["nav"])
def table(S, x, y, cols, rows, widths):
    S.rect(x, y, sum(widths), 26, "#E5E7EB", "#9CA3AF", 1, 0); cx = x
    for c, w in zip(cols, widths): S.text(cx+8, y+18, c, 11.5, "start", True, INK, maxw=w-10); cx += w
    for i, r in enumerate(rows):
        yy = y+26+i*26; S.rect(x, yy, sum(widths), 26, "#FFFFFF", "#D1D5DB", 1, 0); cx = x
        for v, w in zip(r, widths):
            if v in ("Owned", "Not owned"):
                S.rect(cx+6, yy+5, 72, 17, "#E7F5EC" if v == "Not owned" else "#EAF1FB", C["ok_s"] if v == "Not owned" else C["proc_s"], 1, 8); S.text(cx+42, yy+17.5, v, 10.5, "middle", True, INK)
            else: S.text(cx+8, yy+18, v, 11.5, "start", False, INK, maxw=w-10)
            cx += w

def mockups():
    S = Svg(600, 460); window(S, "", "https://cadastru.example/search"); navbar(S, ["Search", "Log in", "Register"], "Search")
    S.text(30, 112, "Search the register", 16, "start", True, INK); S.text(30, 130, "Public view: shows only whether a parcel or building is owned.", 11.5, "start", False, MUTED)
    field(S, 30, 152, 170, "Cadastral number", "100234"); field(S, 215, 152, 190, "Address", "Str. Florilor"); field(S, 420, 152, 140, "Type", "Any", True); button(S, 30, 204, 100, "Search")
    table(S, 30, 256, ["Cadastral no.", "Address", "Type", "Status"], [["100234", "Str. Florilor 5", "Parcel", "Owned"], ["100234-C1", "Str. Florilor 5", "House", "Owned"], ["100301", "Str. Mare 12", "Parcel", "Not owned"], ["100417", "Str. Lunga 3", "Parcel", "Owned"]], [110, 170, 100, 150])
    export(S, "ui_public_search", BUILD)
    S = Svg(600, 360); window(S, "", "https://cadastru.example/login"); navbar(S, ["Search", "Log in", "Register"], "Log in")
    S.rect(150, 110, 300, 210, "#FFFFFF", "#D1D5DB", 1.4, 8); S.text(300, 140, "Log in", 17, "middle", True, INK)
    field(S, 175, 160, 250, "Email", "ion@example.com"); field(S, 175, 212, 250, "Password", "********"); button(S, 175, 262, 250, "Log in")
    S.text(300, 312, "No account yet?  Register", 11.5, "middle", False, C["nav"])
    export(S, "ui_login", BUILD)
    S = Svg(600, 470); window(S, "", "https://cadastru.example/my-properties"); navbar(S, ["Search", "My properties", "Log out"], "My properties", "owner: Ion Popescu")
    S.text(30, 112, "My properties", 16, "start", True, INK)
    table(S, 30, 128, ["Cadastral no.", "Address", "Type", "Share"], [["100234", "Str. Florilor 5", "Parcel", "40 %"], ["100234-C1", "Str. Florilor 5", "House", "40 %"]], [110, 190, 110, 120])
    S.rect(30, 238, 530, 210, "#F9FAFB", "#D1D5DB", 1.2, 6); S.text(44, 262, "Ownership history: parcel 100234", 13, "start", True, INK)
    table(S, 44, 274, ["Owner", "Share", "Price", "From", "To"], [["Ion Popescu", "100 %", "40 000", "2019-05-10", "2024-02-29"], ["Delta Build SRL", "60 %", "39 000", "2024-03-01", "current"], ["Ion Popescu", "40 %", "16 000", "2024-03-01", "current"]], [150, 70, 80, 100, 90])
    export(S, "ui_owner", BUILD)
    S = Svg(600, 470); window(S, "", "https://cadastru.example/clerk/parcels/new"); navbar(S, ["Parcels", "Buildings", "Owners", "Ownership", "Log out"], "Parcels", "clerk")
    S.text(30, 112, "Register a parcel", 16, "start", True, INK)
    field(S, 30, 136, 240, "Cadastral number *", "100234"); field(S, 290, 136, 270, "Address *", "Str. Florilor 5, Cluj-Napoca")
    field(S, 30, 200, 240, "Size (m2) *", "450.00"); field(S, 290, 200, 270, "Land use *", "Residential", True)
    S.rect(30, 270, 530, 70, "#FFF4D6", C["dec_s"], 1.2, 6); S.text(44, 294, "Validation messages appear here, for example:", 11.5, "start", True, INK); S.text(44, 314, "\"The cadastral number is already registered.\"", 11.5, "start", False, INK, True)
    button(S, 30, 360, 110, "Save"); button(S, 150, 360, 110, "Cancel", False)
    export(S, "ui_clerk_parcel", BUILD)

if __name__ == "__main__":
    for f in (usecases, activity, states, packages, components, communication, mockups):
        r = f(); print(f.__name__, "ok")
