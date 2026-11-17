"""Small SVG drawing helpers (pure Python) used to build the Cadastru diagrams.
SVG -> PNG conversion uses macOS Quick Look (qlmanage) and sips, so nothing needs to be installed."""
from html import escape
import subprocess, os, math

FONT = "Helvetica, Arial, sans-serif"
INK = "#1F2937"; LINE = "#374151"; MUTED = "#6B7280"
C = dict(nav="#1F4E79", proc_f="#EAF1FB", proc_s="#2F5C99", dec_f="#FFF4D6", dec_s="#B7791F",
         err_f="#FDECEC", err_s="#B42318", ok_f="#E7F5EC", ok_s="#1E7B4B", act_f="#FFF4DC", act_s="#B7791F",
         fe_f="#E6EEFA", fe_s="#2F5C99", be_f="#E8F4EC", be_s="#1E7B4B", db_f="#F1E9F8", db_s="#6B3FA0",
         grey_f="#F3F4F6", grey_s="#6B7280")
HDR = {"blue": "#D6E4F7", "green": "#D3EBDC", "amber": "#FBE6B8", "purple": "#E6D9F2", "grey": "#E5E7EB"}
EDG = {"blue": "#2F5C99", "green": "#1E7B4B", "amber": "#B7791F", "purple": "#6B3FA0", "grey": "#6B7280"}

def tw(t, size, bold=False):
    w = 0.0
    for ch in t:
        if ch in "il.,:;'|!()[]{}tfjI ": w += 0.29
        elif ch in "mwMW@": w += 0.86
        elif ch.isupper(): w += 0.68
        elif ch.isdigit(): w += 0.556
        else: w += 0.54
    return w * size * (1.07 if bold else 1.0)

class Shape:
    def __init__(s, x, y, w, h, kind="rect"): s.x, s.y, s.w, s.h, s.kind = x, y, w, h, kind
    @property
    def cx(s): return s.x + s.w/2
    @property
    def cy(s): return s.y + s.h/2
    def a(s, side, f=0.5):
        if s.kind == "diamond": f = 0.5
        return {"t": (s.x+s.w*f, s.y), "b": (s.x+s.w*f, s.y+s.h), "l": (s.x, s.y+s.h*f), "r": (s.x+s.w, s.y+s.h*f)}[side]

class Svg:
    def __init__(s, w, h): s.w, s.h, s.el, s.warn = w, h, [], []
    def add(s, x): s.el.append(x)
    def rect(s, x, y, w, h, fill="#fff", stroke=LINE, sw=1.5, rx=0, dash=None, op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""; o = f' fill-opacity="{op}"' if op is not None else ""
        s.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{o} stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def line(s, x1, y1, x2, y2, stroke=LINE, sw=1.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def text(s, x, y, t, size=13, anchor="start", bold=False, fill=INK, italic=False, under=False, halo=False, maxw=None):
        if maxw and tw(t, size, bold) > maxw: s.warn.append(f"text too wide ({tw(t,size,bold):.0f}>{maxw:.0f}): {t}")
        st = []
        if halo: st.append('stroke="white" stroke-width="4" stroke-linejoin="round" paint-order="stroke"')
        if bold: st.append('font-weight="700"')
        if italic: st.append('font-style="italic"')
        if under: st.append('text-decoration="underline"')
        s.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" {" ".join(st)}>{escape(t)}</text>')
    def lines(s, cx, cy, ls, size=13, bold=False, fill=INK, gap=1.25, maxw=None):
        n = len(ls); lh = size*gap; y0 = cy - (n-1)*lh/2 + size*0.35
        for i, t in enumerate(ls): s.text(cx, y0 + i*lh, t, size, "middle", bold, fill, maxw=maxw)
    def poly(s, pts, end=None, start=None, dash=None, stroke=LINE, sw=1.5):
        clean = [pts[0]]
        for p in pts[1:]:
            if abs(p[0]-clean[-1][0]) > 0.1 or abs(p[1]-clean[-1][1]) > 0.1: clean.append(p)
        pts = clean
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        m = (f' marker-end="url(#{end})"' if end else "") + (f' marker-start="url(#{start})"' if start else "")
        da = f' stroke-dasharray="{dash}"' if dash else ""
        s.add(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"{da}{m}/>')
    def diamond(s, sh, fill, stroke, sw=1.5):
        s.add(f'<polygon points="{sh.cx:.1f},{sh.y:.1f} {sh.x+sh.w:.1f},{sh.cy:.1f} {sh.cx:.1f},{sh.y+sh.h:.1f} {sh.x:.1f},{sh.cy:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def label(s, x, y, t, size=12, anchor="start", fill=MUTED, bold=False, italic=False):
        s.text(x, y, t, size, anchor, bold, fill, italic, halo=True)
    def render(s):
        defs = f'''<defs>
<marker id="arrow" markerWidth="12" markerHeight="10" refX="11" refY="5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L11,5 L0,10 z" fill="{LINE}"/></marker>
<marker id="open" markerWidth="12" markerHeight="12" refX="11" refY="6" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0.5 L11,6 L0,11.5" fill="none" stroke="{LINE}" stroke-width="1.5"/></marker>
<marker id="tri" markerWidth="16" markerHeight="14" refX="14" refY="7" orient="auto" markerUnits="userSpaceOnUse"><path d="M0.5,0.5 L14,7 L0.5,13.5 z" fill="white" stroke="{LINE}" stroke-width="1.5"/></marker>
<marker id="arrow2" markerWidth="12" markerHeight="10" refX="11" refY="5" orient="auto-start-reverse" markerUnits="userSpaceOnUse"><path d="M0,0 L11,5 L0,10 z" fill="{LINE}"/></marker>
</defs>'''
        L = max(s.w, s.h)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{L}" height="{L}" viewBox="0 0 {L} {L}">{defs}'
                f'<rect width="{L}" height="{L}" fill="white"/><g transform="translate({(L-s.w)/2:.1f},{(L-s.h)/2:.1f})">' + "".join(s.el) + '</g></svg>')

def route(p, q, sp, sq, mid=None):
    (px, py), (qx, qy) = p, q; vp, vq = sp in "tb", sq in "tb"
    if vp and vq:
        if abs(px-qx) < 0.5: return [p, q]
        m = mid if mid is not None else (py+qy)/2
        return [p, (px, m), (qx, m), q]
    if (not vp) and (not vq):
        if abs(py-qy) < 0.5: return [p, q]
        m = mid if mid is not None else (px+qx)/2
        return [p, (m, py), (m, qy), q]
    if vp and not vq: return [p, (px, qy), q]
    return [p, (qx, py), q]

def export(svg, name, outdir):
    """Render the SVG to a 2x PNG. Quick Look renders a square canvas, the drawing is centred on it
    and sips crops it back to the real size."""
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, name + ".svg"); open(path, "w", encoding="utf8").write(svg.render())
    big = int(max(svg.w, svg.h) * 2)
    subprocess.run(["qlmanage", "-t", "-s", str(big), "-o", outdir, path], capture_output=True)
    png = os.path.join(outdir, name + ".png"); os.replace(path + ".png", png)
    subprocess.run(["sips", "--cropToHeightWidth", str(int(svg.h*2)), str(int(svg.w*2)), png], capture_output=True)
    for w in svg.warn: print(f"[{name}] WARN", w)
    return png

# ---------------- UML helpers ----------------
def classbox(S, x, y, w, name, attrs=(), methods=None, stereo=None, color="blue", fs=12):
    hh = 30 + (15 if stereo else 0)
    ah = (len(attrs)*17 + 12) if attrs else 0
    mh = (len(methods)*17 + 12) if methods else 0
    h = hh + ah + mh; sh = Shape(x, y, w, h); st = EDG[color]
    S.rect(x, y, w, h, "#FFFFFF", st, 1.6, 4)
    S.add(f'<path d="M{x},{y+hh} L{x},{y+4} Q{x},{y} {x+4},{y} L{x+w-4},{y} Q{x+w},{y} {x+w},{y+4} L{x+w},{y+hh} Z" fill="{HDR[color]}" stroke="{st}" stroke-width="1.6"/>')
    if stereo:
        S.text(x+w/2, y+16, f"«{stereo}»", 11.5, "middle", False, MUTED)
        S.text(x+w/2, y+hh-9, name, 13.5, "middle", True, INK, maxw=w-10)
    else: S.text(x+w/2, y+hh/2+5, name, 13.5, "middle", True, INK, maxw=w-10)
    for i, a in enumerate(attrs): S.text(x+10, y+hh+16+i*17, a, fs, "start", False, INK, maxw=w-16)
    if ah and mh: S.line(x, y+hh+ah, x+w, y+hh+ah, st, 1.2)
    for i, m in enumerate(methods or []): S.text(x+10, y+hh+ah+16+i*17, m, fs, "start", False, INK, maxw=w-16)
    if ah or mh: S.line(x, y+hh, x+w, y+hh, st, 1.2)
    return sh

def objbox(S, x, y, w, name, cls, attrs, color="blue", fs=12):
    hh = 28; h = hh + len(attrs)*17 + 12; sh = Shape(x, y, w, h); st = EDG[color]
    S.rect(x, y, w, h, "#FFFFFF", st, 1.6, 4)
    S.add(f'<path d="M{x},{y+hh} L{x},{y+4} Q{x},{y} {x+4},{y} L{x+w-4},{y} Q{x+w},{y} {x+w},{y+4} L{x+w},{y+hh} Z" fill="{HDR[color]}" stroke="{st}" stroke-width="1.6"/>')
    S.text(x+w/2, y+hh/2+5, f"{name} : {cls}", 13, "middle", True, INK, under=True, maxw=w-10)
    for i, a in enumerate(attrs): S.text(x+10, y+hh+16+i*17, a, fs, "start", False, INK, maxw=w-14)
    return sh

def mult(S, pts, m_start=None, m_end=None, size=12):
    def place(p, q, t):
        dx, dy = q[0]-p[0], q[1]-p[1]; L = math.hypot(dx, dy) or 1; ux, uy = dx/L, dy/L
        if abs(uy) > 0.5: anchor, x, y = "start", p[0] + 8, p[1] + uy*18 + 4
        else: anchor, x, y = "middle", p[0] + ux*20, p[1] - 8
        S.label(x, y, t, size, anchor, INK, True)
    if m_start: place(pts[0], pts[1], m_start)
    if m_end: place(pts[-1], pts[-2], m_end)

def assoc(S, pts, m1=None, m2=None, end=None, dash=None, name=None, nx=None, ny=None, nanchor="middle"):
    S.poly(pts, end=end, dash=dash); mult(S, pts, m1, m2)
    if name:
        a, b = pts[len(pts)//2-1], pts[len(pts)//2]
        S.label(nx if nx is not None else (a[0]+b[0])/2, ny if ny is not None else (a[1]+b[1])/2-7, name, 11.5, nanchor, MUTED, False, True)

def tablebox(S, x, y, w, name, cols, color="blue"):
    """ER table: cols = [(badges, name, type)], badges like 'PK', 'FK', 'UQ', 'FK UQ', ''"""
    hh = 28; rh = 19; h = hh + len(cols)*rh + 8; sh = Shape(x, y, w, h); st = EDG[color]
    S.rect(x, y, w, h, "#FFFFFF", st, 1.6, 4)
    S.add(f'<path d="M{x},{y+hh} L{x},{y+4} Q{x},{y} {x+4},{y} L{x+w-4},{y} Q{x+w},{y} {x+w},{y+4} L{x+w},{y+hh} Z" fill="{HDR[color]}" stroke="{st}" stroke-width="1.6"/>')
    S.text(x+w/2, y+hh/2+5, name, 13.5, "middle", True, INK)
    for i, (badge, cname, ctype) in enumerate(cols):
        yy = y + hh + 6 + (i+1)*rh - 5
        if badge: S.text(x+8, yy, badge, 10, "start", True, st)
        S.text(x+52, yy, cname, 11.5, "start", False, INK, maxw=w-52-92)
        S.text(x+w-8, yy, ctype, 10.5, "end", False, MUTED)
    return sh

# ---------------- flow chart helper ----------------
class Flow:
    def __init__(s, w, h): s.S = Svg(w, h); s.n = {}
    def term(s, k, cx, cy, text, w=130, h=38):
        sh = Shape(cx-w/2, cy-h/2, w, h); s.n[k] = sh
        s.S.rect(sh.x, sh.y, w, h, C["nav"], C["nav"], 1.5, h/2); s.S.text(cx, cy+4.5, text, 13, "middle", True, "#FFFFFF")
    def proc(s, k, cx, cy, lines, w=210, h=46, kind="proc"):
        if isinstance(lines, str): lines = [lines]
        h = max(h, 18*len(lines)+16); sh = Shape(cx-w/2, cy-h/2, w, h); s.n[k] = sh
        f, st = {"proc": (C["proc_f"], C["proc_s"]), "err": (C["err_f"], C["err_s"]), "ok": (C["ok_f"], C["ok_s"])}[kind]
        s.S.rect(sh.x, sh.y, w, h, f, st, 1.5, 7); s.S.lines(cx, cy, lines, 13, False, INK, maxw=w-14)
    def dec(s, k, cx, cy, lines, w=250, h=78):
        if isinstance(lines, str): lines = [lines]
        sh = Shape(cx-w/2, cy-h/2, w, h, "diamond"); s.n[k] = sh
        s.S.diamond(sh, C["dec_f"], C["dec_s"]); s.S.lines(cx, cy, lines, 12.5, False, INK, maxw=w*0.62)
    def edge(s, a, sa, b, sb, label=None, mid=None, via=None, ldx=0, ldy=0):
        A, B = s.n[a], s.n[b]; p, q = A.a(sa), B.a(sb)
        pts = [p] + list(via) + [q] if via else route(p, q, sa, sb, mid)
        s.S.poly(pts, end="arrow")
        if label:
            x, y = p
            if sa == "b": s.S.label(x+8+ldx, y+18+ldy, label, 12, "start", INK, True)
            elif sa == "r": s.S.label(x+8+ldx, y-7+ldy, label, 12, "start", INK, True)
            elif sa == "l": s.S.label(x-8+ldx, y-7+ldy, label, 12, "end", INK, True)
            else: s.S.label(x+8+ldx, y-8+ldy, label, 12, "start", INK, True)

# ---------------- sequence diagram helper ----------------
def sequence(parts, msgs, frames=(), W=1060, x0=96, step=176, top=20, dy=30):
    cols = {"actor": ("act_f","act_s"), "ui": ("fe_f","fe_s"), "handler": ("be_f","be_s"), "service": ("be_f","be_s"), "repo": ("be_f","be_s"), "db": ("db_f","db_s")}
    n = len(parts); xs = [x0 + i*step for i in range(n)]; hdr_h = 46; y = top + hdr_h + 34; ys = []
    for m in msgs: ys.append(y); y += dy + (14 if m.get("kind") == "self" else 0)
    H = int(y + 20); S = Svg(W, H)
    for i in range(n): S.line(xs[i], top+hdr_h, xs[i], H-14, "#9CA3AF", 1.3, "6 5")
    for fr in frames:
        y1 = ys[fr["start"]] - 22; y2 = ys[fr["end"]] + 16; x1 = xs[fr["x1"]] - 26; x2 = xs[fr["x2"]] + 26
        S.rect(x1, y1, x2-x1, y2-y1, "none", "#6B7280", 1.3, 4); S.rect(x1, y1, 78, 20, "#F3F4F6", "#6B7280", 1.3, 3)
        S.text(x1+39, y1+14.5, fr["kind"], 12, "middle", True, INK)
        S.text(x1+88, y1+14.5, f"[{fr['cond']}]", 12, "start", False, INK, italic=True, halo=True)
        if "else_at" in fr:
            ye = ys[fr["else_at"]] - 22; S.line(x1, ye, x2, ye, "#6B7280", 1.3, "7 4")
            S.text(x1+88, ye+15, f"[{fr['else_cond']}]", 12, "start", False, INK, italic=True, halo=True)
    for i, (lab, kind) in enumerate(parts):
        f, st = cols[kind]; bw = 138
        S.rect(xs[i]-bw/2, top, bw, hdr_h, C[f], C[st], 1.6, 6); S.lines(xs[i], top+hdr_h/2, lab.split("\n"), 12.5, True, INK, maxw=bw-8)
    for m, y in zip(msgs, ys):
        a, b = m["f"], m["t"]; label = f'{m["num"]}: {m["label"]}'
        if m.get("kind") == "self":
            x = xs[a]; S.poly([(x, y-8), (x+44, y-8), (x+44, y+10), (x, y+10)], end="arrow"); S.text(x+52, y+3, label, 12, "start", False, INK, halo=True); continue
        xa, xb = xs[a], xs[b]; dash = "6 4" if m.get("kind") == "ret" else None
        S.poly([(xa, y), (xb, y)], end="open" if dash else "arrow", dash=dash)
        S.text((xa+xb)/2, y-7, label, 12, "middle", False, INK, halo=True, maxw=abs(xb-xa)-12)
    return S
