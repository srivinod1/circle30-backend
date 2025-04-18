import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import StructuredTool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic.v1 import BaseModel, Field
from .tools import query_zip_scores_tool, get_zip_details_tool

# Load the OpenAI API key from the environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI LLM
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.4,
    api_key=openai_api_key
)

# Define Pydantic v1 models for tool schemas
class QueryZipScoresInput(BaseModel):
    city: str = Field(description="The name of the city")

class GetZipDetailsInput(BaseModel):
    zipcode: str = Field(description="The ZIP code to get details for")

# Define the tools
tools = [
    StructuredTool.from_function(
        func=lambda city: query_zip_scores_tool.invoke({"city": city}),
        name="query_zip_scores",
        description="Get ZIP codes for a given city.",
        args_schema=QueryZipScoresInput
    ),
    StructuredTool.from_function(
        func=lambda zipcode: get_zip_details_tool.invoke({"zipcode": zipcode}),
        name="get_zip_details",
        description="Get detailed statistics for a specific ZIP code.",
        args_schema=GetZipDetailsInput
    )
]

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an assistant that helps analyze EV charging infrastructure in Texas cities.

Your task is to:
1. Find ZIP codes in a city that have low EV charging access relative to their population
2. Only consider ZIP codes with population greater than 10,000
3. Calculate EV count per capita (EV count divided by population) for each ZIP code
4. Sort ZIP codes by EV count per capita (lowest to highest)

For each ZIP code you analyze, you must:
1. First check if its population is greater than 10,000
2. If population is 10,000 or less, immediately exclude it
3. If population is greater than 10,000, calculate its EV count per capita
4. Include it in your final sorted list

In your final response, for each ZIP code you must show:
- Population
- EV count
- EV count per capita

Do not:
- Include any ZIP codes with population ≤ 10,000
- Use or mention any other metrics
- Show any other statistics

Your response should be a clear list of ZIP codes sorted by EV count per capita (lowest to highest), with the required statistics for each ZIP code, followed by a brief analysis of the patterns you observe."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create the agent
agent = create_openai_functions_agent(llm, tools, prompt)

# Create the agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

def test_agent(query: str):
    """Test the agent with a given query."""
    try:
        response = agent_executor.invoke({
            "input": query,
            "chat_history": []
        })
        return response["output"]
    except Exception as e:
        return f"Error: {str(e)}" 