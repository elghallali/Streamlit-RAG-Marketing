import os
from src.populate_database import clear_database, embedding_main
from src.query_data import query_rag
from langchain_community.llms.ollama import Ollama
from dotenv import load_dotenv

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""
load_dotenv()
test_data_path = "./tests/data_test"
chromaDB_test_path = "./tests/chromaDB_Test"
BASE_URL = os.getenv("BASE_URL")


def test_embedding():
    """
    Test the embedding function to ensure it successfully processes the test data.
    """
    assert embedding_main(BASE_URL, test_data_path, chromaDB_test_path) == True


def test_about_Marketing():
    assert query_and_validate(
        chromaDB_path=chromaDB_test_path,
        question="Tell me about Marketing",
        expected_response=' According to J. Estwood\'s book "30 Minutes to Write a Marketing Plan" (1997) and the American Marketing Association',
    )


def test_about_MLOps():
    assert query_and_validate(
        chromaDB_path=chromaDB_test_path,
        question="Tell me about MLOps?",
        expected_response="I apologize, but I don't see any information related to MLOps (Machine Learning Operations) in the provided context. The text appears to be focused on marketing and sales strategies for a product or service, with topics such as 4P (product, price, promotion, place), distribution plans, and sponsorship considerations.",
    )


def query_and_validate(chromaDB_path: str, question: str, expected_response: str):
    response_text = query_rag(BASE_URL, chromaDB_path, question)
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    model = Ollama(model="llama3")
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    print(prompt)

    if "true" in evaluation_results_str_cleaned:
        # Print response in Green if it is correct.
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "false" in evaluation_results_str_cleaned:
        # Print response in Red if it is incorrect.
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        raise ValueError(
            "Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )


def test_clear_database_existing_directory():
    """
    Test that clear_database removes an existing directory.
    """

    # Ensure the directory exists before running the function.
    assert os.path.exists(chromaDB_test_path)

    # Call the function to clear the database.
    clear_database(chromaDB_test_path)

    # Verify the directory has been removed.
    assert not os.path.exists(chromaDB_test_path)
