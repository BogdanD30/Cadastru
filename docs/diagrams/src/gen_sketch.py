"""Hand-sketched look for the UI mock-ups (wobbly pencil lines, handwriting font, marker highlights)."""
import os, random
from lib import Svg, export
BUILD = os.environ.get("BUILD", "/private/tmp/claude-501/-Users-dindiliganbogdan-Project-Cadastru/83778627-cef0-4add-bc92-88247cfbe8f3/scratchpad/build")
HAND = "Bradley Hand, Marker Felt, Noteworthy, Comic Sans MS, cursive"
INK = "#2a2a2a"; PENCIL = "#555555"

class Sk:
    def __init__(s, w, h, seed):
        s.S = Svg(w, h); s.r = random.Random(seed)
    def j(s, a=1.2): return s.r.uniform(-a, a)
    def line(s, x1, y1, x2, y2, w=1.9, col=INK, passes=2, wob=1.4):
        for p in range(passes):
            mx, my = (x1+x2)/2 + s.j(wob), (y1+y2)/2 + s.j(wob)
            d = f"M{x1+s.j():.1f},{y1+s.j():.1f} Q{mx:.1f},{my:.1f} {x2+s.j():.1f},{y2+s.j():.1f}"
            s.S.add(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w if p == 0 else w*0.6:.1f}" stroke-linecap="round" opacity="{1 if p == 0 else 0.55}"/>')
    def rect(s, x, y, w, h, fill=None, col=INK, sw=1.9, over=3):
        if fill:
            s.S.add(f'<path d="M{x+s.j(2):.1f},{y+s.j(2):.1f} L{x+w+s.j(2):.1f},{y+s.j(2):.1f} L{x+w+s.j(2):.1f},{y+h+s.j(2):.1f} L{x+s.j(2):.1f},{y+h+s.j(2):.1f} Z" fill="{fill}" opacity="0.55" stroke="none"/>')
        s.line(x-over, y, x+w+over, y, sw, col); s.line(x+w, y-over, x+w, y+h+over, sw, col)
        s.line(x+w+over, y+h, x-over, y+h, sw, col); s.line(x, y+h+over, x, y-over, sw, col)
    def circle(s, cx, cy, rx, ry=None, fill=None, col=INK, sw=1.9, loops=1):
        ry = ry or rx
        for lp in range(loops):
            pts = []
            n = 14; off = s.r.uniform(0, 6.28)
            for i in range(n+2):
                a = off + i*6.2832/n; k = 1 + s.j(0.04)
                pts.append((cx+rx*k*__import__("math").cos(a), cy+ry*k*__import__("math").sin(a)))
            d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
            s.S.add(f'<path d="{d}" fill="{fill or "none"}" fill-opacity="0.5" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>')
    def text(s, x, y, t, size=16, anchor="start", bold=False, col=INK, rot=None):
        r = s.r.uniform(-1.1, 1.1) if rot is None else rot
        s.S.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{HAND}" font-size="{size}" text-anchor="{anchor}" fill="{col}" {"font-weight=\"700\"" if bold else ""} transform="rotate({r:.2f} {x:.1f} {y:.1f})">{__import__("html").escape(t)}</text>')
    def scribble(s, x, y, w, col=PENCIL):
        pts = []; n = max(4, int(w/9))
        for i in range(n+1): pts.append((x+i*w/n, y+(4 if i % 2 else -2)+s.j(0.8)))
        s.S.add('<path d="M' + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts) + f'" fill="none" stroke="{col}" stroke-width="1.5" stroke-linecap="round" opacity="0.7"/>')
    def hatch(s, x, y, w, h, gap=7, col=PENCIL):
        k = -h
        while k < w:
            x1, y1, x2, y2 = x+max(k, 0), y+max(-k, 0), x+min(k+h, w), y+min(h, h-(k+h-w)) if k+h > w else y+h
            s.S.add(f'<line x1="{x+max(k,0):.1f}" y1="{y+(h if k<0 else 0)-(0 if k<0 else 0):.1f}" x2="{x+min(k+h,w):.1f}" y2="{y+(0 if k+h<=w else h-(k+h-w)):.1f}" stroke="{col}" stroke-width="1" opacity="0.45"/>') if False else None
            k += gap
        for i in range(int(w/gap)+1):
            xs = x + i*gap
            s.S.add(f'<line x1="{xs:.1f}" y1="{y+h:.1f}" x2="{min(xs+h, x+w):.1f}" y2="{y+h-(min(xs+h, x+w)-xs):.1f}" stroke="{col}" stroke-width="1" opacity="0.45"/>')
    def arrow(s, x1, y1, x2, y2, col=INK):
        s.line(x1, y1, x2, y2, 1.8, col, 1, 2.5)
        import math
        a = math.atan2(y2-y1, x2-x1)
        for da in (2.5, -2.5):
            s.line(x2, y2, x2-12*math.cos(a+da*0.22), y2-12*math.sin(a+da*0.22), 1.8, col, 1, 0.5)
    def note(s, x, y, w, h, lines, col="#FFE680"):
        s.rect(x, y, w, h, fill=col, col=PENCIL, sw=1.6, over=1)
        for i, t in enumerate(lines): s.text(x+10, y+22+i*20, t, 14.5)

def window(k, url):
    k.rect(12, 12, 576, 436 if False else 0, None) if False else None
    k.rect(14, 14, 572, k.S.h-28, fill=None, sw=2.2)
    k.line(14, 52, 586, 52, 2)
    for i in range(3): k.circle(36+i*20, 33, 5.5, fill="#BBBBBB", sw=1.5)
    k.rect(118, 22, 440, 24, sw=1.6, over=1); k.text(130, 40, url, 14, col=PENCIL)

def nav(k, brand, items, active=None, who=None):
    k.text(30, 84, brand, 22, bold=True); k.line(28, 90, 28+len(brand)*12, 90, 1.6, INK, 1)
    x = 574
    for t in reversed(items):
        w = len(t)*8.2+6; x -= w
        k.text(x, 82, t, 16, bold=(t == active))
        if t == active: k.circle(x+w/2-2, 76, w/2+7, 14, sw=1.5)
        x -= 14
    if who: k.text(574, 120, who, 13.5, "end", col=PENCIL)
    k.line(20, 100, 580, 100, 1.4, PENCIL, 1)

def field(k, x, y, w, label, value="", dd=False):
    k.text(x, y, label, 14.5, bold=True); k.rect(x, y+8, w, 28, sw=1.6, over=1)
    if value: k.text(x+9, y+28, value, 15, col=PENCIL)
    if dd: k.line(x+w-22, y+19, x+w-15, y+27, 1.6); k.line(x+w-15, y+27, x+w-8, y+19, 1.6)

def button(k, x, y, w, label, hatched=True):
    k.rect(x, y, w, 32, sw=2.1, over=2)
    if hatched: k.hatch(x+2, y+2, w-4, 28, 8)
    k.text(x+w/2, y+22, label, 16, "middle", bold=True)

def table(k, x, y, cols, rows, widths, rowh=30, marks=None):
    W = sum(widths); cx = x
    for c, w in zip(cols, widths): k.text(cx+6, y+20, c, 15, bold=True); cx += w
    k.line(x, y+27, x+W, y+27, 2.2); k.line(x, y+31, x+W, y+31, 1.2, PENCIL, 1)
    for i, r in enumerate(rows):
        yy = y+32+i*rowh; cx = x
        for v, w in zip(r, widths):
            if marks and v in marks:
                col = marks[v]; k.circle(cx+w/2-10 if False else cx+44, yy+17, 40, 12, fill=col, sw=1.5)
                k.text(cx+44, yy+22, v, 14, "middle", bold=True)
            else: k.text(cx+6, yy+22, v, 15)
            cx += w
        k.line(x, yy+rowh, x+W, yy+rowh+ (1 if i % 2 else -1), 1, PENCIL, 1, 0.8)
    k.line(x, y+27, x, y+32+len(rows)*rowh, 1.4, PENCIL, 1); k.line(x+W, y+27, x+W, y+32+len(rows)*rowh, 1.4, PENCIL, 1)

def sketches():
    # 1. public search
    k = Sk(600, 480, 11); window(k, "cadastru.example/search"); nav(k, "Cadastru", ["Search", "Log in", "Register"], "Search")
    k.text(30, 134, "Search the register", 22, bold=True); k.text(30, 156, "public view: only owned / not owned", 14.5, col=PENCIL)
    field(k, 30, 184, 170, "Cadastral number", "100234"); field(k, 215, 184, 190, "Address", "Str. Florilor"); field(k, 420, 184, 150, "Type", "any", True)
    button(k, 30, 242, 110, "Search")
    table(k, 30, 296, ["Cadastral no.", "Address", "Type", "Status"], [["100234", "Str. Florilor 5", "Parcel", "Owned"], ["100234-C1", "Str. Florilor 5", "House", "Owned"], ["100301", "Str. Mare 12", "Parcel", "Not owned"]], [118, 168, 90, 154], marks={"Owned": "#FFD27F", "Not owned": "#9FE3B0"})
    k.arrow(548, 430, 508, 376); k.text(560, 454, "no names, no prices!", 15, "end", col="#B42318", bold=True)
    export(k.S, "ui_public_search", BUILD)
    # 2. login
    k = Sk(600, 380, 22); window(k, "cadastru.example/login"); nav(k, "Cadastru", ["Search", "Log in", "Register"], "Log in")
    k.rect(150, 122, 300, 224, sw=2, over=2); k.text(300, 156, "Log in", 22, "middle", bold=True)
    field(k, 176, 184, 248, "Email", "ion@example.com"); field(k, 176, 240, 248, "Password", "* * * * * * * *")
    button(k, 176, 296, 248, "Log in")
    k.text(300, 340, "no account?  Register", 14.5, "middle", col=PENCIL); k.line(228, 345, 372, 345, 1.2, PENCIL, 1)
    k.arrow(500, 330, 456, 322); k.text(458, 354, "role decides the home page", 13.5, col="#B42318", bold=True) if False else None
    export(k.S, "ui_login", BUILD)
    # 3. owner
    k = Sk(600, 490, 33); window(k, "cadastru.example/my-properties"); nav(k, "Cadastru", ["Search", "My properties", "Log out"], "My properties", "logged in: owner Ion Popescu")
    k.text(30, 134, "My properties", 22, bold=True)
    table(k, 30, 150, ["Cadastral no.", "Address", "Type", "Share"], [["100234", "Str. Florilor 5", "Parcel", "40 %"], ["100234-C1", "Str. Florilor 5", "House", "40 %"]], [120, 190, 110, 110])
    k.rect(30, 262, 540, 206, fill="#EFEFEF", sw=1.8, over=2); k.text(44, 288, "Ownership history: parcel 100234", 16, bold=True)
    table(k, 44, 296, ["Owner", "Share", "Price", "From", "To"], [["Ion Popescu", "100 %", "40 000", "2019-05-10", "2024-02-29"], ["Delta Build SRL", "60 %", "39 000", "2024-03-01", "current"], ["Ion Popescu", "40 %", "16 000", "2024-03-01", "current"]], [148, 70, 82, 112, 90], rowh=28)
    k.text(430, 160, "read-only", 15, col="#B42318", bold=True); k.circle(470, 154, 44, 14, col="#B42318", sw=1.4)
    export(k.S, "ui_owner", BUILD)
    # 4. clerk register parcel
    k = Sk(600, 490, 44); window(k, "cadastru.example/clerk/parcels/new"); nav(k, "Cadastru", ["Parcels", "Buildings", "Owners", "Ownership", "Log out"], "Parcels", "logged in: clerk")
    k.text(30, 134, "Register a parcel", 22, bold=True)
    field(k, 30, 160, 240, "Cadastral number *", "100234"); field(k, 290, 160, 270, "Address *", "Str. Florilor 5, Cluj")
    field(k, 30, 232, 240, "Size (m2) *", "450.00"); field(k, 290, 232, 270, "Land use *", "Residential", True)
    k.note(30, 304, 300, 86, ["validation messages here:", "\"cadastral number is", "already registered\""])
    button(k, 30, 412, 110, "Save"); button(k, 156, 412, 110, "Cancel", False)
    k.text(360, 340, "* = required", 14.5, col=PENCIL); k.arrow(430, 364, 540, 262) if False else None
    export(k.S, "ui_clerk_parcel", BUILD)

if __name__ == "__main__":
    sketches(); print("sketches ok")
