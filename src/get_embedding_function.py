from langchain_community.embeddings.ollama import OllamaEmbeddings


def get_embedding_function(url):
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=url)
    return embeddings
