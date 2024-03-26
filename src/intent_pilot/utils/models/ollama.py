from langchain_core.messages import HumanMessage
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

def format_ollama_message(data):
    text = data["text"]
    image = data["image"]

    image_part = {
        "type": "image_url",
        "image_url": f"data:image/jpeg;base64,{image}",
    }

    content_parts = []

    text_part = {"type": "text", "text": text}

    content_parts.append(text_part)
    content_parts.append(image_part)

    return HumanMessage(content=content_parts)

# ollama_client is the llm=ChatOllama(...) from LangChain
def get_response_from_ollama(ollama_client, messages):
    prompt = ChatPromptTemplate.from_messages(messages)
    chain = prompt | ollama_client
    response = chain.invoke({})
    return response.content
