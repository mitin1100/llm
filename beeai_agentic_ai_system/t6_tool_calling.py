import asyncio
import logging
from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.agents.requirement.requirements.conditional import ConditionalRequirement
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.backend import ChatModel, ChatModelParameters
from beeai_framework.tools.search.wikipedia import WikipediaTool
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool


async def wikipedia_enhanced_agent_example():
    """
    RequirementAgent with Wikipedia - Research Enhancement and tracking
    
    Adding WikipediaTool provides access to Wikipedia summaries for contextual research.
    Same query - but now with research capability.
    Moreover, middleware is used to track all tool usage.
    """
    llm = ChatModel.from_name("gemini:gemini-2.5-flash", ChatModelParameters(temperature=0))
    SYSTEM_INSTRUCTIONS = """You are an expert cybersecurity analyst specializing in threat assessment and risk analysis.

        Your methodology:
        1. Analyze the threat landscape systematically
        2. Research authoritative sources when available
        3. Provide comprehensive risk assessment with actionable recommendations
        4. Focus on practical, implementable security measures"""
    
    wikipedia_agent = RequirementAgent(
        llm=llm,
        memory=UnconstrainedMemory(),
        tools=[WikipediaTool()],
        instructions=SYSTEM_INSTRUCTIONS,
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        requirements=[ConditionalRequirement(WikipediaTool, max_invocations=2)]
    )

    ANALYSIS_QUERY = """Analyze the cybersecurity risks of quantum computing for financial institutions. 
    What are the main threats, timeline for concern, and recommended preparation strategies?"""
    
    result = await wikipedia_agent.run(ANALYSIS_QUERY)
    print(f"\n📖 Research-Enhanced Analysis:\n{result.last_message.text}")

async def main() -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL)
    await wikipedia_enhanced_agent_example()

if __name__ == "__main__":
    asyncio.run(main())

