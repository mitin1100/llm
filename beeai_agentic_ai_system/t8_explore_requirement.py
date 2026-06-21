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


async def controlled_execution_example():
    """
    RequirementAgent with Controlled Execution - Requirements System
    
    Requirements provide precise control over tool execution order and behavior.
    Same query, same tracking - but now with strict execution rules.
    """
    llm = ChatModel.from_name("gemini:gemini-2.5-flash", ChatModelParameters(temperature=0))
    llm.allow_parallel_tool_calls = True
    
    SYSTEM_INSTRUCTIONS = """You are an expert cybersecurity analyst specializing in threat assessment and risk analysis.

        Your methodology:
        1. Analyze the threat landscape systematically
        2. Research authoritative sources when available
        3. Provide comprehensive risk assessment with actionable recommendations
        4. Focus on practical, implementable security measures"""
    
    controlled_agent = RequirementAgent(
        llm=llm,
        memory=UnconstrainedMemory(),
        instructions=SYSTEM_INSTRUCTIONS,
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        tools=[ThinkTool(), WikipediaTool()],
        requirements=[
            ConditionalRequirement(ThinkTool,
                                   force_at_step=1,
                                   min_invocations=1,
                                   max_invocations=3,
                                   consecutive_allowed=False),

            ConditionalRequirement(WikipediaTool,
                                   only_after=[ThinkTool],
                                   min_invocations=1,
                                   max_invocations=2
                                  )
        ]
    )

    ANALYSIS_QUERY = """Analyze the cybersecurity risks of quantum computing for financial institutions. 
    What are the main threats, timeline for concern, and recommended preparation strategies?"""
    
    result = await controlled_agent.run(ANALYSIS_QUERY)
    print(f"\n🔧 Controlled Execution Analysis:\n{result.last_message.text}")

async def main() -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL)
    await controlled_execution_example()

if __name__ == "__main__":
    asyncio.run(main())

