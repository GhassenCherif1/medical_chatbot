from langchain_community.embeddings.ollama import OllamaEmbeddings


def get_embedding_function():
    #localhost
    #embeddings = OllamaEmbeddings(model="bge-m3")
    #docker
    embeddings = OllamaEmbeddings(model="bge-m3",base_url="http://host.docker.internal:11434")
    return embeddings