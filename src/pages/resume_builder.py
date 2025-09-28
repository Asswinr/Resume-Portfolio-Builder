# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import requests # We'll need this to communicate with our Flask backend

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

    # --- AI Suggestion Button for Summary ---
    st.subheader("AI Suggestions for Summary")
    if st.button("Get AI Suggestions for Summary"):
        if summary:
            st.info("Getting AI suggestions for your summary...")
            # Prepare the data to send to the Flask backend
            payload = {
                "prompt": f"Generate a concise, professional, and improved resume summary (2-4 sentences) based on the following text, without any additional explanations or formatting instructions: '{summary}'"
            }
            try:
                # Make a POST request to our Flask AI endpoint
                response = requests.post("http://127.0.0.1:5000/ai/generate-content", json=payload)
                if response.status_code == 200:
                    ai_response = response.json()
                    st.subheader("AI Suggested Summary:")
                    st.write(ai_response.get("generated_content", "No suggestions found."))
                else:
                    st.error(f"Error from AI service: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the Flask backend. Is it running?")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
        else:
            st.warning("Please enter a summary to get AI suggestions.")


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
                st.rerun()
    
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
            st.rerun()

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
                st.rerun()
    
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
            st.rerun()

def skills_section():
    st.subheader("Skills")
    
    # Display existing skills
    if st.session_state["resume_data"]["skills"]:
        st.write("Current Skills:")
        skills_df = pd.DataFrame(st.session_state["resume_data"]["skills"])
        st.dataframe(skills_df)
        
        if st.button("Clear All Skills"):
            st.session_state["resume_data"]["skills"] = []
            st.rerun()
    
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
        st.rerun()

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
                st.rerun()
    
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
            st.rerun()

def preview_resume():
    st.subheader("Resume Preview")

    personal = st.session_state["resume_data"]["personal_info"]
    education_entries = st.session_state["resume_data"]["education"]
    experience_entries = st.session_state["resume_data"]["experience"]
    skills_entries = st.session_state["resume_data"]["skills"]
    projects_entries = st.session_state["resume_data"]["projects"]

    # --- Custom CSS for styling ---
    st.markdown("""
        <style>
        .resume-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header-name {
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            margin-bottom: 5px;
            color: #2c3e50;
        }
        .header-title {
            font-size: 1.2em;
            text-align: center;
            margin-bottom: 15px;
            color: #555;
        }
        .contact-info {
            text-align: center;
            font-size: 0.9em;
            color: #777;
            margin-bottom: 20px;
            border-bottom: 1px solid #eee;
            padding-bottom: 15px;
        }
        .section-header {
            font-size: 1.3em;
            font-weight: bold;
            margin-top: 25px;
            margin-bottom: 10px;
            color: #2c3e50;
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 5px;
            text-transform: uppercase;
        }
        .item-title {
            font-weight: bold;
            font-size: 1.1em;
            color: #34495e;
        }
        .item-subtitle {
            font-style: italic;
            color: #555;
        }
        .item-dates {
            text-align: right;
            font-size: 0.9em;
            color: #777;
        }
        .bullet-point {
            margin-left: 20px;
            list-style-type: disc;
        }
        .skill-category {
            font-weight: bold;
            margin-top: 10px;
            margin-bottom: 5px;
        }
        .skills-list {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 10px;
        }
        .skill-item {
            background-color: #ecf0f1;
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 0.9em;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="resume-container">', unsafe_allow_html=True)

    # --- Name and Title ---
    if personal.get("name"):
        st.markdown(f'<p class="header-name">{personal["name"]}</p>', unsafe_allow_html=True)
    if personal.get("title"): # Assuming you might add a title field later
        st.markdown(f'<p class="header-title">{personal["title"]}</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="header-title">Your Professional Title</p>', unsafe_allow_html=True)


    # --- Contact Information ---
    contact_parts = []
    if personal.get("location"): contact_parts.append(f'{personal["location"]}')
    if personal.get("phone"): contact_parts.append(f'{personal["phone"]}')
    if personal.get("email"): contact_parts.append(f'{personal["email"]}')
    if personal.get("website"): contact_parts.append(f'<a href="{personal["website"]}" target="_blank">{personal["website"]}</a>')
    if personal.get("linkedin"): contact_parts.append(f'<a href="{personal["linkedin"]}" target="_blank">LinkedIn</a>')

    if contact_parts:
        st.markdown(f'<p class="contact-info">{" | ".join(contact_parts)}</p>', unsafe_allow_html=True)

    # --- Professional Summary ---
    if personal.get("summary"):
        st.markdown('<p class="section-header">Professional Summary</p>', unsafe_allow_html=True)
        st.write(personal["summary"])

    # --- Work Experience ---
    if experience_entries:
        st.markdown('<p class="section-header">Work Experience</p>', unsafe_allow_html=True)
        for exp in experience_entries:
            col_exp_left, col_exp_right = st.columns([3, 1])
            with col_exp_left:
                st.markdown(f'<p class="item-title">{exp.get("title", "")} at {exp.get("company", "")}</p>', unsafe_allow_html=True)
                if exp.get("location"):
                    st.markdown(f'<p class="item-subtitle">{exp.get("location", "")}</p>', unsafe_allow_html=True)
            with col_exp_right:
                st.markdown(f'<p class="item-dates">{exp.get("start_date", "")} - {exp.get("end_date", "")}</p>', unsafe_allow_html=True)
            if exp.get("description"):
                # Assuming description is a single string, split by lines for bullet points
                description_lines = exp["description"].split('\n')
                for line in description_lines:
                    if line.strip(): # Only add non-empty lines
                        st.markdown(f'<li class="bullet-point">{line.strip()}</li>', unsafe_allow_html=True)
            st.markdown("---") # Small divider between experiences

    # --- Education ---
    if education_entries:
        st.markdown('<p class="section-header">Education</p>', unsafe_allow_html=True)
        for edu in education_entries:
            col_edu_left, col_edu_right = st.columns([3, 1])
            with col_edu_left:
                st.markdown(f'<p class="item-title">{edu.get("degree", "")}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="item-subtitle">{edu.get("institution", "")}, {edu.get("location", "")}</p>', unsafe_allow_html=True)
            with col_edu_right:
                st.markdown(f'<p class="item-dates">{edu.get("start_date", "")} - {edu.get("end_date", "")}</p>', unsafe_allow_html=True)
            if edu.get("gpa"):
                st.markdown(f'<li class="bullet-point">GPA: {edu["gpa"]}</li>', unsafe_allow_html=True)
            if edu.get("description"):
                description_lines = edu["description"].split('\n')
                for line in description_lines:
                    if line.strip():
                        st.markdown(f'<li class="bullet-point">{line.strip()}</li>', unsafe_allow_html=True)
            st.markdown("---") # Small divider between education entries

    # --- Skills ---
    if skills_entries:
        st.markdown('<p class="section-header">Skills</p>', unsafe_allow_html=True)
        skills_by_category = {}
        for skill in skills_entries:
            category = skill.get("category", "Other")
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(f'{skill.get("skill", "")} ({skill.get("proficiency", "")})')

        for category, skills in skills_by_category.items():
            st.markdown(f'<p class="skill-category">{category}:</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="skills-list">{"".join([f"<span class='skill-item'>{s}</span>" for s in skills])}</div>', unsafe_allow_html=True)
        st.markdown("---")

    # --- Projects ---
    if projects_entries:
        st.markdown('<p class="section-header">Projects</p>', unsafe_allow_html=True)
        for proj in projects_entries:
            st.markdown(f'<p class="item-title">{proj.get("name", "")}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="item-subtitle">Role: {proj.get("role", "")} | Period: {proj.get("period", "")}</p>', unsafe_allow_html=True)
            if proj.get("technologies"):
                st.markdown(f'<li class="bullet-point">Technologies: {proj["technologies"]}</li>', unsafe_allow_html=True)
            if proj.get("description"):
                description_lines = proj["description"].split('\n')
                for line in description_lines:
                    if line.strip():
                        st.markdown(f'<li class="bullet-point">{line.strip()}</li>', unsafe_allow_html=True)
            if proj.get("link"):
                st.markdown(f'<li class="bullet-point">Link: <a href="{proj["link"]}" target="_blank">{proj["link"]}</a></li>', unsafe_allow_html=True)
            st.markdown("---")

    st.markdown('</div>', unsafe_allow_html=True) # Close resume-container



def resume_builder_page():
    st.title("Resume Builder")
    st.write("Enter your resume details below and get AI-powered suggestions!")

    # --- Contact Information ---
    st.header("Contact Information")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email")
    with col2:
        phone = st.text_input("Phone Number")
        linkedin = st.text_input("LinkedIn Profile URL")

    # --- Summary/Objective ---
    st.header("Summary/Objective")
    summary = st.text_area("Professional Summary or Objective", height=150)

    # --- Work Experience ---
    st.header("Work Experience")
    # We'll make this dynamic later, for now, a single entry
    job_title = st.text_input("Job Title")
    company = st.text_input("Company")
    col3, col4 = st.columns(2)
    with col3:
        start_date_exp = st.text_input("Start Date (e.g., Jan 2020)", key="exp_start")
    with col4:
        end_date_exp = st.text_input("End Date (e.g., Dec 2022 or Present)", key="exp_end")
    responsibilities = st.text_area("Key Responsibilities and Achievements (bullet points)", height=150)

    # --- Education ---
    st.header("Education")
    degree = st.text_input("Degree/Certification")
    university = st.text_input("University/Institution")
    col5, col6 = st.columns(2)
    with col5:
        start_date_edu = st.text_input("Start Date (e.g., Sep 2018)", key="edu_start")
    with col6:
        end_date_edu = st.text_input("End Date (e.g., May 2022)", key="edu_end")

    # --- Skills ---
    st.header("Skills")
    skills = st.text_area("List your skills (comma-separated)", height=100)

    # --- AI Suggestion Button ---
    st.header("AI Suggestions")
    if st.button("Get AI Suggestions for Summary"):
        if summary:
            st.info("Getting AI suggestions for your summary...")
            # Prepare the data to send to the Flask backend
            payload = {
                "prompt": f"Improve this professional summary for a resume: '{summary}'"
            }
            try:
                # Make a POST request to our Flask AI endpoint
                response = requests.post("http://127.0.0.1:5000/ai/generate-content", json=payload)
                if response.status_code == 200:
                    ai_response = response.json()
                    st.subheader("AI Suggested Summary:")
                    st.write(ai_response.get("generated_content", "No suggestions found."))
                else:
                    st.error(f"Error from AI service: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the Flask backend. Is it running?")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
        else:
            st.warning("Please enter a summary to get AI suggestions.")

# This is important for Streamlit to recognize this as a page
if __name__ == "__main__":
    resume_builder_page()