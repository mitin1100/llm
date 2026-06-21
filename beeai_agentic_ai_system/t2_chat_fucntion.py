import asyncio
import logging
from beeai_framework.backend import ChatModel, ChatModelParameters, UserMessage, SystemMessage
from google import genai
from google.genai.types import GenerateContentConfig

# client = genai.client()

async def basic_chat_example():
    llm = ChatModel.from_name(
        "gemini:gemini-2.5-flash", 
        ChatModelParameters(temperature=0)
    )

    messages = [
        SystemMessage(content="You are a helpful AI assistant and creative writing expert."),
        UserMessage(content="Help me brainstorm a unique business idea for a food delivery service that doesn't exist yet.")
    ]

    response = await llm.run(messages)

    print("User: Help me brainstorm a unique business idea for a food delivery service that doesn't exist yet.")
    print(f"Assistant: {response.get_text_content()}")
    return response

async def main() -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL)
    response = await basic_chat_example()


if __name__ == "__main__":
    asyncio.run(main())

