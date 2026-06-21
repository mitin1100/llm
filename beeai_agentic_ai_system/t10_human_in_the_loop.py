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
from beeai_framework.agents.requirement.requirements.ask_permission import AskPermissionRequirement


async def production_security_example():
    """
    Production-Ready RequirementAgent with Security Approval
    
    AskPermissionRequirement adds human-in-the-loop security controls.
    Same query, same tracking - but now with approval workflow.
    """
    llm = ChatModel.from_name("gemini:gemini-2.5-flash", ChatModelParameters(temperature=0))
    llm.allow_parallel_tool_calls = True
    
    SYSTEM_INSTRUCTIONS = """You are an expert cybersecurity analyst specializing in threat assessment and risk analysis.

        Your methodology:
        1. Analyze the threat landscape systematically
        2. Research authoritative sources when available
        3. Provide comprehensive risk assessment with actionable recommendations
        4. Focus on practical, implementable security measures"""

    # Production-grade RequirementAgent with security approval
    secure_agent = RequirementAgent(
        llm=llm,
        tools=[ThinkTool(), WikipediaTool()],
        memory=UnconstrainedMemory(),
        instructions=SYSTEM_INSTRUCTIONS,
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        
        requirements=[
            # Same systematic thinking requirement
            ConditionalRequirement(
                ThinkTool,
                force_at_step=1,
                min_invocations=1,
                max_invocations=2,
                consecutive_allowed=False
            ),
            # SECURITY: Permission required for external access
            AskPermissionRequirement(
                WikipediaTool,
            ),
            # Same control after permission granted
            ConditionalRequirement(
                WikipediaTool,
                only_after=[ThinkTool],
                min_invocations=0,  # Optional after approval
                max_invocations=1  # Limited even after approval
            )
        ]
    )

    ANALYSIS_QUERY = """Analyze the cybersecurity risks of quantum computing for financial institutions. 
    What are the main threats, timeline for concern, and recommended preparation strategies?"""
    
    result = await secure_agent.run(ANALYSIS_QUERY)
    print(f"\n🛡️ Security-Approved Analysis:\n{result.last_message.text}")

async def main() -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL)
    await production_security_example()

if __name__ == "__main__":
    asyncio.run(main())
