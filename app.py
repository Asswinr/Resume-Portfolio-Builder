# -*- coding: utf-8 -*-
import streamlit as st
from src.pages import home, resume_builder, portfolio_builder

st.set_page_config(page_title='AI Resume & Portfolio Builder', layout='wide')

def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.radio('Go to', ['Home', 'Resume Builder', 'Portfolio Builder'])

    if page == 'Home':
        home.show()
    elif page == 'Resume Builder':
        resume_builder.show()
    elif page == 'Portfolio Builder':
        portfolio_builder.show()

if __name__ == '__main__':
    main()
