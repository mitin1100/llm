import asyncio
import logging
from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.agents.requirement.requirements.conditional import ConditionalRequirement
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.backend import ChatModel, ChatModelParameters
from beeai_framework.tools.think import ThinkTool
from beeai_framework.tools.search.wikipedia import WikipediaTool
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool


async def reasoning_enhanced_agent_example():
    """
    RequirementAgent with Systematic Reasoning - ThinkTool + WikipediaTool
    
    Adding ThinkTool enables structured reasoning alongside research.
    Same query, same tracking - now with visible thinking process.
    """
    llm = ChatModel.from_name("gemini:gemini-2.5-flash", ChatModelParameters(temperature=0))
    SYSTEM_INSTRUCTIONS = """You are an expert cybersecurity analyst specializing in threat assessment and risk analysis.

        Your methodology:
        1. Analyze the threat landscape systematically
        2. Research authoritative sources when available
        3. Provide comprehensive risk assessment with actionable recommendations
        4. Focus on practical, implementable security measures"""
    reasoning_agent = RequirementAgent(
        llm=llm,
        memory=UnconstrainedMemory(),
        tools=[ThinkTool(), WikipediaTool()],
        instructions=SYSTEM_INSTRUCTIONS,
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        requirements=[
            ConditionalRequirement(ThinkTool, max_invocations=2),
            ConditionalRequirement(WikipediaTool, max_invocations=2)
        ]
    )

    ANALYSIS_QUERY = """Analyze the cybersecurity risks of quantum computing for financial institutions. 
    What are the main threats, timeline for concern, and recommended preparation strategies?"""
    
    result = await reasoning_agent.run(ANALYSIS_QUERY)
    print(f"\n🧠 Reasoning + Research Analysis:\n{result.last_message.text}")

async def main() -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL)
    await reasoning_enhanced_agent_example()

if __name__ == "__main__":
    asyncio.run(main())

