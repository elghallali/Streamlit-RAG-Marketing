import os
import shutil
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from src.get_embedding_function import get_embedding_function
from typing import List
import time

from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader


def embedding_main(data_path, chroma_path):

    tic = time.time()
    # Create (or update) the data store.
    documents = load_documents(data_path)
    if not documents:
        print("No documents loaded.")
        return False

    chunks = split_documents(documents)
    add_to_chroma(chroma_path, chunks)
    toc = time.time()
    print(f"The time is :{(toc - tic)} seconds")
    return True


def load_documents(data_path):
    document_loader = PyPDFDirectoryLoader(data_path)
    return document_loader.load()


def split_documents(documents: List[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    print(documents)
    return text_splitter.split_documents(documents)


def add_to_chroma(chroma_path, chunks: List[Document]):
    # Load the existing database.
    db = Chroma(
        persist_directory=chroma_path, embedding_function=get_embedding_function()
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of documents existing in the database: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 {len(new_chunks)} new documents to add ")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("✅ No documents to add! ")


def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks


def clear_database(chroma_path):
    if os.path.exists(chroma_path):
        shutil.rmtree(chroma_path)
