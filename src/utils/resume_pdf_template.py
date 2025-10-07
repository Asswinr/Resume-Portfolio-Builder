from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def build_resume_pdf(target, data):
    """
    target can be a path string (e.g., 'resume.pdf') OR a file-like buffer (e.g., io.BytesIO()).
    """
    doc = SimpleDocTemplate(
        target,                  # accepts file-like or path
        pagesize=A4,
        topMargin=28,
        bottomMargin=28,
        leftMargin=32,
        rightMargin=32
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Name", fontSize=18, leading=22, spaceAfter=6, alignment=1))  # center
    styles.add(ParagraphStyle(name="Role", fontSize=10.5, leading=14, spaceAfter=6, alignment=1))
    styles.add(ParagraphStyle(name="Contact", fontSize=9.5, textColor=colors.grey, alignment=1, spaceAfter=10))
    styles.add(ParagraphStyle(name="H", fontSize=10.5, leading=14, spaceBefore=10, spaceAfter=4, textTransform="uppercase"))
    styles.add(ParagraphStyle(name="Body", fontSize=10.3, leading=14))
    styles.add(ParagraphStyle(name="Subtle", fontSize=9.8, textColor=colors.grey))

    story = []
    story.append(Paragraph(data["name"], styles["Name"]))
    story.append(Paragraph(data.get("role",""), styles["Role"]))
    contact = " | ".join([x for x in [data.get("location"), data.get("email"), data.get("phone"), data.get("linkedin"), data.get("website")] if x])
    story.append(Paragraph(contact, styles["Contact"]))
    if data.get("summary"):
        story.append(Paragraph(data["summary"], styles["Body"]))

    # Skills grid (2 columns)
    if data.get("skills"):
        story.append(Paragraph("Area of Expertise", styles["H"]))
        skills = data["skills"]
        rows = []
        for i in range(0, len(skills), 2):
            left = skills[i]
            right = skills[i+1] if i+1 < len(skills) else ""
            rows.append([left, right])
        tbl = Table(rows, colWidths=[250, 250])
        tbl.setStyle(TableStyle([('BOTTOMPADDING',(0,0),(-1,-1),2)]))
        story.append(tbl)

    # Experience
    if data.get("experience"):
        story.append(Paragraph("Professional Experience", styles["H"]))
        for e in data["experience"]:
            years = e.get("years") or f'{e.get("start_date","")} – {e.get("end_date","")}'
            story.append(Paragraph(f'<b>{e.get("title","")}</b>', styles["Body"]))
            sub = " · ".join([x for x in [e.get("company"), e.get("location")] if x])
            story.append(Paragraph(sub, styles["Subtle"]))
            items = e.get("details")
            if not items:
                desc = (e.get("description") or "").strip().splitlines()
                items = [d for d in desc if d.strip()]
            if items:
                story.append(ListFlowable([ListItem(Paragraph(i, styles["Body"])) for i in items], bulletType='bullet'))
            story.append(Paragraph(years, styles["Subtle"]))
            story.append(Spacer(1, 6))

    # Education
    if data.get("education"):
        story.append(Paragraph("Education", styles["H"]))
        for ed in data["education"]:
            years = ed.get("years") or f'{ed.get("start_date","")} – {ed.get("end_date","")}'
            story.append(Paragraph(f'<b>{ed.get("degree","")}</b>', styles["Body"]))
            sub = " · ".join([x for x in [ed.get("institution"), ed.get("location")] if x])
            story.append(Paragraph(sub, styles["Subtle"]))
            if ed.get("details"):
                story.append(ListFlowable([ListItem(Paragraph(i, styles["Body"])) for i in ed["details"]], bulletType='bullet'))
            story.append(Paragraph(years, styles["Subtle"]))
            story.append(Spacer(1, 6))

    # Projects
    if data.get("projects"):
        story.append(Paragraph("Projects", styles["H"]))
        for p in data["projects"]:
            story.append(Paragraph(f'<b>{p.get("name","")}</b>', styles["Body"]))
            story.append(Paragraph(p.get("role",""), styles["Subtle"]))
            if p.get("description"): story.append(Paragraph(p["description"], styles["Body"]))
            if p.get("technologies"): story.append(Paragraph(f'<b>Technologies:</b> {p["technologies"]}', styles["Subtle"]))
            if p.get("link"): story.append(Paragraph(p["link"], styles["Subtle"]))
            if p.get("period"): story.append(Paragraph(p["period"], styles["Subtle"]))
            story.append(Spacer(1, 6))

    # Additional
    if data.get("additional"):
        story.append(Paragraph("Additional Information", styles["H"]))
        story.append(ListFlowable([ListItem(Paragraph(i, styles["Body"])) for i in data["additional"]], bulletType='bullet'))

    doc.build(story)
