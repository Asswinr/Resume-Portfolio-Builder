# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

def show():
    st.title("Resume Builder")
    
    # Initialize session state for resume data
    if "resume_data" not in st.session_state:
        st.session_state["resume_data"] = {
            "personal_info": {},
            "education": [],
            "experience": [],
            "skills": [],
            "projects": []
        }
    
    # Sidebar for sections
    section = st.sidebar.radio(
        "Resume Sections",
        ["Personal Information", "Education", "Experience", "Skills", "Projects"]
    )
    
    if section == "Personal Information":
        personal_info_section()
    elif section == "Education":
        education_section()
    elif section == "Experience":
        experience_section()
    elif section == "Skills":
        skills_section()
    elif section == "Projects":
        projects_section()
    
    # Preview and export options
    st.sidebar.divider()
    if st.sidebar.button("Preview Resume"):
        preview_resume()
    
    if st.sidebar.button("Export Resume"):
        # This will be implemented in the export functionality task
        st.sidebar.success("Export functionality will be implemented soon!")

def personal_info_section():
    st.subheader("Personal Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name", st.session_state["resume_data"]["personal_info"].get("name", ""))
        email = st.text_input("Email", st.session_state["resume_data"]["personal_info"].get("email", ""))
        phone = st.text_input("Phone", st.session_state["resume_data"]["personal_info"].get("phone", ""))
    
    with col2:
        location = st.text_input("Location", st.session_state["resume_data"]["personal_info"].get("location", ""))
        linkedin = st.text_input("LinkedIn", st.session_state["resume_data"]["personal_info"].get("linkedin", ""))
        website = st.text_input("Website/Portfolio", st.session_state["resume_data"]["personal_info"].get("website", ""))
    
    summary = st.text_area("Professional Summary", st.session_state["resume_data"]["personal_info"].get("summary", ""), height=150)
    
    if st.button("Save Personal Information"):
        st.session_state["resume_data"]["personal_info"] = {
            "name": name,
            "email": email,
            "phone": phone,
            "location": location,
            "linkedin": linkedin,
            "website": website,
            "summary": summary
        }
        st.success("Personal information saved!")

def education_section():
    st.subheader("Education")
    
    # Display existing education entries
    for i, edu in enumerate(st.session_state["resume_data"]["education"]):
        with st.expander(f"{edu.get('degree', 'Education')} - {edu.get('institution', '')}"):
            st.write(f"**Degree:** {edu.get('degree', '')}")
            st.write(f"**Institution:** {edu.get('institution', '')}")
            st.write(f"**Location:** {edu.get('location', '')}")
            st.write(f"**Period:** {edu.get('start_date', '')} - {edu.get('end_date', '')}")
            st.write(f"**GPA:** {edu.get('gpa', '')}")
            st.write(f"**Description:** {edu.get('description', '')}")
            
            if st.button("Remove", key=f"remove_edu_{i}"):
                st.session_state["resume_data"]["education"].pop(i)
                st.experimental_rerun()
    
    # Add new education entry
    with st.expander("Add Education"):
        col1, col2 = st.columns(2)
        
        with col1:
            degree = st.text_input("Degree/Certificate", key="new_edu_degree")
            institution = st.text_input("Institution", key="new_edu_institution")
            location = st.text_input("Location", key="new_edu_location")
        
        with col2:
            start_date = st.text_input("Start Date", key="new_edu_start")
            end_date = st.text_input("End Date (or 'Present')", key="new_edu_end")
            gpa = st.text_input("GPA (optional)", key="new_edu_gpa")
        
        description = st.text_area("Description/Achievements", key="new_edu_desc")
        
        if st.button("Add Education"):
            st.session_state["resume_data"]["education"].append({
                "degree": degree,
                "institution": institution,
                "location": location,
                "start_date": start_date,
                "end_date": end_date,
                "gpa": gpa,
                "description": description
            })
            st.success("Education added!")
            st.experimental_rerun()

def experience_section():
    st.subheader("Work Experience")
    
    # Display existing experience entries
    for i, exp in enumerate(st.session_state["resume_data"]["experience"]):
        with st.expander(f"{exp.get('title', 'Position')} at {exp.get('company', '')}"):
            st.write(f"**Title:** {exp.get('title', '')}")
            st.write(f"**Company:** {exp.get('company', '')}")
            st.write(f"**Location:** {exp.get('location', '')}")
            st.write(f"**Period:** {exp.get('start_date', '')} - {exp.get('end_date', '')}")
            st.write(f"**Description:**")
            st.write(exp.get('description', ''))
            
            if st.button("Remove", key=f"remove_exp_{i}"):
                st.session_state["resume_data"]["experience"].pop(i)
                st.experimental_rerun()
    
    # Add new experience entry
    with st.expander("Add Experience"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Job Title", key="new_exp_title")
            company = st.text_input("Company", key="new_exp_company")
            location = st.text_input("Location", key="new_exp_location")
        
        with col2:
            start_date = st.text_input("Start Date", key="new_exp_start")
            end_date = st.text_input("End Date (or 'Present')", key="new_exp_end")
        
        description = st.text_area("Description/Achievements", key="new_exp_desc", 
                                 help="Use bullet points for better readability")
        
        if st.button("Add Experience"):
            st.session_state["resume_data"]["experience"].append({
                "title": title,
                "company": company,
                "location": location,
                "start_date": start_date,
                "end_date": end_date,
                "description": description
            })
            st.success("Experience added!")
            st.experimental_rerun()

def skills_section():
    st.subheader("Skills")
    
    # Display existing skills
    if st.session_state["resume_data"]["skills"]:
        st.write("Current Skills:")
        skills_df = pd.DataFrame(st.session_state["resume_data"]["skills"])
        st.dataframe(skills_df)
        
        if st.button("Clear All Skills"):
            st.session_state["resume_data"]["skills"] = []
            st.experimental_rerun()
    
    # Add new skills
    st.write("Add Skills:")
    col1, col2 = st.columns(2)
    
    with col1:
        skill = st.text_input("Skill Name")
    
    with col2:
        proficiency = st.select_slider(
            "Proficiency",
            options=["Beginner", "Intermediate", "Advanced", "Expert"]
        )
    
    category = st.selectbox(
        "Category",
        ["Technical", "Soft Skills", "Languages", "Tools", "Other"]
    )
    
    if st.button("Add Skill"):
        st.session_state["resume_data"]["skills"].append({
            "skill": skill,
            "proficiency": proficiency,
            "category": category
        })
        st.success(f"Added {skill} to your skills!")
        st.experimental_rerun()

def projects_section():
    st.subheader("Projects")
    
    # Display existing projects
    for i, proj in enumerate(st.session_state["resume_data"]["projects"]):
        with st.expander(f"{proj.get('name', 'Project')}"):
            st.write(f"**Project Name:** {proj.get('name', '')}")
            st.write(f"**Role:** {proj.get('role', '')}")
            st.write(f"**Period:** {proj.get('period', '')}")
            st.write(f"**Description:**")
            st.write(proj.get('description', ''))
            st.write(f"**Technologies:** {proj.get('technologies', '')}")
            st.write(f"**Link:** {proj.get('link', '')}")
            
            if st.button("Remove", key=f"remove_proj_{i}"):
                st.session_state["resume_data"]["projects"].pop(i)
                st.experimental_rerun()
    
    # Add new project
    with st.expander("Add Project"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Project Name", key="new_proj_name")
            role = st.text_input("Your Role", key="new_proj_role")
        
        with col2:
            period = st.text_input("Time Period", key="new_proj_period")
            technologies = st.text_input("Technologies Used", key="new_proj_tech")
        
        description = st.text_area("Project Description", key="new_proj_desc")
        link = st.text_input("Project Link (if any)", key="new_proj_link")
        
        if st.button("Add Project"):
            st.session_state["resume_data"]["projects"].append({
                "name": name,
                "role": role,
                "period": period,
                "description": description,
                "technologies": technologies,
                "link": link
            })
            st.success("Project added!")
            st.experimental_rerun()

def preview_resume():
    st.header("Resume Preview")
    
    # Personal Information
    personal = st.session_state["resume_data"]["personal_info"]
    if personal:
        st.subheader(personal.get("name", "Your Name"))
        contact_info = []
        if personal.get("email"): contact_info.append(f"📧 {personal['email']}")
        if personal.get("phone"): contact_info.append(f"📱 {personal['phone']}")
        if personal.get("location"): contact_info.append(f"📍 {personal['location']}")
        if personal.get("linkedin"): contact_info.append(f"🔗 {personal['linkedin']}")
        if personal.get("website"): contact_info.append(f"🌐 {personal['website']}")
        
        st.write(" | ".join(contact_info))
        
        if personal.get("summary"):
            st.write("### Summary")
            st.write(personal["summary"])
    
    # Education
    if st.session_state["resume_data"]["education"]:
        st.write("### Education")
        for edu in st.session_state["resume_data"]["education"]:
            st.write(f"**{edu.get('degree', '')}** - {edu.get('institution', '')}")
            st.write(f"*{edu.get('start_date', '')} - {edu.get('end_date', '')}* | {edu.get('location', '')}")
            if edu.get('gpa'): st.write(f"GPA: {edu['gpa']}")
            if edu.get('description'): st.write(edu['description'])
            st.write("---")
    
    # Experience
    if st.session_state["resume_data"]["experience"]:
        st.write("### Work Experience")
        for exp in st.session_state["resume_data"]["experience"]:
            st.write(f"**{exp.get('title', '')}** - {exp.get('company', '')}")
            st.write(f"*{exp.get('start_date', '')} - {exp.get('end_date', '')}* | {exp.get('location', '')}")
            if exp.get('description'): st.write(exp['description'])
            st.write("---")
    
    # Skills
    if st.session_state["resume_data"]["skills"]:
        st.write("### Skills")
        skills_by_category = {}
        for skill in st.session_state["resume_data"]["skills"]:
            category = skill.get("category", "Other")
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(f"{skill.get('skill', '')} ({skill.get('proficiency', '')})")
        
        for category, skills in skills_by_category.items():
            st.write(f"**{category}:** {', '.join(skills)}")
    
    # Projects
    if st.session_state["resume_data"]["projects"]:
        st.write("### Projects")
        for proj in st.session_state["resume_data"]["projects"]:
            st.write(f"**{proj.get('name', '')}** - {proj.get('role', '')}")
            st.write(f"*{proj.get('period', '')}*")
            if proj.get('description'): st.write(proj['description'])
            if proj.get('technologies'): st.write(f"**Technologies:** {proj['technologies']}")
            if proj.get('link'): st.write(f"**Link:** {proj['link']}")
            st.write("---")