import pandas as pd
from langchain.tools import tool

@tool
def list_cities() -> str:
    """List all available cities in the dataset."""
    df = pd.read_csv('data/texas_ev_data.csv')
    cities = df['city'].unique().tolist()
    return f"Available cities: {', '.join(cities)}"

@tool
def query_zip_scores(city: str) -> str:
    """Get ZIP codes for a given city."""
    df = pd.read_csv('data/texas_ev_data.csv')
    city_data = df[df['city'].str.lower() == city.lower()]
    if city_data.empty:
        return f"No data found for city: {city}"
    
    result = []
    for _, row in city_data.iterrows():
        result.append(f"ZIP: {row['zipcode']}, Population: {row['population']}, EV Count: {row['ev_count']}")
    return "\n".join(result)

@tool
def get_geojson_for_city(city: str) -> str:
    """Get GeoJSON data for a given city."""
    # This is a placeholder - implement actual GeoJSON retrieval
    return f"GeoJSON data for {city}"

@tool
def get_zip_details(zipcode: str) -> str:
    """Get detailed statistics for a specific ZIP code."""
    df = pd.read_csv('data/texas_ev_data.csv')
    zip_data = df[df['zipcode'] == int(zipcode)]
    if zip_data.empty:
        return f"No data found for ZIP code: {zipcode}"
    
    row = zip_data.iloc[0]
    return f"""
ZIP Code: {row['zipcode']}
City: {row['city']}
Population: {row['population']}
EV Count: {row['ev_count']}
EV per Capita: {row['ev_count'] / row['population']:.6f}
""" 