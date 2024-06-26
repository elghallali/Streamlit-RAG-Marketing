import streamlit as st
import os
from pathlib import Path
import warnings
from dotenv import load_dotenv
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from src.populate_database import clear_database, embedding_main
from src.query_data import query_rag
from static.style.style import style

warnings.filterwarnings("ignore")
load_dotenv()
# Create the directory for storing uploaded files
path_articles = Path("./data/")
path_articles.mkdir(parents=True, exist_ok=True)
CHROMA_PATH = "./chroma"
DATA_PATH = "./data"
BASE_URL = os.getenv("BASE_URL")

st.set_page_config(page_title="Chatbot | Home", page_icon=":robot_face:", layout="wide")

style()

with open("./config.yaml", encoding="utf-8") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["pre-authorized"],
)

with st.sidebar:
    authenticator.login()
    if st.session_state["authentication_status"]:

        st.header(f'*{st.session_state["name"]}*')
        st.markdown("""<br><br>""", unsafe_allow_html=True)
        st.subheader("Enter your datasource")
        uploaded_files = st.file_uploader(
            "Import your data",
            key="data_import",
            accept_multiple_files=True,
            label_visibility="hidden",
        )
        if uploaded_files:
            for uploaded_file in uploaded_files:
                bytes_data = uploaded_file.read()
                file_path = os.path.join(path_articles, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(bytes_data)
            # Assuming embedding_main() is defined elsewhere
            embedding_main(
                BASE_URL, DATA_PATH, CHROMA_PATH
            )  # Make sure this function is defined or imported

        if st.button("Empty Data Source", type="primary"):
            clear_database(CHROMA_PATH)
        st.markdown("""<br><br>""", unsafe_allow_html=True)
        authenticator.logout()
    elif st.session_state["authentication_status"] is False:
        st.error("Username/password is incorrect")
    elif st.session_state["authentication_status"] is None:
        st.warning("Please enter your username and password")

st.markdown(
    """

<center>

# 💬 Chatbot About Marketing

</center>

<div style="height: 30px;"></div>
""",
    unsafe_allow_html=True,
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Message Chatbot?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    response = query_rag(BASE_URL, CHROMA_PATH, prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
