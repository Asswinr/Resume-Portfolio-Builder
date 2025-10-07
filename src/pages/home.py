# -*- coding: utf-8 -*-
import streamlit as st

def show():
    # Logo at top (perfectly centered) - FIXED: removed deprecated use_column_width
    _, col_center, _ = st.columns([1, 1, 1])
    with col_center:
        st.image("src/assets/logo.png", width=200)
    
    # Title and branding
    st.markdown("<h1 style='text-align: center; color: #69a6d1; margin-top: 1rem;'>Zenith AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #e0e0e0; font-weight: 400;'>AI Resume & Portfolio Builder</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Welcome message
    st.markdown("""
    <div style='text-align: center; font-size: 1.1rem; line-height: 1.8; color: #e0e0e0;'>
    Welcome to <strong>Zenith AI</strong> — your smart assistant for creating professional resumes, 
    cover letters, and personalized portfolios in minutes.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Features in cards with buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: rgba(105, 166, 209, 0.1); padding: 2rem; border-radius: 12px; text-align: center; height: 280px; display: flex; flex-direction: column; justify-content: space-between;'>
            <div>
                <h2 style='color: #69a6d1; margin-bottom: 1rem;'>🧠</h2>
                <h4 style='margin-bottom: 0.5rem;'>AI-Generated Resumes</h4>
                <p style='color: #b0b0b0;'>Build tailored resumes from your skills and experiences</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📄 Create Resume", key="btn_nav_resume", use_container_width=True):
            st.session_state['navigate_to'] = 'Resume Builder'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style='background: rgba(105, 166, 209, 0.1); padding: 2rem; border-radius: 12px; text-align: center; height: 280px; display: flex; flex-direction: column; justify-content: space-between;'>
            <div>
                <h2 style='color: #69a6d1; margin-bottom: 1rem;'>🌐</h2>
                <h4 style='margin-bottom: 0.5rem;'>Personalized Portfolios</h4>
                <p style='color: #b0b0b0;'>Design stunning portfolios to showcase your work</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎨 Build Portfolio", key="btn_nav_portfolio", use_container_width=True):
            st.session_state['navigate_to'] = 'Portfolio Builder'
            st.rerun()
    
    with col3:
        st.markdown("""
        <div style='background: rgba(105, 166, 209, 0.1); padding: 2rem; border-radius: 12px; text-align: center; height: 280px; display: flex; flex-direction: column; justify-content: space-between;'>
            <div>
                <h2 style='color: #69a6d1; margin-bottom: 1rem;'>📄</h2>
                <h4 style='margin-bottom: 0.5rem;'>Export Anywhere</h4>
                <p style='color: #b0b0b0;'>Download results in HTML or PDF format</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #b0b0b0; margin-top: 1rem;'>Build a resume or portfolio first to export</p>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Quick start
    st.markdown("""
    <div style='background: rgba(13, 27, 42, 0.5); padding: 2rem; border-radius: 12px; border-left: 4px solid #69a6d1;'>
        <h3 style='color: #69a6d1; margin-top: 0;'>🚀 Quick Start</h3>
        <p style='font-size: 1.05rem;'>Click the buttons above or use the <strong>Navigation</strong> menu on the left to get started with the Resume Builder or Portfolio Builder.</p>
    </div>
    """, unsafe_allow_html=True)
