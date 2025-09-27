import streamlit as st
import pandas as pd

def show():
    st.title("Portfolio Builder")
    
    # Initialize session state for portfolio data
    if "portfolio_data" not in st.session_state:
        st.session_state["portfolio_data"] = {
            "personal_info": {},
            "about": "",
            "projects": [],
            "skills": [],
            "contact": {}
        }
    
    # Sidebar for sections
    section = st.sidebar.radio(
        "Portfolio Sections",
        ["Personal Information", "About Me", "Projects", "Skills", "Contact"]
    )
    
    if section == "Personal Information":
        personal_info_section()
    elif section == "About Me":
        about_section()
    elif section == "Projects":
        projects_section()
    elif section == "Skills":
        skills_section()
    elif section == "Contact":
        contact_section()
    
    # Preview and export options
    st.sidebar.divider()
    if st.sidebar.button("Preview Portfolio"):
        preview_portfolio()
    
    if st.sidebar.button("Export Portfolio"):
        # This will be implemented in the export functionality task
        st.sidebar.success("Export functionality will be implemented soon!")

def personal_info_section():
    st.subheader("Personal Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name", st.session_state["portfolio_data"]["personal_info"].get("name", ""))
        title = st.text_input("Professional Title", st.session_state["portfolio_data"]["personal_info"].get("title", ""))
    
    with col2:
        location = st.text_input("Location", st.session_state["portfolio_data"]["personal_info"].get("location", ""))
        photo = st.file_uploader("Profile Photo", type=["jpg", "jpeg", "png"])
    
    social_media = st.expander("Social Media Links")
    with social_media:
        linkedin = st.text_input("LinkedIn", st.session_state["portfolio_data"]["personal_info"].get("linkedin", ""))
        github = st.text_input("GitHub", st.session_state["portfolio_data"]["personal_info"].get("github", ""))
        twitter = st.text_input("Twitter", st.session_state["portfolio_data"]["personal_info"].get("twitter", ""))
        other = st.text_input("Other", st.session_state["portfolio_data"]["personal_info"].get("other_social", ""))
    
    if st.button("Save Personal Information"):
        portfolio_info = {
            "name": name,
            "title": title,
            "location": location,
            "linkedin": linkedin,
            "github": github,
            "twitter": twitter,
            "other_social": other
        }
        
        if photo is not None:
            # In a real implementation, we would save the photo
            portfolio_info["has_photo"] = True
        
        st.session_state["portfolio_data"]["personal_info"] = portfolio_info
        st.success("Personal information saved!")

def about_section():
    st.subheader("About Me")
    
    about_text = st.text_area(
        "Tell your story",
        st.session_state["portfolio_data"].get("about", ""),
        height=300,
        help="Write a compelling bio that highlights your journey, values, and what makes you unique."
    )
    
    if st.button("Save About Me"):
        st.session_state["portfolio_data"]["about"] = about_text
        st.success("About Me section saved!")

def projects_section():
    st.subheader("Projects")
    
    # Display existing projects
    for i, proj in enumerate(st.session_state["portfolio_data"]["projects"]):
        with st.expander(f"{proj.get('title', 'Project')}"):
            st.write(f"**Project Title:** {proj.get('title', '')}")
            st.write(f"**Category:** {proj.get('category', '')}")
            st.write(f"**Description:**")
            st.write(proj.get('description', ''))
            st.write(f"**Technologies:** {proj.get('technologies', '')}")
            
            if proj.get('image_url'):
                st.write(f"**Image URL:** {proj['image_url']}")
            
            if proj.get('project_url'):
                st.write(f"**Project URL:** {proj['project_url']}")
            
            if st.button("Remove", key=f"remove_portfolio_proj_{i}"):
                st.session_state["portfolio_data"]["projects"].pop(i)
                st.experimental_rerun()
    
    # Add new project
    with st.expander("Add Project"):
        title = st.text_input("Project Title", key="new_portfolio_proj_title")
        category = st.selectbox(
            "Category",
            ["Web Development", "Mobile App", "Data Science", "Machine Learning", 
             "UI/UX Design", "Game Development", "Other"],
            key="new_portfolio_proj_category"
        )
        
        description = st.text_area("Project Description", key="new_portfolio_proj_desc")
        technologies = st.text_input("Technologies Used", key="new_portfolio_proj_tech")
        
        col1, col2 = st.columns(2)
        with col1:
            image = st.file_uploader("Project Image", type=["jpg", "jpeg", "png"], key="new_portfolio_proj_img")
        with col2:
            image_url = st.text_input("or Image URL", key="new_portfolio_proj_img_url")
        
        project_url = st.text_input("Project URL", key="new_portfolio_proj_url")
        
        if st.button("Add Project"):
            project_data = {
                "title": title,
                "category": category,
                "description": description,
                "technologies": technologies,
                "project_url": project_url
            }
            
            if image is not None:
                # In a real implementation, we would save the image
                project_data["has_image"] = True
            elif image_url:
                project_data["image_url"] = image_url
            
            st.session_state["portfolio_data"]["projects"].append(project_data)
            st.success("Project added!")
            st.experimental_rerun()

def skills_section():
    st.subheader("Skills")
    
    # Display existing skills
    if st.session_state["portfolio_data"]["skills"]:
        st.write("Current Skills:")
        skills_df = pd.DataFrame(st.session_state["portfolio_data"]["skills"])
        st.dataframe(skills_df)
        
        if st.button("Clear All Skills"):
            st.session_state["portfolio_data"]["skills"] = []
            st.experimental_rerun()
    
    # Add new skills
    st.write("Add Skills:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        skill = st.text_input("Skill Name", key="portfolio_skill_name")
    
    with col2:
        proficiency = st.slider(
            "Proficiency (%)",
            min_value=10,
            max_value=100,
            step=5,
            value=75,
            key="portfolio_skill_prof"
        )
    
    with col3:
        category = st.selectbox(
            "Category",
            ["Technical", "Creative", "Soft Skills", "Languages", "Tools", "Other"],
            key="portfolio_skill_cat"
        )
    
    if st.button("Add Skill"):
        st.session_state["portfolio_data"]["skills"].append({
            "skill": skill,
            "proficiency": proficiency,
            "category": category
        })
        st.success(f"Added {skill} to your skills!")
        st.experimental_rerun()

def contact_section():
    st.subheader("Contact Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        email = st.text_input("Email", st.session_state["portfolio_data"]["contact"].get("email", ""))
        phone = st.text_input("Phone", st.session_state["portfolio_data"]["contact"].get("phone", ""))
    
    with col2:
        location = st.text_input("Location", st.session_state["portfolio_data"]["contact"].get("location", ""))
        availability = st.selectbox(
            "Availability",
            ["Available for hire", "Open to freelance", "Not available", "Contact me"],
            index=0 if not st.session_state["portfolio_data"]["contact"].get("availability") else 
                  ["Available for hire", "Open to freelance", "Not available", "Contact me"].index(
                      st.session_state["portfolio_data"]["contact"].get("availability")
                  )
        )
    
    contact_message = st.text_area(
        "Contact Form Message",
        st.session_state["portfolio_data"]["contact"].get("message", "Thank you for your interest! Please fill out the form to get in touch with me."),
        height=100
    )
    
    if st.button("Save Contact Information"):
        st.session_state["portfolio_data"]["contact"] = {
            "email": email,
            "phone": phone,
            "location": location,
            "availability": availability,
            "message": contact_message
        }
        st.success("Contact information saved!")

def preview_portfolio():
    st.header("Portfolio Preview")
    
    # Personal Information
    personal = st.session_state["portfolio_data"]["personal_info"]
    if personal:
        st.title(personal.get("name", "Your Name"))
        st.subheader(personal.get("title", "Professional Title"))
        st.write(f"📍 {personal.get('location', 'Location')}")
        
        # Social media links
        social_links = []
        if personal.get("linkedin"): social_links.append(f"[LinkedIn]({personal['linkedin']})")
        if personal.get("github"): social_links.append(f"[GitHub]({personal['github']})")
        if personal.get("twitter"): social_links.append(f"[Twitter]({personal['twitter']})")
        if personal.get("other_social"): social_links.append(f"[Other]({personal['other_social']})")
        
        if social_links:
            st.write(" | ".join(social_links))
    
    # About section
    if st.session_state["portfolio_data"].get("about"):
        st.header("About Me")
        st.write(st.session_state["portfolio_data"]["about"])
    
    # Projects section
    if st.session_state["portfolio_data"]["projects"]:
        st.header("Projects")
        
        for i, project in enumerate(st.session_state["portfolio_data"]["projects"]):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if project.get("has_image") or project.get("image_url"):
                    st.image("https://via.placeholder.com/300x200?text=Project+Image", use_column_width=True)
            
            with col2:
                st.subheader(project.get("title", "Project Title"))
                st.write(f"**Category:** {project.get('category', 'Category')}")
                st.write(project.get("description", "Project description"))
                st.write(f"**Technologies:** {project.get('technologies', 'Technologies')}")
                
                if project.get("project_url"):
                    st.write(f"[View Project]({project['project_url']})")
            
            st.divider()
    
    # Skills section
    if st.session_state["portfolio_data"]["skills"]:
        st.header("Skills")
        
        # Group skills by category
        skills_by_category = {}
        for skill in st.session_state["portfolio_data"]["skills"]:
            category = skill.get("category", "Other")
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(skill)
        
        # Display skills by category
        for category, skills in skills_by_category.items():
            st.subheader(category)
            for skill in skills:
                st.write(f"{skill.get('skill', 'Skill')}: {skill.get('proficiency', 0)}%")
                st.progress(int(skill.get('proficiency', 0)) / 100)
    
    # Contact section
    if st.session_state["portfolio_data"]["contact"]:
        st.header("Contact Me")
        contact = st.session_state["portfolio_data"]["contact"]
        
        st.write(contact.get("message", ""))
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Email:** {contact.get('email', '')}")
            st.write(f"**Phone:** {contact.get('phone', '')}")
        
        with col2:
            st.write(f"**Location:** {contact.get('location', '')}")
            st.write(f"**Status:** {contact.get('availability', '')}")