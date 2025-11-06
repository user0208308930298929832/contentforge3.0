
import io, csv
from datetime import datetime
from typing import Dict, Any
from fpdf import FPDF

def export_csv_bytes(contents: Dict[str, Any]) -> bytes:
    output = io.StringIO()
    w = csv.writer(output)
    w.writerow(["type","platform","idea","caption","hashtags","cta"])
    for s in contents.get("shorts", []):
        w.writerow(["short", s.get("platform",""), s.get("idea",""), s.get("caption",""),
                    " ".join(s.get("hashtags", [])), s.get("cta","")])
    for c in contents.get("carousels", []):
        w.writerow(["carousel","instagram", c.get("title",""),
                    " | ".join(c.get("bullets", [])), "", ""])
    for b in contents.get("blogs", []):
        w.writerow(["blog","blog", b.get("title",""),
                    " | ".join(b.get("outline", [])), "", ""])
    return output.getvalue().encode("utf-8")

def export_txt_bytes(contents: Dict[str, Any]) -> bytes:
    lines = [f"# Export {datetime.utcnow().isoformat()}Z", ""]
    lines.append("## Shorts")
    for s in contents.get("shorts", []):
        lines += [f"### {s.get('platform','').upper()} — {s.get('idea','')}", s.get("caption","")]
        if s.get("hashtags"): lines.append(" ".join(s["hashtags"]))
        if s.get("cta"): lines.append(f"CTA: {s['cta']}")
        lines.append("")
    lines.append("## Carrosséis (IG)")
    for c in contents.get("carousels", []):
        lines.append(f"### {c.get('title','')}")
        for b in c.get("bullets", []): lines.append(f"- {b}")
        lines.append("")
    lines.append("## Blogs")
    for b in contents.get("blogs", []):
        lines.append(f"### {b.get('title','')}")
        for o in b.get("outline", []): lines.append(f"- {o}")
        lines.append("")
    return "\n".join(lines).encode("utf-8")

def export_pdf_bytes(contents: Dict[str, Any], title: str="ContentForge Report") -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, title, ln=1)
    pdf.set_font("Arial", size=11)

    def write_section(h):
        pdf.set_font("Arial","B",13); pdf.ln(2); pdf.cell(0,8,h,ln=1); pdf.set_font("Arial", size=11)

    write_section("Shorts")
    for s in contents.get("shorts", []):
        pdf.multi_cell(0,6, f"- [{s.get('platform','').upper()}] {s.get('idea','')}")
        pdf.multi_cell(0,6, f"  {s.get('caption','')}")
        if s.get("hashtags"): pdf.multi_cell(0,6, "  " + " ".join(s["hashtags"]))
        if s.get("cta"): pdf.multi_cell(0,6, f"  CTA: {s['cta']}")
        pdf.ln(2)

    write_section("Carrosséis (IG)")
    for c in contents.get("carousels", []):
        pdf.multi_cell(0,6, f"- {c.get('title','')}")
        for b in c.get("bullets", []): pdf.multi_cell(0,6, f"   • {b}")
        pdf.ln(1)

    write_section("Blogs")
    for b in contents.get("blogs", []):
        pdf.multi_cell(0,6, f"- {b.get('title','')}")
        for o in b.get("outline", []): pdf.multi_cell(0,6, f"   • {o}")
        pdf.ln(1)

    return bytes(pdf.output(dest="S").encode("latin-1"))
