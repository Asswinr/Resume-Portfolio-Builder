# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from src.data.portfolio_data import PortfolioData, PersonalInfo, AboutMe, Experience, Education, Project, Contact, Skill
from src.utils.portfolio_generator import generate_portfolio_html

def show():
    st.title("Portfolio Builder")

    # Initialize session state for portfolio data
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
    st.sidebar.subheader("Customization")
    primary_color = st.sidebar.color_picker("Select Primary Color", "#0056b3")
    st.session_state["portfolio_data"].custom_css = f"h1, h2, h3, .project-item a, .contact-info a {{ color: {primary_color}; }}"
    if st.sidebar.button("Preview Portfolio"):
        st.subheader("Live Preview")
        portfolio_html = generate_portfolio_html(st.session_state["portfolio_data"])
        # Render portfolio preview correctly
        components.html(portfolio_html, height=800, scrolling=True)

    if st.sidebar.button("Export Portfolio"):
        # This will be implemented in the export functionality task
        st.sidebar.success("Export functionality will be implemented soon!")

def personal_info_section():
    st.subheader("Personal Information")
    
    portfolio_data = st.session_state["portfolio_data"].personal_info
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name", portfolio_data.name)
        role = st.text_input("Professional Role", portfolio_data.role)
    
    with col2:
        introduction = st.text_area("Introduction", portfolio_data.introduction, height=100)
        # photo = st.file_uploader("Profile Photo", type=["jpg", "jpeg", "png"])
    
    if st.button("Save Personal Information"):
        st.session_state["portfolio_data"].personal_info = PersonalInfo(
            name=name,
            role=role,
            introduction=introduction
        )
        st.success("Personal information saved!")

def about_section():
    st.subheader("About Me")
    
    portfolio_data = st.session_state["portfolio_data"].about_me
    
    biography = st.text_area(
        "Tell your story",
        portfolio_data.biography,
        height=300,
        help="Write a compelling bio that highlights your journey, values, and what makes you unique."
    )
    
    st.subheader("Skills & Interests")
    
    # Display existing skills
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
    
    # Add new skill
    new_skill_name = st.text_input("New Skill", key="new_portfolio_skill_name")
    if st.button("Add Skill"):
        if new_skill_name:
            portfolio_data.skills.append(Skill(name=new_skill_name))
            st.session_state["portfolio_data"].about_me = portfolio_data
            st.success(f"Added {new_skill_name} to your skills!")
            st.rerun()
    
    if st.button("Save About Me"):
        st.session_state["portfolio_data"].about_me.biography = biography
        st.success("About Me section saved!")

def experience_section():
    st.subheader("Experience")

    portfolio_data = st.session_state["portfolio_data"].experience

    # Display existing experiences
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

    # Add new experience
    with st.expander("Add New Experience"):
        new_company = st.text_input("Company", key="new_exp_company")
        new_role = st.text_input("Role", key="new_exp_role")
        new_years = st.text_input("Years (e.g., 2020-2023)", key="new_exp_years")
        new_description = st.text_area("Description", key="new_exp_description")
        if st.button("Add Experience"):
            if new_company and new_role and new_years and new_description:
                portfolio_data.append(Experience(company=new_company, role=new_role, years=new_years, description=new_description))
                st.session_state["portfolio_data"].experience = portfolio_data
                st.success("Experience added!")
                st.rerun()

def education_section():
    st.subheader("Education")

    portfolio_data = st.session_state["portfolio_data"].education

    # Display existing education entries
    for i, edu in enumerate(portfolio_data):
        with st.expander(f"{edu.degree} from {edu.institution}"):
            st.write(f"**Degree:** {edu.degree}")
            st.write(f"**Institution:** {edu.institution}")
            st.write(f"**Years:** {edu.years}")
            if st.button("Remove", key=f"remove_edu_{i}"):
                portfolio_data.pop(i)
                st.session_state["portfolio_data"].education = portfolio_data
                st.rerun()

    # Add new education
    with st.expander("Add New Education"):
        new_degree = st.text_input("Degree", key="new_edu_degree")
        new_institution = st.text_input("Institution", key="new_edu_institution")
        new_years = st.text_input("Years (e.g., 2016-2020)", key="new_edu_years")
        if st.button("Add Education"):
            if new_degree and new_institution and new_years:
                portfolio_data.append(Education(degree=new_degree, institution=new_institution, years=new_years))
                st.session_state["portfolio_data"].education = portfolio_data
                st.success("Education added!")
                st.rerun()

def projects_section():
    st.subheader("Projects")
    
    portfolio_data = st.session_state["portfolio_data"].projects
    
    # Display existing projects
    for i, proj in enumerate(portfolio_data):
        with st.expander(f"{proj.title}"):
            st.write(f"**Project Title:** {proj.title}")
            st.write(f"**Description:**")
            st.write(proj.description)
            if proj.link:
                st.write(f"**Project Link:** {proj.link}")
            
            if st.button("Remove", key=f"remove_portfolio_proj_{i}"):
                portfolio_data.pop(i)
                st.session_state["portfolio_data"].projects = portfolio_data
                st.rerun()
    
    # Add new project
    with st.expander("Add Project"):
        title = st.text_input("Project Title", key="new_portfolio_proj_title")
        description = st.text_area("Project Description", key="new_portfolio_proj_desc")
        link = st.text_input("Project URL", key="new_portfolio_proj_url")
        
        if st.button("Add Project"):
            if title and description:
                portfolio_data.append(Project(title=title, description=description, link=link))
                st.session_state["portfolio_data"].projects = portfolio_data
                st.success("Project added!")
                st.rerun()

def contact_section():
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
    
    if st.button("Save Contact Information"):
        st.session_state["portfolio_data"].contact = Contact(
            email=email,
            phone=phone,
            linkedin=linkedin,
            github=github,
            twitter=twitter
        )
        st.success("Contact information saved!")


def upload_resume_section():
    st.subheader("Upload Resume for Portfolio Creation")

    uploaded_file = st.file_uploader("Upload your resume (PDF or JSON format)", type=["pdf", "json"])

    if uploaded_file:
        st.info("This feature is under development. Uploaded file will not be processed yet.")