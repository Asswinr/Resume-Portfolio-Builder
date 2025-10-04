import streamlit as st

def show():
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

    # Create tabs for different sections
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

    with tabs[0]:
        personal_info_section()
    with tabs[1]:
        skills_section()
    with tabs[2]:
        achievements_section()
    with tabs[3]:
        experience_section()
    with tabs[4]:
        education_section()
    with tabs[5]:
        projects_section()
    with tabs[6]:
        additional_info_section()
    with tabs[7]:
        preview_resume()


def personal_info_section():
    st.subheader("Personal Information")
    
    # Get existing personal info or initialize empty dict
    personal_info = st.session_state["resume_data"].get("personal_info", {})
    
    # Create two columns for layout
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
    
    # Update session state
    st.session_state["resume_data"]["personal_info"] = {
        "name": name,
        "role": role,
        "email": email,
        "phone": phone,
        "location": location,
        "linkedin": linkedin,
        "website": website,
        "summary": summary
    }


def education_section():
    st.subheader("Education")
    
    # Initialize education list if not exists
    if "education" not in st.session_state["resume_data"]:
        st.session_state["resume_data"]["education"] = []
    
    # Display existing education entries
    for i, edu in enumerate(st.session_state["resume_data"]["education"]):
        with st.expander(f"Education {i+1}: {edu.get('degree', 'No Degree')} - {edu.get('institution', 'No Institution')}"):
            st.write(edu)
            if st.button("Remove", key=f"remove_education_{i}"):
                st.session_state["resume_data"]["education"].pop(i)
                st.rerun()
    
    # Add new education entry
    with st.expander("Add New Education"):
        with st.form("education_form"):
            degree = st.text_input("Degree/Certificate")
            institution = st.text_input("Institution")
            location = st.text_input("Location")
            start_date = st.text_input("Start Date (e.g., Sep 2020)")
            end_date = st.text_input("End Date (e.g., Jun 2024 or Present)")
            description = st.text_area("Description (use new lines for bullet points)")
            
            if st.form_submit_button("Add Education"):
                if degree and institution:
                    new_education = {
                        "degree": degree,
                        "institution": institution,
                        "location": location,
                        "start_date": start_date,
                        "end_date": end_date,
                        "description": description
                    }
                    st.session_state["resume_data"]["education"].append(new_education)
                    st.success("Education added!")
                    st.rerun()
                else:
                    st.warning("Please enter at least the degree and institution.")


def experience_section():
    st.subheader("Professional Experience")
    
    # Initialize experience list if not exists
    if "experience" not in st.session_state["resume_data"]:
        st.session_state["resume_data"]["experience"] = []
    
    # Display existing experience entries
    for i, exp in enumerate(st.session_state["resume_data"]["experience"]):
        with st.expander(f"Experience {i+1}: {exp.get('title', 'No Title')} at {exp.get('company', 'No Company')}"):
            st.write(exp)
            if st.button("Remove", key=f"remove_experience_{i}"):
                st.session_state["resume_data"]["experience"].pop(i)
                st.rerun()
    
    # Add new experience entry
    with st.expander("Add New Experience"):
        with st.form("experience_form"):
            title = st.text_input("Job Title")
            company = st.text_input("Company")
            location = st.text_input("Location")
            start_date = st.text_input("Start Date (e.g., Jan 2020)")
            end_date = st.text_input("End Date (e.g., Dec 2023 or Present)")
            description = st.text_area("Description (use new lines for bullet points)")
            
            if st.form_submit_button("Add Experience"):
                if title and company:
                    new_experience = {
                        "title": title,
                        "company": company,
                        "location": location,
                        "start_date": start_date,
                        "end_date": end_date,
                        "description": description
                    }
                    st.session_state["resume_data"]["experience"].append(new_experience)
                    st.success("Experience added!")
                    st.rerun()
                else:
                    st.warning("Please enter at least the job title and company.")


def skills_section():
    st.subheader("Skills & Expertise")
    
    # Initialize skills dict if not exists
    if "skills" not in st.session_state["resume_data"]:
        st.session_state["resume_data"]["skills"] = {}
    
    # Display existing skill categories
    for category in st.session_state["resume_data"]["skills"].keys():
        with st.expander(f"Category: {category}"):
            st.write(", ".join(st.session_state["resume_data"]["skills"][category]))
            if st.button("Remove Category", key=f"remove_category_{category}"):
                del st.session_state["resume_data"]["skills"][category]
                st.rerun()
    
    # Add new skill category
    with st.expander("Add New Skill Category"):
        with st.form("skills_form"):
            category = st.text_input("Category Name (e.g., Programming Languages, Tools, Soft Skills)")
            skills = st.text_area("Skills (comma-separated)")
            
            if st.form_submit_button("Add Skills"):
                if category and skills:
                    # Convert skills string to list and clean up
                    skills_list = [skill.strip() for skill in skills.split(",") if skill.strip()]
                    st.session_state["resume_data"]["skills"][category] = skills_list
                    st.success("Skills category added!")
                    st.rerun()
                else:
                    st.warning("Please enter both category name and skills.")


def projects_section():
    st.subheader("Projects")

    # Initialize projects list if not exists
    if "projects" not in st.session_state["resume_data"]:
        st.session_state["resume_data"]["projects"] = []

    # Display existing project entries
    for i, proj in enumerate(st.session_state["resume_data"]["projects"]):
        with st.expander(f"Project {i+1}: {proj.get('title', 'No Title')}"):
            st.write(proj)
            if st.button("Remove", key=f"remove_project_{i}"):
                st.session_state["resume_data"]["projects"].pop(i)
                st.rerun()

    # Add new project entry
    with st.expander("Add New Project"):
        with st.form("project_form"):
            title = st.text_input("Project Title")
            role = st.text_input("Your Role")
            period = st.text_input("Time Period (e.g., Jan 2023 - Mar 2023)")
            description = st.text_area("Description (use new lines for bullet points)")
            technologies = st.text_input("Technologies Used (comma-separated)")
            link = st.text_input("Project Link (optional)")

            if st.form_submit_button("Add Project"):
                if title and description:
                    new_project = {
                        "title": title,
                        "role": role,
                        "period": period,
                        "description": description,
                        "technologies": technologies,
                        "link": link
                    }
                    st.session_state["resume_data"]["projects"].append(new_project)
                    st.success("Project added!")
                    st.rerun()
                else:
                    st.warning("Please enter at least the project title and description.")


def achievements_section():
    st.subheader("Key Achievements")

    # Display existing achievements
    for i, achievement in enumerate(st.session_state["resume_data"]["achievements"]):
        with st.expander(f"Achievement {i+1}"):
            st.write(achievement)
            if st.button("Remove", key=f"remove_achievement_{i}"):
                st.session_state["resume_data"]["achievements"].pop(i)
                st.rerun()

    # Add new achievement entry
    with st.expander("Add New Achievement"):
        new_achievement = st.text_area("Achievement Description", key="new_achievement_desc")
        if st.button("Add Achievement"):
            if new_achievement:
                st.session_state["resume_data"]["achievements"].append(new_achievement)
                st.success("Achievement added!")
                st.rerun()
            else:
                st.warning("Please enter an achievement description.")


def preview_resume():
    st.subheader("Resume Preview")

    # Generate resume HTML
    resume_data = st.session_state["resume_data"]
    resume_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{resume_data['personal_info'].get('name', 'Resume')}</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                background: #f4f4f9;
                color: #333;
            }}
            .container {{
                width: 90%;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                text-align: center;
                padding: 50px 0;
                background: #0056b3;
                color: #fff;
                border-radius: 10px;
            }}
            .header h1 {{
                font-size: 2.5rem;
                margin: 0;
            }}
            .header h2 {{
                font-size: 1.5rem;
                margin: 10px 0;
            }}
            .section {{
                margin-bottom: 30px;
                padding: 20px;
                background: #fff;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .section h3 {{
                font-size: 1.8rem;
                margin-bottom: 15px;
                border-bottom: 2px solid #0056b3;
                display: inline-block;
            }}
            .timeline-item {{
                margin-bottom: 15px;
                padding: 10px;
                background: #f4f4f9;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .timeline-item h4 {{
                font-size: 1.2rem;
                margin: 0;
            }}
            .timeline-item p {{
                margin: 5px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{resume_data['personal_info'].get('name', 'Your Name')}</h1>
                <h2>{resume_data['personal_info'].get('role', 'Professional Role')}</h2>
                <p>{resume_data['personal_info'].get('summary', 'Professional Summary')}</p>
            </div>

            <div class="section">
                <h3>Education</h3>
                {''.join([f'<div class="timeline-item"><h4>{edu['degree']} - {edu['institution']}</h4><p>{edu['start_date']} - {edu['end_date']}</p><p>{edu['description']}</p></div>' for edu in resume_data['education']])}
            </div>

            <div class="section">
                <h3>Experience</h3>
                {''.join([f'<div class="timeline-item"><h4>{exp['title']} - {exp['company']}</h4><p>{exp['start_date']} - {exp['end_date']}</p><p>{exp['description']}</p></div>' for exp in resume_data['experience']])}
            </div>

            <div class="section">
                <h3>Skills</h3>
                {''.join([f'<div><h4>{category}</h4><p>{", ".join(skills)}</p></div>' for category, skills in resume_data['skills'].items()])}
            </div>

            <div class="section">
                <h3>Projects</h3>
                {''.join([f'<div class="timeline-item"><h4>{proj['title']}</h4><p>{proj['description']}</p>{f'<a href="{proj['link']}" target="_blank">View Project</a>' if proj['link'] else ''}</div>' for proj in resume_data['projects']])}
            </div>
        </div>
    </body>
    </html>
    """

    # Display resume HTML
    st.components.v1.html(resume_html, height=800, scrolling=True)

    # Add button to share data with portfolio builder
    if st.button("Share Data with Portfolio Builder"):
        st.session_state["portfolio_data"] = st.session_state["resume_data"]
        st.success("Data shared with Portfolio Builder!")


def additional_info_section():
    st.subheader("Additional Information")
    # Placeholder for additional information input
    st.write("This section is under construction.")


# This is important for Streamlit to recognize this as a page
if __name__ == "__main__":
    try:
        show()
    except Exception as e:
        st.error(f"An error occurred: {e}")