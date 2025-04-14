import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool, AgentType
import geopandas as gpd
from typing import List, Union

# Load the OpenAI API key from the environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI LLM
llm = OpenAI(api_key=openai_api_key)

# Load GeoData from the enriched GeoJSON
def load_geojson_data(city: str):
    ZIP_DATA_PATH = "outputs/zip_ev_scores_enriched.geojson"  # Path to the geojson file
    gdf = gpd.read_file(ZIP_DATA_PATH)
    city_gdf = gdf[gdf["city"].str.lower() == city.lower()]
    return city_gdf

# 1️⃣ Get underserved ZIPs based on underserved_score without using the query_zip_scores tool
@tool
def get_top_underserved_zips(city: str, top_n: int = 3) -> str:
    """
    Return the top underserved ZIP codes for a given city, sorted by 'underserved_score' (higher is worse).
    """
    city_gdf = load_geojson_data(city)
    if city_gdf.empty:
        return f"No ZIPs found for city: {city}"

    # Sort by underserved score (higher is worse)
    top_zips = city_gdf.sort_values("underserved_score", ascending=False).head(top_n)
    
    # Format the response
    top_zips_info = top_zips[["ZIP", "population", "ev_poi_count", "underserved_score"]].to_markdown(index=False)
    return top_zips_info

# 2️⃣ Get GeoJSON for a city (this is for optional map display)
@tool
def get_geojson_for_city(city: str) -> str:
    """
    Return a GeoJSON feature collection of ZIP codes for the given city.
    Useful for displaying maps.
    """
    city_gdf = load_geojson_data(city)
    if city_gdf.empty:
        return f"No ZIPs found for city: {city}"
    return city_gdf.to_json()

# Define the agent tools
tools = [
    Tool(
        name="get_top_underserved_zips",
        func=get_top_underserved_zips,
        description="Get the top underserved ZIP codes for a given city"
    ),
    Tool(
        name="get_geojson_for_city",
        func=get_geojson_for_city,
        description="Get the boundaries of a city in GeoJSON format"
    )
]

# Initialize the LLM chain
llm_chain = LLMChain(llm=llm, prompt=PromptTemplate(input_variables=["question"], template="{question}"))

# Initialize the agent with tools
agent = initialize_agent(
    tools,
    llm_chain,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Function to interact with the agent
def test_agent(query: str):
    response = agent.run(query)
    return response

# Example usage
query = "What are the top 3 underserved zip codes in Austin for EV?"
result = test_agent(query)
print(result)
