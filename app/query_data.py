from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from .get_embedding_function import get_embedding_function
from .schemas import ChatMessage
#Testing Retriver
# from get_embedding_function import get_embedding_function
# from schemas import ChatMessage
from typing import List
import httpx
CHROMA_PATH = "app/chroma"
#Testing Retriever
#CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Below are the relevant context documents that may assist in answering the user's question:

{context}

---

Based on the above context, please provide a clear, accurate and direct answer to the following question without mentioning that you are using any external sources:

{question}

"""


async def query_rag(chatmessages : List[ChatMessage]):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    query_text = chatmessages[-1].content
    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=3)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)
    chatmessages[-1].content = prompt
    #local
    #url = "http://localhost:11434/api/chat"
    #docker
    url = "http://host.docker.internal:11434/api/chat"
    payload = {"messages": [msg.model_dump() for msg in chatmessages], "model":"llama3.2:1b-instruct-q6_K", "stream": False}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, timeout=3600)
        response_text = response.json()  # ou `response.json()` si c'est un JSON


    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text

def query_retriever(chatmessages : List[ChatMessage]):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    query_text = chatmessages[-1].content
    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=3)
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Sources: {sources}"
    print(formatted_response)
    return sources