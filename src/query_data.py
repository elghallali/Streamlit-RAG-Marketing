from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from src.get_embedding_function import get_embedding_function
from langchain_community.vectorstores import Chroma

CHROMA_PATH = "./chroma"

# Configurer Template Prompt
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an assistant answering questions ."),
        ("human", "Try to respond using the following context :{context}"),
        ("human", "Answer the following question : {question}"),
    ]
)


def query_rag(url, chroma_path, query_text: str) -> str:
    # Prepare the DB.
    embedding_function = get_embedding_function(url)
    db = Chroma(persist_directory=chroma_path, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)
    if len(results) == 0:
        return "Sorry, the answer to your question does not exist in the database 😞 , try asking another question!"

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = Ollama(model="llama3", temperature=0, base_url=url, verbose=True)

    generated_response = ""
    for word in model.stream(prompt):
        generated_response += word

    return generated_response
