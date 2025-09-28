# -*- coding: utf-8 -*-
import streamlit as st

def show():
    st.title("AI Resume & Portfolio Builder")
    
    st.markdown("""
    ## Welcome to the AI Resume & Portfolio Builder!
    
    This application helps you create professional resumes and portfolios with AI assistance.
    
    ### Features:
    - **Resume Builder**: Create professional resumes with AI-powered content suggestions
    - **Portfolio Builder**: Showcase your work with customizable portfolio templates
    - **Export Options**: Download your resume and portfolio in multiple formats
    
    Get started by selecting an option from the sidebar.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("### Resume Builder")
        st.write("Create a professional resume with AI assistance.")
        if st.button("Create Resume", key="resume_btn"):
            st.session_state["page"] = "Resume Builder"
            st.rerun()
    
    with col2:
        st.info("### Portfolio Builder")
        st.write("Showcase your work with a customizable portfolio.")
        if st.button("Create Portfolio", key="portfolio_btn"):
            st.session_state["page"] = "Portfolio Builder"
            st.rerun()