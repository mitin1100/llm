import asyncio
import logging
from pydantic import BaseModel, Field
from beeai_framework.backend import ChatModel, ChatModelParameters, UserMessage, SystemMessage


# Define a structured output for business planning
class BusinessPlan(BaseModel):
    """A comprehensive business plan structure."""
    business_name: str = Field(description="Catchy name for the business")
    elevator_pitch: str = Field(description="30-second description of the business")
    target_market: str = Field(description="Primary target audience")
    unique_value_proposition: str = Field(description="What makes this business special")
    revenue_streams: list[str] = Field(description="Ways the business will make money")
    startup_costs: str = Field(description="Estimated initial investment needed")
    key_success_factors: list[str] = Field(description="Critical elements for success")


async def structured_output_example():
    llm = ChatModel.from_name(
        "gemini:gemini-2.5-flash", 
        ChatModelParameters(temperature=0)
    )
    messages = [
        SystemMessage(content="You are an expert business consultant and entrepreneur."),
        UserMessage(content="Create a business plan for a mobile app that helps people find and book unique local experiences in their city.")
    ]
    response = await llm.run(messages, response_format=BusinessPlan)
    business_plan = BusinessPlan.model_validate_json(
        response.get_text_content()
    )
    print("User: Create a business plan for a mobile app that helps people find and book unique local experiences in their city.")
    print("\n🚀 AI-Generated Business Plan:")
    print(f"💡 Business Name: {business_plan.business_name}")
    print(f"🎯 Elevator Pitch: {business_plan.elevator_pitch}")
    print(f"👥 Target Market: {business_plan.target_market}")
    print(f"⭐ Unique Value Proposition: {business_plan.unique_value_proposition}")
    print(f"💰 Revenue Streams: {', '.join(business_plan.revenue_streams)}")
    print(f"💵 Startup Costs: {business_plan.startup_costs}")
    print(f"🔑 Key Success Factors:")
    for factor in business_plan.key_success_factors:
        print(f"  - {factor}")


async def main() -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL) # Suppress unwanted warnings
    await structured_output_example()

if __name__ == "__main__":
    asyncio.run(main())

