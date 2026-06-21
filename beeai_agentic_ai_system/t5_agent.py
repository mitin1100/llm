import asyncio
import logging
from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.backend import ChatModel, ChatModelParameters
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from dotenv import load_dotenv
load_dotenv()


async def minimal_tracked_agent_example():
    """
    Minimal RequirementAgent
    """
    llm = ChatModel.from_name(
        "gemini:gemini-2.5-flash", 
        ChatModelParameters(temperature=0)
    )
    # CONSISTENT SYSTEM PROMPT (used in all examples)
    SYSTEM_INSTRUCTIONS = """You are an expert cybersecurity analyst specializing in threat assessment and risk analysis.

        Your methodology:
        1. Analyze the threat landscape systematically
        2. Research authoritative sources when available
        3. Provide comprehensive risk assessment with actionable recommendations
        4. Focus on practical, implementable security measures"""
    # Minimal RequirementAgent
    minimal_agent = RequirementAgent(
        llm=llm,
        memory=UnconstrainedMemory(),
        tools=[],
        instructions=SYSTEM_INSTRUCTIONS
    )

    # CONSISTENT QUERY (used in all examples)
    ANALYSIS_QUERY = """Analyze the cybersecurity risks of quantum computing for financial institutions. 
    What are the main threats, timeline for concern, and recommended preparation strategies?"""

    result = await minimal_agent.run(ANALYSIS_QUERY)

    print(f"\n💬 Pure LLM Analysis:\n{result.last_message.text}")

async def main() -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL)
    await minimal_tracked_agent_example()

if __name__ == "__main__":
    asyncio.run(main())

