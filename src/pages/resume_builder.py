import streamlit as st
import streamlit.components.v1 as components
from src.utils.resume_pdf_template import build_resume_pdf
from io import BytesIO


# Map Streamlit session data into the ReportLab PDF template schema
def _map_resume_data_for_template(resume_state: dict) -> dict:
    personal = resume_state.get("personal_info", {}) or {}

    # Skills: flatten categories -> simple list
    skills_section = resume_state.get("skills", {}) or {}
    flat_skills = []
    for cat, items in skills_section.items():
        for s in items:
            flat_skills.append(s)

    # Experience: accept either "details" or split "description" into bullets
    mapped_experience = []
    for exp in (resume_state.get("experience") or []):
        details = exp.get("details")
        if not details:
            desc = (exp.get("description") or "").strip().splitlines()
            details = [d.strip() for d in desc if d.strip()]
        mapped_experience.append({
            "title": exp.get("title", ""),
            "company": exp.get("company", ""),
            "location": exp.get("location", ""),
            "years": exp.get("years") or (f"{exp.get('start_date','')} – {exp.get('end_date','')}").strip(" –"),
            "details": details
        })

    # Education
    mapped_education = []
    for ed in (resume_state.get("education") or []):
        ed_details = ed.get("details")
        if not ed_details:
            e_desc = (ed.get("description") or "").strip().splitlines()
            ed_details = [d.strip() for d in e_desc if d.strip()]
        mapped_education.append({
            "degree": ed.get("degree", ""),
            "institution": ed.get("institution", ""),
            "location": ed.get("location", ""),
            "years": ed.get("years") or (f"{ed.get('start_date','')} – {ed.get('end_date','')}").strip(" –"),
            "details": ed_details
        })

    # Projects
    mapped_projects = []
    for p in (resume_state.get("projects") or []):
        mapped_projects.append({
            "name": p.get("title", p.get("name", "")),
            "role": p.get("role", ""),
            "period": p.get("period", ""),
            "description": p.get("description", ""),
            "technologies": p.get("technologies", ""),
            "link": p.get("link", "")
        })

    return {
        "name": personal.get("name", ""),
        "role": personal.get("role", ""),
        "location": personal.get("location", ""),
        "email": personal.get("email", ""),
        "phone": personal.get("phone", ""),
        "linkedin": personal.get("linkedin", ""),
        "website": personal.get("website", ""),
        "summary": personal.get("summary", ""),
        "skills": flat_skills,
        "achievements": resume_state.get("achievements", []) or [],
        "experience": mapped_experience,
        "education": mapped_education,
        "projects": mapped_projects,
        "additional": resume_state.get("additional_info", []) or [],
    }


# --- GLOBAL CSS STYLING ---
st.markdown("""
<style>
  .stButton>button {background-color:#007bff;color:white;border-radius:6px;}
  .stButton>button:hover {background-color:#0056b3;color:white;}
  .timeline-item {background: #f2f7ff; border-left: 4px solid #007bff; padding: 15px 20px; margin-bottom: 20px; border-radius: 8px;}
  ul {padding-left: 20px;}
</style>
""", unsafe_allow_html=True)


def show():
    # Initialize session state
    if "resume_data" not in st.session_state:
        st.session_state["resume_data"] = {
            "personal_info": {},
            "skills": {},
            "achievements": [],
            "experience": [],
            "education": [],
            "projects": [],
            "additional_info": []
        }

    # Tabs
    tabs = st.tabs([
        "Personal Info",
        "Skills",
        "Key Achievements",
        "Experience",
        "Education",
        "Projects",
        "Additional Info",
        "Preview"
    ])

    with tabs[0]: personal_info_section()
    with tabs[1]: skills_section()
    with tabs[2]: achievements_section()
    with tabs[3]: experience_section()
    with tabs[4]: education_section()
    with tabs[5]: projects_section()
    with tabs[6]: additional_info_section()
    with tabs[7]: preview_resume()


# ---------------- SECTIONS ----------------

def personal_info_section():
    st.markdown("### 📘 Personal Information")
    personal_info = st.session_state["resume_data"].get("personal_info", {})

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", personal_info.get("name", ""))
        role = st.text_input("Professional Role", personal_info.get("role", ""))
        email = st.text_input("Email", personal_info.get("email", ""))
        phone = st.text_input("Phone", personal_info.get("phone", ""))
    with col2:
        location = st.text_input("Location", personal_info.get("location", ""))
        linkedin = st.text_input("LinkedIn URL", personal_info.get("linkedin", ""))
        website = st.text_input("Portfolio Website", personal_info.get("website", ""))

    summary = st.text_area("Professional Summary", personal_info.get("summary", ""), height=150)

    st.session_state["resume_data"]["personal_info"] = {
        "name": name, "role": role, "email": email, "phone": phone,
        "location": location, "linkedin": linkedin, "website": website, "summary": summary
    }
    st.markdown("---")


def education_section():
    st.markdown("### 🎓 Education")
    if "education" not in st.session_state["resume_data"]:
        st.session_state["resume_data"]["education"] = []

    for i, edu in enumerate(st.session_state["resume_data"]["education"]):
        with st.expander(f"{edu.get('degree', 'No Degree')} - {edu.get('institution', 'No Institution')}"):
            st.markdown(edu.get("description", ""))
            if st.button("Remove", key=f"remove_education_{i}"):
                st.session_state["resume_data"]["education"].pop(i)
                st.rerun()

    with st.expander("Add New Education"):
        with st.form("resume_education_form"):
            degree = st.text_input("Degree/Certificate")
            institution = st.text_input("Institution")
            location = st.text_input("Location")
            start_date = st.text_input("Start Date (e.g., Sep 2020)")
            end_date = st.text_input("End Date (e.g., Jun 2024 or Present)")
            description = st.text_area("Description (use new lines for bullet points)")
            if st.form_submit_button("Add Education"):
                if degree and institution:
                    new_edu = {
                        "degree": degree, "institution": institution, "location": location,
                        "start_date": start_date, "end_date": end_date, "description": description
                    }
                    st.session_state["resume_data"]["education"].append(new_edu)
                    st.success("Education added!")
                    st.rerun()
                else:
                    st.warning("Please enter at least the degree and institution.")
    st.markdown("---")


def experience_section():
    st.markdown("### 💼 Professional Experience")
    if "experience" not in st.session_state["resume_data"]:
        st.session_state["resume_data"]["experience"] = []

    for i, exp in enumerate(st.session_state["resume_data"]["experience"]):
        with st.expander(f"{exp.get('title', 'No Title')} at {exp.get('company', 'No Company')}"):
            st.markdown(exp.get("description", ""))
            if st.button("Remove", key=f"remove_experience_{i}"):
                st.session_state["resume_data"]["experience"].pop(i)
                st.rerun()

    with st.expander("Add New Experience"):
        with st.form("resume_experience_form"):
            title = st.text_input("Job Title")
            company = st.text_input("Company")
            location = st.text_input("Location")
            start_date = st.text_input("Start Date (e.g., Jan 2020)")
            end_date = st.text_input("End Date (e.g., Dec 2023 or Present)")
            description = st.text_area("Description (use new lines for bullet points)")
            if st.form_submit_button("Add Experience"):
                if title and company:
                    new_exp = {
                        "title": title, "company": company, "location": location,
                        "start_date": start_date, "end_date": end_date, "description": description
                    }
                    st.session_state["resume_data"]["experience"].append(new_exp)
                    st.success("Experience added!")
                    st.rerun()
                else:
                    st.warning("Please enter at least the job title and company.")
    st.markdown("---")


def skills_section():
    st.markdown("### 🛠 Skills & Expertise")
    if "skills" not in st.session_state["resume_data"]:
        st.session_state["resume_data"]["skills"] = {}

    for category in st.session_state["resume_data"]["skills"].keys():
        with st.expander(f"Category: {category}"):
            st.write(", ".join(st.session_state["resume_data"]["skills"][category]))
            if st.button("Remove Category", key=f"remove_category_{category}"):
                del st.session_state["resume_data"]["skills"][category]
                st.rerun()

    with st.expander("Add New Skill Category"):
        with st.form("resume_skills_form"):
            category = st.text_input("Category Name (e.g., Programming Languages, Tools, Soft Skills)")
            skills = st.text_area("Skills (comma-separated)")
            if st.form_submit_button("Add Skills"):
                if category and skills:
                    skills_list = [skill.strip() for skill in skills.split(",") if skill.strip()]
                    st.session_state["resume_data"]["skills"][category] = skills_list
                    st.success("Skills category added!")
                    st.rerun()
                else:
                    st.warning("Please enter both category name and skills.")
    st.markdown("---")


def projects_section():
    st.markdown("### 📂 Projects")
    if "projects" not in st.session_state["resume_data"]:
        st.session_state["resume_data"]["projects"] = []

    for i, proj in enumerate(st.session_state["resume_data"]["projects"]):
        with st.expander(f"{proj.get('title', 'No Title')}"):
            st.markdown(proj.get("description", ""))
            if st.button("Remove", key=f"remove_project_{i}"):
                st.session_state["resume_data"]["projects"].pop(i)
                st.rerun()

    with st.expander("Add New Project"):
        with st.form("resume_projects_form"):
            title = st.text_input("Project Title")
            role = st.text_input("Your Role")
            period = st.text_input("Time Period (e.g., Jan 2023 - Mar 2023)")
            description = st.text_area("Description (use new lines for bullet points)")
            technologies = st.text_input("Technologies Used (comma-separated)")
            link = st.text_input("Project Link (optional)")
            if st.form_submit_button("Add Project"):
                if title and description:
                    new_proj = {
                        "title": title, "role": role, "period": period,
                        "description": description, "technologies": technologies, "link": link
                    }
                    st.session_state["resume_data"]["projects"].append(new_proj)
                    st.success("Project added!")
                    st.rerun()
                else:
                    st.warning("Please enter at least the project title and description.")
    st.markdown("---")


def achievements_section():
    st.markdown("### 🏆 Key Achievements")
    for i, achievement in enumerate(st.session_state["resume_data"]["achievements"]):
        with st.expander(f"Achievement {i+1}"):
            st.markdown(achievement)
            if st.button("Remove", key=f"remove_achievement_{i}"):
                st.session_state["resume_data"]["achievements"].pop(i)
                st.rerun()

    with st.expander("Add New Achievement"):
        new_achievement = st.text_area("Achievement Description", key="new_achievement_desc")
        if st.button("Add Achievement", key="btn_add_achievement"):
            if new_achievement:
                st.session_state["resume_data"]["achievements"].append(new_achievement)
                st.success("Achievement added!")
                st.rerun()
            else:
                st.warning("Please enter an achievement description.")
    st.markdown("---")


def additional_info_section():
    st.markdown("### ℹ Additional Info")
    info_list = st.session_state["resume_data"].get("additional_info", [])
    for i, info in enumerate(info_list):
        st.write(info)
        if st.button("Remove", key=f"remove_info_{i}"):
            info_list.pop(i)
            st.rerun()

    new_info = st.text_area("Add Additional Info", key="new_additional_info")
    if st.button("Add Info", key="btn_add_info"):
        if new_info:
            info_list.append(new_info)
            st.session_state["resume_data"]["additional_info"] = info_list
            st.success("Additional Info added!")
            st.rerun()
    st.markdown("---")


# ---------------- PREVIEW ----------------
def preview_resume():
    st.markdown("### 🖥 Resume Preview")
    resume_state = st.session_state["resume_data"]
    data = _map_resume_data_for_template(resume_state)

    # Build contact line (linkify only http/https)
    contact_bits = [x for x in [
        data.get("location"), data.get("email"), data.get("phone"),
        data.get("linkedin"), data.get("website")
    ] if x]
    def _linkify(v: str) -> str:
        return f'<a href="{v}" target="_blank">{v}</a>' if v.startswith("http://") or v.startswith("https://") else v
    contact_html = " | ".join(_linkify(x) for x in contact_bits)

    # HTML (style + body) rendered once
    html = f"""
    <div id="resume-root">
      <style>
        #resume-root * {{ box-sizing: border-box; }}
        :root {{ --ink:#111; --muted:#59606a; --rule:#d9dde3; }}
        #resume-root .sheet {{
          background:#fff; width:794px; margin:10px auto; border-radius:12px;
          box-shadow:0 6px 28px rgba(0,0,0,.20); padding:34px 38px 38px;
          color:var(--ink); font:14px/1.5 system-ui,Segoe UI,Roboto,Helvetica,Arial;
        }}
        #resume-root h1 {{ margin:0; text-align:center; font-weight:800; letter-spacing:.6px; font-size:28px; }}
        #resume-root .role {{ margin:6px 0 10px; text-align:center; font-size:13px; font-weight:700; letter-spacing:.5px; }}
        #resume-root .contact {{ font-size:12px; color:var(--muted); text-align:center; border-top:1px solid var(--rule); padding-top:8px; }}
        #resume-root .contact a {{ color:var(--muted); text-decoration:none; }}
        #resume-root .summary {{ margin-top:12px; font-size:13px; color:#2b2b2b; }}
        #resume-root .hsec {{ margin-top:18px; font-weight:800; font-size:12px; letter-spacing:.9px; text-transform:uppercase; }}
        #resume-root .divider {{ margin:6px 0 10px; height:1px; background:var(--rule); border:none; }}
        #resume-root .grid-2 {{ display:grid; grid-template-columns:1fr 1fr; gap:4px 18px; font-size:12.5px; }}
        #resume-root ul.bul {{ list-style:disc; margin:6px 0 4px; padding-left:18px; font-size:12.5px; }}
        #resume-root ul.bul li {{ margin:6px 0; }}
        #resume-root .row {{ display:flex; justify-content:space-between; align-items:flex-start; gap:16px; margin:10px 0 14px; }}
        #resume-root .row .l {{ flex:1 1 auto; min-width:0; }}
        #resume-root .row .r {{ flex:0 0 auto; width:180px; text-align:right; font-size:12.5px; color:var(--muted); margin-top:2px; }}
        #resume-root .title {{ font-weight:700; font-size:13.5px; margin:0; }}
        #resume-root .sub {{ font-size:12.5px; color:var(--muted); margin:2px 0 6px; }}
        #resume-root .small {{ font-size:12px; color:var(--muted); }}
      </style>

      <div class="sheet">
        <h1>{data.get("name","")}</h1>
        <div class="role">{(data.get("role") or "").upper()}</div>
        <div class="contact">{contact_html}</div>

        {f"<div class='summary'>{data['summary']}</div>" if data.get("summary") else ""}

        {(
          "<div class='hsec'>Area of Expertise</div><hr class='divider' />"
          "<div class='grid-2'>"
          + "".join(f"<div>{s}</div>" for s in data.get("skills", []))
          + "</div>"
        ) if data.get("skills") else ""}

        {(
          "<div class='hsec'>Key Achievements</div><hr class='divider' />"
          "<ul class='bul'>"
          + "".join(f"<li>{a}</li>" for a in data.get("achievements", []))
          + "</ul>"
        ) if data.get("achievements") else ""}

        {(
          "<div class='hsec'>Professional Experience</div><hr class='divider' />"
          + "".join(
              "<div class='row'><div class='l'>"
              f"<p class='title'>{e.get('title','')}</p>"
              f"<p class='sub'>{e.get('company','')}{(' · ' + e.get('location','')) if e.get('location') else ''}</p>"
              + ("<ul class='bul'>" + "".join(f"<li>{d}</li>" for d in e.get('details', [])) + "</ul>" if e.get('details') else "")
              + "</div><div class='r'>" + (e.get('years','')) + "</div></div>"
              for e in data.get("experience", [])
            )
        ) if data.get("experience") else ""}

        {(
          "<div class='hsec'>Education</div><hr class='divider' />"
          + "".join(
              "<div class='row'><div class='l'>"
              f"<p class='title'>{ed.get('degree','')}</p>"
              f"<p class='sub'>{ed.get('institution','')}{(' · ' + ed.get('location','')) if ed.get('location') else ''}</p>"
              + ("<ul class='bul'>" + "".join(f"<li>{d}</li>" for d in ed.get('details', [])) + "</ul>" if ed.get('details') else "")
              + "</div><div class='r'>" + (ed.get('years','')) + "</div></div>"
              for ed in data.get("education", [])
            )
        ) if data.get("education") else ""}

        {(
          "<div class='hsec'>Projects</div><hr class='divider' />"
          + "".join(
              "<div class='row'><div class='l'>"
              f"<p class='title'>{p.get('name','')}</p>"
              f"<p class='sub'>{p.get('role','')}</p>"
              + (f"<p>{p.get('description','')}</p>" if p.get("description") else "")
              + (f"<p class='small'><strong>Technologies:</strong> {p.get('technologies','')}</p>" if p.get('technologies') else "")
              + (f"<p class='small'><a href='{p.get('link')}' target='_blank'>{p.get('link')}</a></p>" if p.get('link') else "")
              + "</div><div class='r'>" + (p.get('period','')) + "</div></div>"
              for p in data.get("projects", [])
            )
        ) if data.get("projects") else ""}

        {(
          "<div class='hsec'>Additional Information</div><hr class='divider' />"
          "<ul class='bul'>"
          + "".join(f"<li>{it}</li>" for it in data.get("additional", []))
          + "</ul>"
        ) if data.get("additional") else ""}
      </div>
    </div>
    """

    components.html(html, height=1200, scrolling=True)

    # Export
    st.subheader("Export Resume")
    if st.button("Download as PDF", key="btn_download_pdf"):
        buf = BytesIO()
        build_resume_pdf(buf, data)
        buf.seek(0)
        st.download_button(
            label="Click here to download PDF",
            data=buf.read(),
            file_name="resume.pdf",
            mime="application/pdf",
            key="btn_download_pdf_dl"
        )

