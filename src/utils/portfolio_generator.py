"""
Portfolio Generator Module
Generates HTML portfolio from user data using template-based approach
"""
from typing import List
from dataclasses import asdict
from pathlib import Path
from src.data.portfolio_data import PortfolioData, PersonalInfo, Skill, AboutMe, Experience, Education, Project, Contact

# Import the advanced template-based generator
from .advanced_portfolio_generator import generate_portfolio_html as generate_template_portfolio


def generate_portfolio_html(portfolio_data: PortfolioData) -> str:
    """
    Generate complete portfolio HTML from portfolio data using template approach
    """
    # Convert portfolio data to dictionary format for template
    portfolio_dict = {
        "personal_info": asdict(portfolio_data.personal_info),
        "about_me": {
            "biography": portfolio_data.about_me.biography,
            "skills": [asdict(skill) for skill in portfolio_data.about_me.skills]
        },
        "education": [asdict(edu) for edu in portfolio_data.education],
        "experience": [asdict(exp) for exp in portfolio_data.experience],
        "projects": [asdict(proj) for proj in portfolio_data.projects],
        "contact": asdict(portfolio_data.contact)
    }
    
    # Generate HTML using template-based approach
    return generate_template_portfolio(portfolio_dict)


def save_portfolio_to_file(portfolio_data: PortfolioData, output_path: str) -> None:
    """
    Generate portfolio HTML and save to file
    """
    html_content = generate_portfolio_html(portfolio_data)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def get_sample_portfolio_data() -> PortfolioData:
    """
    Get sample portfolio data for testing
    """
    return PortfolioData(
        personal_info=PersonalInfo(
            name="John Doe",
            role="Full Stack Developer",
            location="San Francisco, CA"
        ),
        about_me=AboutMe(
            biography="Passionate developer with 5+ years of experience in building scalable web applications. Specialized in Python, JavaScript, and cloud technologies.",
            skills=[
                Skill(name="Python", level="Expert"),
                Skill(name="JavaScript", level="Expert"),
                Skill(name="React", level="Advanced"),
                Skill(name="Node.js", level="Advanced"),
                Skill(name="AWS", level="Intermediate"),
                Skill(name="Docker", level="Intermediate")
            ]
        ),
        education=[
            Education(
                degree="Bachelor of Science in Computer Science",
                institution="University of Technology",
                period="2015-2019",
                description="Graduated with honors. Focused on software engineering and algorithms.",
                gpa="3.8"
            ),
            Education(
                degree="Master of Science in Data Science",
                institution="Tech Institute",
                period="2019-2021",
                description="Specialized in machine learning and big data technologies.",
                gpa="3.9"
            )
        ],
        experience=[
            Experience(
                position="Senior Developer",
                company="Tech Corp",
                period="2020-Present",
                description="Leading development of enterprise-scale applications",
                responsibilities=[
                    "Team leadership and mentorship",
                    "Architecture design and implementation",
                    "Code reviews and quality assurance",
                    "Agile project management"
                ]
            ),
            Experience(
                position="Software Engineer",
                company="Startup Inc",
                period="2019-2020",
                description="Full-stack development for early-stage startup",
                responsibilities=[
                    "Frontend development with React",
                    "Backend development with Node.js",
                    "Database design and optimization",
                    "DevOps and deployment"
                ]
            )
        ],
        projects=[
            Project(
                name="E-commerce Platform",
                description="Full-stack e-commerce solution with payment integration",
                technologies=["React", "Node.js", "MongoDB", "Stripe"],
                github_url="https://github.com/johndoe/ecommerce",
                live_url="https://ecommerce.example.com"
            ),
            Project(
                name="Task Management App",
                description="Collaborative task management application",
                technologies=["Vue.js", "Python", "PostgreSQL", "Docker"],
                github_url="https://github.com/johndoe/taskmanager",
                live_url="https://taskmanager.example.com"
            )
        ],
        contact=Contact(
            email="john.doe@example.com",
            phone="+1-555-0123",
            linkedin="https://linkedin.com/in/johndoe",
            github="https://github.com/johndoe",
            twitter="https://twitter.com/johndoe"
        )
    )