import streamlit as st
import os
from pathlib import Path
import warnings
from src.populate_database import clear_database, embedding_main
from src.query_data import query_rag
from static.style.style import style

warnings.filterwarnings("ignore")

# Create the directory for storing uploaded files
path_articles = Path("./data/")
path_articles.mkdir(parents=True, exist_ok=True)
CHROMA_PATH = "./chroma"
DATA_PATH = "./data"

st.set_page_config(page_title="Chatbot | Home", page_icon=":robot_face:", layout="wide")

style()

with st.sidebar:
    st.header("Enter your datasource")
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
            DATA_PATH, CHROMA_PATH
        )  # Make sure this function is defined or imported

    if st.button("Empty Data Source"):
        clear_database(CHROMA_PATH)

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
    response = query_rag(CHROMA_PATH, prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
