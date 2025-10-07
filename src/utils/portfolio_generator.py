import os
from pathlib import Path
from typing import List
from dataclasses import asdict
from src.data.portfolio_data import PortfolioData


def generate_portfolio_html(portfolio_data: PortfolioData) -> str:
    """
    Generates a complete HTML portfolio by injecting user data
    into the provided portfolio.html template.
    """

    # Path to your HTML template
    template_path = Path(__file__).resolve().parent.parent.parent / "frontend" / "portfolio.html"
    css_path = "portfolio.css"
    js_path = "portfolio.js"

    # Read the existing HTML template
    if not template_path.exists():
        raise FileNotFoundError(f"Portfolio template not found at {template_path}")
    html = template_path.read_text(encoding="utf-8")

    # Replace static placeholders with user data
    personal = portfolio_data.personal_info
    about = portfolio_data.about_me
    education = portfolio_data.education
    experience = portfolio_data.experience
    contact = portfolio_data.contact
    projects = portfolio_data.projects

    # ---- Replace Main Hero Section ----
    html = html.replace("Your Name", personal.name or "Your Name")
    html = html.replace("[Your Name]", personal.name or "Your Name")
    html = html.replace("[Your Profession, e.g., Web Developer]", personal.role or "Your Profession")

    # ---- About Me ----
    bio_html = about.biography or "Welcome to my portfolio!"
    skills_html = ""
    if about.skills:
        skills_html = "<ul style='margin-top:1rem;'>"
        for skill in about.skills:
            skills_html += f"<li>{skill.name}</li>"
        skills_html += "</ul>"

    html = html.replace(
        "Replace this text with a brief but engaging summary about yourself, your skills, and what drives you. "
        "Mention your key areas of expertise and what you're looking for in your career.",
        f"{bio_html}{skills_html}"
    )

    # ---- Education ----
    edu_html = ""
    for edu in education:
        edu_html += f"""
        <div class="timeline-item">
            <h3>{edu.degree}</h3>
            <h4>{edu.institution} | {edu.years}</h4>
        </div>
        """
    html = html.replace(
        """<div class="timeline">
                    <div class="timeline-item">
                        <h3>Master's Degree in Computer Science</h3>
                        <h4>University Name | 2022 - 2024</h4>
                        <p>Focused on advanced algorithms, machine learning, and software architecture. Completed a thesis on [Your Thesis Topic].</p>
                    </div>
                    <div class="timeline-item">
                        <h3>Bachelor's Degree in Information Technology</h3>
                        <h4>Another University Name | 2018 - 2022</h4>
                        <p>Gained a strong foundation in programming, database management, and web development. Graduated with honors.</p>
                    </div>
                </div>""",
        f"<div class='timeline'>{edu_html}</div>"
    )

    # ---- Experience ----
    exp_html = ""
    for exp in experience:
        exp_html += f"""
        <div class="timeline-item">
            <h3>{exp.role}</h3>
            <h4>{exp.company} | {exp.years}</h4>
            <p>{exp.description}</p>
        </div>
        """
    html = html.replace(
        """<div class="timeline">
                    <div class="timeline-item">
                        <h3>Senior Software Engineer</h3>
                        <h4>Tech Company Inc. | 2024 - Present</h4>
                        <p>Lead developer on the main product team. Responsible for architecting new features, mentoring junior developers, and improving system performance by 20%.</p>
                    </div>
                    <div class="timeline-item">
                        <h3>Junior Web Developer</h3>
                        <h4>Creative Agency | 2022 - 2024</h4>
                        <p>Developed and maintained client websites using HTML, CSS, JavaScript, and Python/Django. Collaborated with designers to create responsive and user-friendly interfaces.</p>
                    </div>
                </div>""",
        f"<div class='timeline'>{exp_html}</div>"
    )

    # ---- Projects Section ----
    if projects:
        proj_html = ""
        for proj in projects:
            proj_html += f"""
            <div class="timeline-item">
                <h3>{proj.title}</h3>
                <p>{proj.description}</p>
                {'<a href="' + proj.link + '" target="_blank">View Project</a>' if proj.link else ''}
            </div>
            """
        html = html.replace("</section>\n\n        <section id=\"contact\">", f"<div class='timeline'>{proj_html}</div>\n</section>\n\n        <section id=\"contact\">")

    # ---- Contact Info ----
    contact_links = ""
    if contact.linkedin:
        contact_links += f"<a href='{contact.linkedin}' target='_blank'>LinkedIn</a> | "
    if contact.github:
        contact_links += f"<a href='{contact.github}' target='_blank'>GitHub</a> | "
    if contact.twitter:
        contact_links += f"<a href='{contact.twitter}' target='_blank'>Twitter</a>"

    contact_html = f"""
        <p>Email: <a href='mailto:{contact.email}'>{contact.email}</a></p>
        <p>Phone: {contact.phone}</p>
        <div class="social-links">{contact_links}</div>
    """

    html = html.replace(
        """<div class="social-links">
                    <a href="#">LinkedIn</a> | <a href="#">GitHub</a> | <a href="#">Twitter</a>
                </div>""",
        contact_html
    )

    # ---- Custom Color ----
    if hasattr(portfolio_data, "custom_css") and portfolio_data.custom_css:
        css_tag = f"<style>{portfolio_data.custom_css}</style>"
        html = html.replace("</head>", f"{css_tag}</head>")

    # Return final HTML for rendering in Streamlit
    return html
