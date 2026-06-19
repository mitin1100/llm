import asyncio
import logging
from beeai_framework.backend import ChatModel, ChatModelParameters, UserMessage, SystemMessage
from google import genai
from google.genai.types import GenerateContentConfig

client = genai.client()

async def basic_chat_example():
    messages = [
        SystemMessage(content="You are a helpful AI assistant and creative writing expert."),
        UserMessage(content="Help me brainstorm a unique business idea for a food delivery service that doesn't exist yet.")
    ]

    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents="\n".join(messages),
        config=GenerateContentConfig(
            temperature=0
        )
    )
    print("User: Help me brainstorm a unique business idea for a food delivery service that doesn't exist yet.")
    print(f"Assistant: {response.text}")

