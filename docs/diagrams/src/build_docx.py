"""Builds docs/Cadastru_Design_Diagrams_1-5.docx from the PNGs produced by gen_diagrams.py (pure Python, no Word needed)."""
import zipfile, struct, os
from xml.sax.saxutils import escape as esc

BUILD = os.environ.get("BUILD", "/private/tmp/claude-501/-Users-dindiliganbogdan-Project-Cadastru/83778627-cef0-4add-bc92-88247cfbe8f3/scratchpad/build")
OUT = os.environ.get("OUT", "/Users/dindiliganbogdan/Project_Cadastru/docs/Cadastru_Design_Diagrams_1-5.docx")
EMU = 914400
body, rels, media = [], [], []
nfig = [0]; did = [100]

def png_size(p):
    d = open(p, "rb").read(32); return struct.unpack(">II", d[16:24])

def P(text="", style=None, align=None, keep=False, pbb=False, before=None, after=None):
    ppr = (f'<w:pStyle w:val="{style}"/>' if style else '') + ('<w:keepNext/>' if keep else '') + ('<w:pageBreakBefore/>' if pbb else '')
    if before is not None or after is not None:
        ppr += '<w:spacing' + (f' w:before="{before}"' if before is not None else '') + (f' w:after="{after}"' if after is not None else '') + '/>'
    if align: ppr += f'<w:jc w:val="{align}"/>'
    return f'<w:p>{"<w:pPr>"+ppr+"</w:pPr>" if ppr else ""}<w:r><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>'

def bullet(text):
    return ('<w:p><w:pPr><w:pStyle w:val="ListBullet"/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')

def figure(file, caption, max_w_in, max_h_in):
    nfig[0] += 1; path = os.path.join(BUILD, file); w, h = png_size(path); ratio = w / h
    hi = max_h_in; wi = hi * ratio
    if wi > max_w_in: wi = max_w_in; hi = wi / ratio
    cx, cy = int(wi*EMU), int(hi*EMU); rid = f"rIdImg{nfig[0]}"; name = f"image{nfig[0]}.png"
    rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{name}"/>')
    media.append((name, path)); did[0] += 1
    drawing = (f'<w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
               f'<wp:docPr id="{did[0]}" name="Figure {nfig[0]}" descr="{esc(caption)}"/><wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
               f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
               f'<pic:nvPicPr><pic:cNvPr id="{did[0]}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
               f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing>')
    body.append(f'<w:p><w:pPr><w:keepNext/><w:spacing w:before="60" w:after="40"/><w:jc w:val="center"/></w:pPr><w:r>{drawing}</w:r></w:p>')
    body.append(P(f"Figure {nfig[0]} – {caption}", style="Caption", align="center"))

def sect(orient):
    pg = '<w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/>' if orient == "landscape" else '<w:pgSz w:w="11906" w:h="16838"/>'
    return f'<w:sectPr><w:footerReference w:type="default" r:id="rIdFooter"/>{pg}<w:pgMar w:top="720" w:right="720" w:bottom="720" w:left="720" w:header="360" w:footer="360" w:gutter="0"/></w:sectPr>'
def section_end(orient): body.append(f'<w:p><w:pPr>{sect(orient)}</w:pPr></w:p>')

LW, LH = 10.4, 5.5      # landscape image box (inches)
PW, PH = 7.4, 8.3       # portrait image box

# ---------------- title page
body.append(P("Cadastru – System Design Diagrams", style="Title"))
body.append(P("Cadastre management web application  ·  Diagrams 1 to 5, updated to the implemented database", style="Subtitle"))
body.append(P("Dindiligan Bogdan  ·  11.11.2026  ·  Version 0.2 (draft)", style="Meta"))
body.append(P("Contents", style="Heading2"))
for t in ["1.  General system architecture diagram", "2.  Flow charts (log in, register a parcel, search the register, change ownership)",
          "3.  Class diagrams and database schema (domain model, backend structure, ER diagram)", "4.  Object diagram",
          "5.  Sequence diagrams (log in, register a parcel, view the ownership history, change ownership)"]:
    body.append(P(t))
body.append(P("Assumptions used in the diagrams", style="Heading2", before=200))
for t in [
 "Frontend: Angular (TypeScript). Backend: plain Java 21 with Javalin, JDBC and a HikariCP connection pool (no Spring). Database: PostgreSQL 17 running in Docker.",
 "Three kinds of visitor: anyone without a login (public view: parcels and buildings are shown only as owned or not owned, with no names), an owner (an account linked to an owner record, who sees their own properties in detail) and a clerk (who maintains the register).",
 "An account has the role user or clerk. “Owner” is not a role but a fact: the account is linked to an owner record. A clerk creates that link. A person or a company can own property without having an account.",
 "An owner record is either a single user (a person) or a company, never both.",
 "Ownership is stored in two tables, parcel_ownership and building_ownership: owner, property, share (percentage), price paid for that share, start date and end date. The end date is the last day of ownership and is empty for the current period. Co-owners are separate rows, and the periods of one owner on one property never overlap.",
 "A building stands on exactly one parcel. Land use and building type come from lookup tables.",
 "Rules checked by the service and not by the database: the current shares of a property total at most 100%, a building is registered only on an owned parcel, and the full CNP validation."]:
    body.append(bullet(t))

# ---------------- 1 architecture
body.append(P("1. General System Architecture Diagram", style="Heading1", pbb=True))
body.append(P("The system is a three-tier web application. Visitors, owners and clerks use the Angular frontend in the browser, which talks to the Java backend through a REST API using JSON. The backend is split into handler, service and repository layers and reaches PostgreSQL, which runs in Docker, through JDBC and a connection pool. The database holds the ten tables listed in the diagram.", keep=True))
figure("d1_architecture.png", "General system architecture", LW, LH)
section_end("landscape")

# ---------------- 2 flow charts (portrait)
body.append(P("2. Flow Charts", style="Heading1"))
body.append(P("The flow charts show the step-by-step logic of four operations. Diamonds are decisions, red boxes are error paths and green boxes are successful results.", keep=True))
body.append(P("2.1 Log in", style="Heading2", keep=True))
body.append(P("The user enters email and password. If the account exists and the password is correct, a session or token is created and the role is loaded. A clerk goes to the clerk home page. Any other account is checked for a link to an owner: a linked account sees its own properties, an unlinked one gets the public view.", keep=True))
figure("d2a_login.png", "Flow chart: log in", PW, PH)
body.append(P("2.2 Register a parcel", style="Heading2", pbb=True, keep=True))
body.append(P("Only a logged-in clerk can register a parcel. The data, including the land use, is validated and the cadastral number must not already exist. When both checks pass, the parcel is saved and a confirmation is shown.", keep=True))
figure("d2b_register_parcel.png", "Flow chart: register a parcel", PW, PH)
body.append(P("2.3 Search the register", style="Heading2", pbb=True, keep=True))
body.append(P("Search is open to everybody. Visitors and accounts without an owner link get the public view, which shows only whether a parcel or building is owned. A linked owner sees their own properties in full detail and the others in the public view. A clerk searches the whole register with all details.", keep=True))
figure("d2c_search.png", "Flow chart: search the register", PW, PH)
body.append(P("2.4 Change ownership", style="Heading2", pbb=True, keep=True))
body.append(P("A change of owner or share closes the current row (end date = new start date minus one day) and inserts a new row, in one transaction. The dates and the total share (at most 100%) are checked first. The database refuses overlapping periods and invalid dates, and in that case the transaction is rolled back.", keep=True))
figure("d2d_change_ownership.png", "Flow chart: change ownership", PW, PH)
section_end("portrait")

# ---------------- 3 class diagrams + ER (landscape)
body.append(P("3. Class Diagrams and Database Schema", style="Heading1"))
body.append(P("3.1 Domain model", style="Heading2", keep=True))
body.append(P("An Account has a role and may be linked to one Owner. An Owner is either a SingleUser (person) or a Company. ParcelOwnership and BuildingOwnership connect an owner to a parcel or a building over time, with share, price and dates. A parcel has a land use and can have many buildings, and each building has a type.", keep=True))
figure("d3a_class_domain.png", "Class diagram: domain model", LW, LH-0.5)
body.append(P("3.2 Backend structure and design patterns", style="Heading2", pbb=True, keep=True))
body.append(P("The backend follows Handler → Service → Repository. The service depends on the ParcelRepository interface, which JdbcParcelRepository implements. Patterns used: Repository, DTO (ParcelDto), Builder (ParcelBuilder), Factory (RepositoryFactory) and Singleton (ConnectionPool). The same structure is repeated for buildings, owners and accounts.", keep=True))
figure("d3b_class_patterns.png", "Class diagram: backend structure and design patterns (shown for Parcel)", LW, LH-0.15)
body.append(P("3.3 Database schema", style="Heading2", pbb=True, keep=True))
body.append(P("The ten tables as created in PostgreSQL, with primary keys, foreign keys, unique and optional columns, and the rules the database enforces on its own.", keep=True))
figure("d3c_database_er.png", "Database schema (ER diagram)", LW, LH)

# ---------------- 4 object
body.append(P("4. Object Diagram", style="Heading1", pbb=True))
body.append(P("A snapshot of the system at one moment. Ion Popescu owned 100% of parcel 100234 until 2024-02-29. Since 2024-03-01 Delta Build SRL holds 60% and Ion keeps 40%, so they are co-owners. Delta Build SRL also owns the building on the parcel. Rows with an end date of null are the current periods.", keep=True))
figure("d4_object.png", "Object diagram: ownership of parcel 100234", LW, LH-0.2)

# ---------------- 5 sequence
body.append(P("5. Sequence Diagrams", style="Heading1", pbb=True))
body.append(P("5.1 Log in", style="Heading2", keep=True))
body.append(P("The Angular UI sends the credentials to the AuthHandler. The AuthService loads the account and verifies the password hash. On success it returns a token and the role; otherwise the user gets a 401 error.", keep=True))
figure("d5a_seq_login.png", "Sequence diagram: log in", LW, LH-0.5)
body.append(P("5.2 Register a parcel", style="Heading2", pbb=True, keep=True))
body.append(P("The service checks that the user is a clerk, validates the data and checks that the cadastral number is new before saving. A duplicate number ends with a 409 Conflict.", keep=True))
figure("d5b_seq_register_parcel.png", "Sequence diagram: register a parcel", LW, LH-0.2)
body.append(P("5.3 View the ownership history", style="Heading2", pbb=True, keep=True))
body.append(P("An owner opens the history of a parcel. The service loads the history from the repository and checks that the parcel belongs to the logged-in owner before returning it; otherwise it answers 403 Forbidden.", keep=True))
figure("d5c_seq_ownership_history.png", "Sequence diagram: view the ownership history", LW, LH-0.2)
body.append(P("5.4 Change ownership", style="Heading2", pbb=True, keep=True))
body.append(P("The service checks the role, the dates and the total share, closes the current row and inserts the new one, then commits. If the database refuses either statement because of an overlap or invalid dates, everything is rolled back and the clerk sees a 409 Conflict.", keep=True))
figure("d5d_seq_change_ownership.png", "Sequence diagram: change ownership", LW, LH-0.3)

NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"')
document = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS}><w:body>{"".join(body)}{sect("landscape")}</w:body></w:document>'
styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/><w:sz w:val="21"/><w:szCs w:val="21"/><w:lang w:val="en-GB"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="100" w:line="264" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="240" w:after="60"/></w:pPr><w:rPr><w:b/><w:color w:val="1F4E79"/><w:sz w:val="52"/><w:szCs w:val="52"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:after="60"/></w:pPr><w:rPr><w:color w:val="4B5563"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:customStyle="1" w:styleId="Meta"><w:name w:val="Meta"/><w:basedOn w:val="Normal"/><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="8" w:space="8" w:color="1F4E79"/></w:pBdr><w:spacing w:after="240"/></w:pPr><w:rPr><w:color w:val="6B7280"/><w:sz w:val="20"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="120" w:after="80"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:color w:val="1F4E79"/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="120" w:after="60"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:color w:val="2F5C99"/><w:sz w:val="27"/><w:szCs w:val="27"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="caption"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="20" w:after="0"/></w:pPr><w:rPr><w:i/><w:color w:val="6B7280"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListBullet"><w:name w:val="List Bullet"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="60"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Footer"><w:name w:val="footer"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="0"/></w:pPr><w:rPr><w:color w:val="6B7280"/><w:sz w:val="17"/></w:rPr></w:style>
</w:styles>'''
numbering = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="hybridMultilevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="540" w:hanging="270"/></w:pPr><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/></w:rPr></w:lvl></w:abstractNum><w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>'''
footer = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:p><w:pPr><w:pStyle w:val="Footer"/></w:pPr><w:r><w:t xml:space="preserve">Cadastru – System Design Diagrams   |   Page </w:t></w:r><w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>'''
ctypes = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/><Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>'''
root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>'''
core = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>Cadastru – System Design Diagrams</dc:title><dc:creator>Dindiligan Bogdan</dc:creator></cp:coreProperties>'''
doc_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
 '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
 '<Relationship Id="rIdNum" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
 '<Relationship Id="rIdFooter" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>' + "".join(rels) + '</Relationships>')

import xml.dom.minidom as md
for x in (document, styles, numbering, footer, ctypes, doc_rels, root_rels, core): md.parseString(x.encode("utf8"))
if os.path.exists(OUT): os.remove(OUT)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", ctypes); z.writestr("_rels/.rels", root_rels); z.writestr("word/document.xml", document)
    z.writestr("word/styles.xml", styles); z.writestr("word/numbering.xml", numbering); z.writestr("word/footer1.xml", footer)
    z.writestr("word/_rels/document.xml.rels", doc_rels); z.writestr("docProps/core.xml", core)
    for name, p in media: z.write(p, "word/media/" + name)
print("written", OUT, os.path.getsize(OUT)//1024, "KB;", len(media), "images")
