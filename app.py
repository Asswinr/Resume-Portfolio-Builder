# -*- coding: utf-8 -*-
import streamlit as st
from src.pages import home, resume_builder, portfolio_builder

st.set_page_config(
    page_title='Zenith AI - Resume & Portfolio Builder', 
    layout='wide',
    page_icon='✨'
)

# Custom CSS for better navigation styling
st.markdown("""
<style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a5f 0%, #0d1b2a 100%);
    }
    
    /* Navigation title styling */
    [data-testid="stSidebar"] h1 {
        color: #69a6d1 !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 2rem !important;
        padding: 1rem 0;
        border-bottom: 2px solid rgba(105, 166, 209, 0.3);
    }
    
    /* Radio button styling */
    [data-testid="stSidebar"] .stRadio > label {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #e0e0e0 !important;
    }
    
    /* Hide default radio circles, use custom styling */
    [data-testid="stSidebar"] [role="radiogroup"] label {
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: rgba(105, 166, 209, 0.2);
    }
    
    /* Active radio selection */
    [data-testid="stSidebar"] [role="radiogroup"] [data-checked="true"] {
        background: rgba(105, 166, 209, 0.3);
        border-left: 4px solid #69a6d1;
    }
    
    /* Main content area */
    .block-container {
        padding-top: 2rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #69a6d1 0%, #5a8cb8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(105, 166, 209, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #5a8cb8 0%, #4a7a9e 100%);
        box-shadow: 0 6px 16px rgba(105, 166, 209, 0.5);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize navigation state
    if 'navigate_to' not in st.session_state:
        st.session_state['navigate_to'] = None
    
    # Sidebar branding
    st.sidebar.markdown("# ✨ Zenith AI")
    st.sidebar.markdown("---")
    
    # Check if navigation was triggered from home page buttons
    if st.session_state['navigate_to']:
        page = st.session_state['navigate_to']
        st.session_state['navigate_to'] = None  # Reset after navigation
    else:
        # Navigation
        page = st.sidebar.radio(
            'Navigation',
            ['Home', 'Resume Builder', 'Portfolio Builder'],
            label_visibility='collapsed'
        )
    
    # Route to pages
    if page == 'Home':
        home.show()
    elif page == 'Resume Builder':
        resume_builder.show()
    elif page == 'Portfolio Builder':
        portfolio_builder.show()

if __name__ == '__main__':
    main()
