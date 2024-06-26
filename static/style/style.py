import streamlit as st
import base64
import os


def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

background_img = get_img_as_base64(f"{os.getcwd()}/static/img/background.jpg")

def style():

    st.markdown(f"""
    <style>
        div.block-container {{padding-top: 0.1rem;}}
        
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{background_img}");
            background-size: cover;
        }}

        [data-testid="stSidebar"] > div:first-child {{
            background-image: linear-gradient(45deg, #00ffff, #800080);
        }}

        [data-testid="stHeader"]{{
            background-color: rgba(0,0,0,0);
        }}

        [data-testid="stBottom"] > div:first-child {{
            background-color: rgba(0,0,0,0);
        }}
        
        [data-testid="stToolbar"] {{
            right: 2rem;
        }}
        
        [data-testid="stChatMessage"] {{
            background : rgba(0,0,0,0.8);
            border: 1px solid #800080;
            padding-right: 15px;
        }}
        
        [data-testid="stSidebarUserContent"] [data-testid="stMarkdownContainer"] h2 {{
            text-align: center;
        }}
        
        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="element-container"]:last-child [data-testid="stButton"] {{
            display: flex;
            justify-content: flex-end;
            
            
        }}
        
        [data-testid="stMarkdownContainer"] p {{
            font-size: 1.4rem;
            font-weight: 400;
        }}
        
        [data-testid="stMarkdownContainer"] li {{
            font-size: 1.4rem;
            font-weight: 400;
        }}
        
        [data-baseweb="base-input"] textarea {{
            font-size: 1.4rem;
            font-weight: 400;
        }}
        
        #MainMenu {{visibility: hidden;}}
        
        footer {{visibility: hidden;}}
        
        header {{visibility: hidden;}}
        
    </style>
    
    """,unsafe_allow_html=True)