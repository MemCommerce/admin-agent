from httpx import AsyncClient
from agents import Agent, Runner

from schemas import DescriptionReq


prompt_builder_agent = Agent(
    name="prompt_builder_agent",
    instructions="""
You are a prompt builder. Based on the given product details and instructions, 
generate a clear, detailed prompt for a product description AI.
Output only the final prompt text.
""",
)

description_agent = Agent(
    name="product_description_agent",
    instructions="You are a helpful assistant that writes product descriptions for e-commerce listings.",
)


async def get_prompt_template() -> str:
    async with AsyncClient() as client:
        response = await client.get(
            "https://raw.githubusercontent.com/MemCommerce/memcommerce-docs/refs/heads/main/description-prompt-template.md"
        )
        return response.text


async def create_ai_description(product_details: DescriptionReq) -> str:
    runner = Runner()

    prompt_template = await get_prompt_template()

    # Build input for prompt builder agent
    builder_input = f"""
        Instructions:
        {prompt_template}

        Product Details:
        {product_details.model_dump_json(indent=2)}
    """

    # Step 1: build the prompt
    built_prompt_result = await runner.run(prompt_builder_agent, input=builder_input)
    final_prompt = built_prompt_result.final_output

    # Step 2: generate product description from prompt
    description_result = await runner.run(description_agent, input=final_prompt)
    description = description_result.final_output

    return description
