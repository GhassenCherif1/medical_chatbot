import asyncio
from query_data import query_rag
from langchain.schema import ChatMessage  # Ensure this matches your actual import

async def main():
    chat = [ChatMessage(role="user", content="What is Pneumonia?"),]
    response = await query_rag(chat)

if __name__ == "__main__":
    asyncio.run(main())