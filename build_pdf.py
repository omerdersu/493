import markdown
from weasyprint import HTML
from pathlib import Path
import base64, re

report_md = Path("report_phase1.md").read_text(encoding="utf-8")

# Embed images as base64 so they appear in the PDF
img_map = {
    "histograms.png": Path("histograms.png"),
    "warmup.png": Path("warmup.png"),
}

# Insert figures at the right places in the markdown
figure_1 = '\n\n![Figure 1 — Distribution Fits](histograms.png)\n\n'
figure_2 = '\n\n![Figure 2 — Warm-up Period](warmup.png)\n\n'

report_md = report_md.replace(
    "Histograms with the fitted curves are shown in Figure 1.",
    "Histograms with the fitted curves are shown in Figure 1." + figure_1
)
report_md = report_md.replace(
    "The warm-up plot is shown in Figure 2.",
    "The warm-up plot is shown in Figure 2." + figure_2
)

# Convert markdown to HTML
html_body = markdown.markdown(report_md, extensions=["tables", "fenced_code"])

# Replace image src with base64
for fname, fpath in img_map.items():
    if fpath.exists():
        b64 = base64.b64encode(fpath.read_bytes()).decode()
        html_body = html_body.replace(
            f'src="{fname}"',
            f'src="data:image/png;base64,{b64}"'
        )

html_full = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    @page {{
        size: A4;
        margin: 2cm;
    }}
    body {{
        font-family: 'Georgia', 'Times New Roman', serif;
        font-size: 11pt;
        line-height: 1.5;
        color: #222;
    }}
    h1 {{
        font-size: 20pt;
        border-bottom: 2px solid #333;
        padding-bottom: 6px;
        margin-top: 0;
    }}
    h2 {{
        font-size: 14pt;
        color: #1a1a1a;
        margin-top: 24px;
        border-bottom: 1px solid #ccc;
        padding-bottom: 4px;
    }}
    h3 {{
        font-size: 12pt;
        color: #333;
        margin-top: 18px;
    }}
    table {{
        border-collapse: collapse;
        margin: 12px 0;
        font-size: 10pt;
        width: 100%;
    }}
    th, td {{
        border: 1px solid #999;
        padding: 6px 10px;
        text-align: left;
    }}
    th {{
        background-color: #f0f0f0;
        font-weight: bold;
    }}
    tr:nth-child(even) {{
        background-color: #fafafa;
    }}
    img {{
        max-width: 100%;
        display: block;
        margin: 16px auto;
    }}
    hr {{
        border: none;
        border-top: 1px solid #ddd;
        margin: 20px 0;
    }}
    strong {{
        color: #111;
    }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

HTML(string=html_full).write_pdf("report_phase1.pdf")
print("PDF created: report_phase1.pdf")
