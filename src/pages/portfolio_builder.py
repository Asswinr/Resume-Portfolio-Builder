# -*- coding: utf-8 -*-
import re
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from src.data.portfolio_data import PortfolioData, PersonalInfo, AboutMe, Experience, Education, Project, Contact, Skill
from src.utils.portfolio_generator import generate_portfolio_html


# ---------- Dynamic portfolio HTML builder ----------

def build_portfolio_from_data(pdata: PortfolioData, css_src: str, js_src: str) -> str:
    """
    Build a complete HTML portfolio using the exact template structure.
    Matches portfolio.html DOM so portfolio.css styles apply correctly.
    """
    # Extract user data safely
    name = getattr(pdata.personal_info, "name", "Your Name") or "Your Name"
    role = getattr(pdata.personal_info, "role", "Your Profession") or "Your Profession"
    intro = getattr(pdata.personal_info, "introduction", "") or ""
    
    bio = getattr(pdata.about_me, "biography", "") or "Welcome to my portfolio! I am a dedicated and passionate professional with a love for technology and creative problem-solving."
    
    # Skills list
    skills_html = ""
    if pdata.about_me and pdata.about_me.skills:
        skills_html = "<ul style='list-style:disc; padding-left:20px; text-align:left; max-width:700px; margin:1rem auto;'>"
        skills_html += "".join(f"<li>{s.name}</li>" for s in pdata.about_me.skills)
        skills_html += "</ul>"
    
    # Education - using timeline structure from original template
    education_html = ""
    if pdata.education:
        education_html = '<div class="timeline">'
        for edu in pdata.education:
            education_html += f"""
            <div class="timeline-item">
                <h3>{edu.degree}</h3>
                <h4>{edu.institution} | {edu.years}</h4>
                <p>Focused on relevant coursework and practical applications.</p>
            </div>
            """
        education_html += '</div>'
    else:
        education_html = "<p>No education entries yet. Add your degrees and certifications!</p>"
    
    # Experience - using timeline structure
    experience_html = ""
    if pdata.experience:
        experience_html = '<div class="timeline">'
        for exp in pdata.experience:
            experience_html += f"""
            <div class="timeline-item">
                <h3>{exp.role}</h3>
                <h4>{exp.company} | {exp.years}</h4>
                <p>{exp.description}</p>
            </div>
            """
        experience_html += '</div>'
    else:
        experience_html = "<p>No experience entries yet. Add your work history!</p>"
    
    # Projects - using original styling
    projects_html = ""
    if pdata.projects:
        for proj in pdata.projects:
            link_tag = f'<br><a href="{proj.link}" target="_blank" style="color:var(--accent-color); text-decoration:none; font-weight:600;">View Project →</a>' if proj.link else ""
            projects_html += f"""
            <div style="background:rgba(255,255,255,0.05); padding:1.5rem; border-radius:10px; margin-bottom:1.5rem; text-align:left;">
                <h3>{proj.title}</h3>
                <p>{proj.description}</p>
                {link_tag}
            </div>
            """
    else:
        projects_html = "<p>No projects yet. Showcase your best work here!</p>"
    
    # Contact
    email = getattr(pdata.contact, "email", "") or ""
    phone = getattr(pdata.contact, "phone", "") or ""
    linkedin = getattr(pdata.contact, "linkedin", "") or ""
    github = getattr(pdata.contact, "github", "") or ""
    twitter = getattr(pdata.contact, "twitter", "") or ""
    
    contact_items = []
    if email:
        contact_items.append(f"<strong>Email:</strong> <a href='mailto:{email}'>{email}</a>")
    if phone:
        contact_items.append(f"<strong>Phone:</strong> {phone}")
    if linkedin:
        contact_items.append(f"<strong>LinkedIn:</strong> <a href='{linkedin}' target='_blank'>{linkedin}</a>")
    if github:
        contact_items.append(f"<strong>GitHub:</strong> <a href='{github}' target='_blank'>{github}</a>")
    if twitter:
        contact_items.append(f"<strong>Twitter:</strong> <a href='{twitter}' target='_blank'>{twitter}</a>")
    
    contact_html = "<br>".join(contact_items) if contact_items else "<p>Add your contact information to let people reach you!</p>"
    
    # Build the full HTML matching original template structure exactly
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{name} - Portfolio</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
        <style>
        {css_src}
        </style>
    </head>
    <body>
        <!-- Header / Navigation -->
        <header>
            <nav>
                <h1 class="logo">{name}</h1>
                <ul class="nav-links">
                    <li><a href="#home">Home</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#education">Education</a></li>
                    <li><a href="#experience">Experience</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </nav>
        </header>

        <!-- Hero Section (Home) -->
        <section id="home">
            <div class="container">
                <h1>Hello, I'm {name}</h1>
                <p>A Passionate {role}</p>
                <a href="#about" class="cta-button">View My Work</a>
            </div>
        </section>

        <!-- About Section -->
        <section id="about">
            <div class="container">
                <h2>About Me</h2>
                <p>{bio}</p>
                {skills_html}
            </div>
        </section>

        <!-- Education Section -->
        <section id="education">
            <div class="container">
                <h2>Education</h2>
                {education_html}
            </div>
        </section>

        <!-- Experience Section -->
        <section id="experience">
            <div class="container">
                <h2>Experience</h2>
                {experience_html}
            </div>
        </section>

        <!-- Projects Section -->
        <section id="projects">
            <div class="container">
                <h2>Projects</h2>
                {projects_html}
            </div>
        </section>

        <!-- Contact Section -->
        <section id="contact">
            <div class="container">
                <h2>Get In Touch</h2>
                <p>I'm currently open to new opportunities. Feel free to reach out!</p>
                <div style="margin-top:2rem; font-size:1rem; line-height:2;">
                {contact_html}
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer>
            <p>&copy; 2025 {name}. All rights reserved.</p>
        </footer>

        <script>
        {js_src}
        </script>
    </body>
    </html>
    """
    return html



# ---------- Main page ----------

def show():
    st.title("Portfolio Builder")

    # Initialize session state early
    if "portfolio_data" not in st.session_state:
        st.session_state["portfolio_data"] = PortfolioData()

    # Sidebar for sections
    section = st.sidebar.radio(
        "Portfolio Sections",
        ["Personal Information", "About Me", "Experience", "Education", "Projects", "Contact"]
    )

    if section == "Personal Information":
        personal_info_section()
    elif section == "About Me":
        about_section()
    elif section == "Experience":
        experience_section()
    elif section == "Education":
        education_section()
    elif section == "Projects":
        projects_section()
    elif section == "Contact":
        contact_section()

    # Preview and export options
    st.sidebar.markdown("---")
    st.sidebar.subheader("Actions")
    if st.sidebar.button("🔍 Preview Portfolio", key="btn_preview_portfolio", use_container_width=True):
        st.subheader("Live Preview")
    
        # Resolve paths relative to this file
        base_dir = Path(__file__).resolve().parent
        css_path = base_dir / "portfolio.css"
        js_path = base_dir / "portfolio.js"

        # Check existence
        if not css_path.exists():
            st.error(f"{css_path.name} not found at {css_path}. Place it next to portfolio_builder.py.")
            return
        if not js_path.exists():
            st.error(f"{js_path.name} not found at {js_path}. Place it next to portfolio_builder.py.")
            return

        with open(css_path, "r", encoding="utf-8") as f:
            css_src = f.read()
        with open(js_path, "r", encoding="utf-8") as f:
            js_src = f.read()

        # Build HTML from live data
        pdata = st.session_state["portfolio_data"]
        portfolio_html = build_portfolio_from_data(pdata, css_src, js_src)

        # Render via iframe
        components.html(portfolio_html, height=1400, scrolling=True)

    if st.sidebar.button("📥 Export Portfolio", key="btn_export_portfolio", use_container_width=True):
    # portfolio_html = build_portfolio_from_data(st.session_state["portfolio_data"], css_src, js_src)
    
            # Resolve paths relative to this file
        base_dir = Path(__file__).resolve().parent
        css_path = base_dir / "portfolio.css"
        js_path = base_dir / "portfolio.js"

    # Check existence
        if not css_path.exists():
            st.error(f"{css_path.name} not found at {css_path}. Place it next to portfolio_builder.py.")
            return
        if not js_path.exists():
            st.error(f"{js_path.name} not found at {js_path}. Place it next to portfolio_builder.py.")
            return

        with open(css_path, "r", encoding="utf-8") as f:
            css_src = f.read()
        with open(js_path, "r", encoding="utf-8") as f:
            js_src = f.read()

        # Build HTML from latest data
        pdata = st.session_state["portfolio_data"]
        portfolio_html = build_portfolio_from_data(pdata, css_src, js_src)

        st.sidebar.download_button(
            label="Download HTML",
            data=portfolio_html,
            file_name="portfolio.html",
            mime="text/html"
        )

# ---------- Sections (keep as-is from your current code) ----------

def personal_info_section():
    if "portfolio_data" not in st.session_state:
        st.session_state["portfolio_data"] = PortfolioData()

    st.subheader("Personal Information")
    portfolio_data = st.session_state["portfolio_data"].personal_info

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", portfolio_data.name)
        role = st.text_input("Professional Role", portfolio_data.role)
    with col2:
        introduction = st.text_area("Introduction", portfolio_data.introduction, height=100)

    if st.button("Save Personal Information", key="btn_save_personal"):
        st.session_state["portfolio_data"].personal_info = PersonalInfo(
            name=name,
            role=role,
            introduction=introduction
        )
        st.success("Personal information saved!")


def about_section():
    if "portfolio_data" not in st.session_state:
        st.session_state["portfolio_data"] = PortfolioData()

    st.subheader("About Me")
    portfolio_data = st.session_state["portfolio_data"].about_me

    biography = st.text_area(
        "Tell your story",
        portfolio_data.biography,
        height=300,
        help="Write a compelling bio."
    )

    st.subheader("Skills & Interests")
    if portfolio_data.skills:
        st.write("Current Skills:")
        for i, skill_obj in enumerate(portfolio_data.skills):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.write(skill_obj.name)
            with col2:
                if st.button("Remove", key=f"remove_skill_{i}"):
                    portfolio_data.skills.pop(i)
                    st.session_state["portfolio_data"].about_me = portfolio_data
                    st.rerun()

    new_skill_name = st.text_input("New Skill", key="new_portfolio_skill_name")
    if st.button("Add Skill", key="btn_add_skill"):
        if new_skill_name:
            portfolio_data.skills.append(Skill(name=new_skill_name))
            st.session_state["portfolio_data"].about_me = portfolio_data
            st.success(f"Added {new_skill_name}!")
            st.rerun()

    if st.button("Save About Me", key="btn_save_about"):
        st.session_state["portfolio_data"].about_me.biography = biography
        st.success("About Me saved!")


def experience_section():
    if "portfolio_data" not in st.session_state:
        st.session_state["portfolio_data"] = PortfolioData()

    st.subheader("Experience")
    portfolio_data = st.session_state["portfolio_data"].experience

    for i, exp in enumerate(portfolio_data):
        with st.expander(f"{exp.role} at {exp.company}"):
            st.write(f"**Company:** {exp.company}")
            st.write(f"**Role:** {exp.role}")
            st.write(f"**Years:** {exp.years}")
            st.write(f"**Description:** {exp.description}")
            if st.button("Remove", key=f"remove_exp_{i}"):
                portfolio_data.pop(i)
                st.session_state["portfolio_data"].experience = portfolio_data
                st.rerun()

    with st.expander("Add New Experience"):
        new_company = st.text_input("Company", key="new_exp_company")
        new_role = st.text_input("Role", key="new_exp_role")
        new_years = st.text_input("Years (e.g., 2020-2023)", key="new_exp_years")
        new_description = st.text_area("Description", key="new_exp_description")
        if st.button("Add Experience", key="btn_add_experience"):
            if new_company and new_role and new_years and new_description:
                portfolio_data.append(Experience(company=new_company, role=new_role, years=new_years, description=new_description))
                st.session_state["portfolio_data"].experience = portfolio_data
                st.success("Experience added!")
                st.rerun()


def education_section():
    if "portfolio_data" not in st.session_state:
        st.session_state["portfolio_data"] = PortfolioData()

    st.subheader("Education")
    portfolio_data = st.session_state["portfolio_data"].education

    for i, edu in enumerate(portfolio_data):
        with st.expander(f"{edu.degree} from {edu.institution}"):
            st.write(f"**Degree:** {edu.degree}")
            st.write(f"**Institution:** {edu.institution}")
            st.write(f"**Years:** {edu.years}")
            if st.button("Remove", key=f"remove_edu_{i}"):
                portfolio_data.pop(i)
                st.session_state["portfolio_data"].education = portfolio_data
                st.rerun()

    with st.expander("Add New Education"):
        new_degree = st.text_input("Degree", key="new_edu_degree")
        new_institution = st.text_input("Institution", key="new_edu_institution")
        new_years = st.text_input("Years (e.g., 2016-2020)", key="new_edu_years")
        if st.button("Add Education", key="btn_add_education"):
            if new_degree and new_institution and new_years:
                portfolio_data.append(Education(degree=new_degree, institution=new_institution, years=new_years))
                st.session_state["portfolio_data"].education = portfolio_data
                st.success("Education added!")
                st.rerun()


def projects_section():
    if "portfolio_data" not in st.session_state:
        st.session_state["portfolio_data"] = PortfolioData()

    st.subheader("Projects")
    portfolio_data = st.session_state["portfolio_data"].projects

    for i, proj in enumerate(portfolio_data):
        with st.expander(f"{proj.title}"):
            st.write(f"**Project Title:** {proj.title}")
            st.write(f"**Description:** {proj.description}")
            if proj.link:
                st.write(f"**Project Link:** {proj.link}")
            if st.button("Remove", key=f"remove_portfolio_proj_{i}"):
                portfolio_data.pop(i)
                st.session_state["portfolio_data"].projects = portfolio_data
                st.rerun()

    with st.expander("Add Project"):
        title = st.text_input("Project Title", key="new_portfolio_proj_title")
        description = st.text_area("Project Description", key="new_portfolio_proj_desc")
        link = st.text_input("Project URL", key="new_portfolio_proj_url")

        if st.button("Add Project", key="btn_add_project"):
            if title and description:
                portfolio_data.append(Project(title=title, description=description, link=link))
                st.session_state["portfolio_data"].projects = portfolio_data
                st.success("Project added!")
                st.rerun()


def contact_section():
    if "portfolio_data" not in st.session_state:
        st.session_state["portfolio_data"] = PortfolioData()

    st.subheader("Contact Information")
    portfolio_data = st.session_state["portfolio_data"].contact

    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Email", portfolio_data.email)
        phone = st.text_input("Phone", portfolio_data.phone)
    with col2:
        linkedin = st.text_input("LinkedIn", portfolio_data.linkedin)
        github = st.text_input("GitHub", portfolio_data.github)
        twitter = st.text_input("Twitter", portfolio_data.twitter)

    if st.button("Save Contact Information", key="btn_save_contact"):
        st.session_state["portfolio_data"].contact = Contact(
            email=email,
            phone=phone,
            linkedin=linkedin,
            github=github,
            twitter=twitter
        )
        st.success("Contact information saved!")
