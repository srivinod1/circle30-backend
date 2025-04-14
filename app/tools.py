import os
import geopandas as gpd
from typing import List, Union
from langchain.tools import tool
from .storage import storage

# Global cache (so tools don't reload on every call)
ZIP_DATA_PATH = "zip_ev_score.geojson"  # Updated file path
_gdf = None

def load_data():
    global _gdf
    if _gdf is None:
        print(f"Loading data from S3: {ZIP_DATA_PATH}")
        local_path = storage.get_file(ZIP_DATA_PATH)
        if not local_path:
            print(f"ERROR: Could not load data file from S3")
            return None
        try:
            _gdf = gpd.read_file(local_path)
            print(f"Data loaded successfully. Shape: {_gdf.shape}")
            print(f"Available columns: {_gdf.columns.tolist()}")
            print(f"Available cities: {sorted(_gdf['city'].dropna().unique().tolist())[:5]} ...")
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return None
    return _gdf

# 1️⃣ List all unique cities
def list_cities() -> List[str]:
    """List all available cities in the ZIP-level EV data."""
    try:
        gdf = load_data()
        return sorted(gdf["city"].dropna().unique().tolist())
    except Exception as e:
        print(f"Error in list_cities: {str(e)}")
        return []

# 2️⃣ Query underserved ZIPs in a city
def query_zip_scores(city: str, top_n: int = 5) -> str:
    """
    Return ZIP codes for a given city with population > 10,000, sorted by EV count per capita (lowest to highest).
    """
    try:
        print(f"Querying ZIP scores for city: {city}")
        gdf = load_data()
        
        # Normalize city names (case insensitive matching)
        city = city.strip().lower()
        print(f"Normalized city name: {city}")
        
        # Filter the dataset for the city
        df = gdf[gdf["city"].str.lower() == city]
        print(f"Found {len(df)} ZIP codes for {city}")
        
        if df.empty:
            print(f"No ZIPs found for city: {city}")
            return f"No ZIPs found for city: {city}"

        # Filter out ZIP codes with population ≤ 10,000
        df = df[df["population"] > 10000]
        print(f"After population filter: {len(df)} ZIP codes")
        
        if df.empty:
            print(f"No ZIPs found for {city} with population > 10,000")
            return f"No ZIPs found for city: {city} with population > 10,000"

        # Calculate EV count per capita
        df["evs_per_capita"] = df["ev_poi_count"] / (df["population"] + 1)
        
        # Sort by EV count per capita (lowest to highest) and get top_n rows
        top = df.sort_values("evs_per_capita", ascending=True).head(top_n)
        print(f"Top {top_n} underserved ZIP codes:")
        print(top[["ZIP", "population", "ev_poi_count", "evs_per_capita"]])
        
        return top[["ZIP", "population", "ev_poi_count", "evs_per_capita"]].to_markdown(index=False)
    except Exception as e:
        print(f"Error in query_zip_scores: {str(e)}")
        return f"Error processing request: {str(e)}"

# 3️⃣ Get ZIP boundaries for a city (GeoJSON string)
def get_geojson_for_city(city: str) -> str:
    """
    Return a GeoJSON feature collection of ZIP codes for the given city.
    Useful for displaying maps.
    """
    try:
        gdf = load_data()
        
        # Normalize city names (case insensitive matching)
        city = city.strip().lower()  # Ensure leading/trailing spaces are removed and it's lowercase
        
        # Filter the dataset for the city
        city_gdf = gdf[gdf["city"].str.lower() == city]
        
        if city_gdf.empty:
            return f"No ZIPs found for city: {city}"

        return city_gdf.to_json()
    except Exception as e:
        print(f"Error in get_geojson_for_city: {str(e)}")
        return f"Error processing request: {str(e)}"

# 4️⃣ Show all stats for a given ZIP
def get_zip_details(zipcode: Union[str, int]) -> str:
    """
    Return detailed statistics for a specific ZIP code.
    """
    try:
        gdf = load_data()
        row = gdf[gdf["ZIP"].astype(str) == str(zipcode)]
        if row.empty:
            return f"No data found for ZIP code: {zipcode}"
        
        # Check if population is > 10,000
        if row["population"].iloc[0] <= 10000:
            return f"ZIP code {zipcode} has population ≤ 10,000 and is excluded from analysis"
        
        fields = ["ZIP", "city", "population", "ev_poi_count", "evs_per_capita"]
        return row[fields].to_markdown(index=False)
    except Exception as e:
        print(f"Error in get_zip_details: {str(e)}")
        return f"Error processing request: {str(e)}"

# Create tool versions of the functions for the agent
list_cities_tool = tool(list_cities)
query_zip_scores_tool = tool(query_zip_scores)
get_geojson_for_city_tool = tool(get_geojson_for_city)
get_zip_details_tool = tool(get_zip_details)

# Expose both the regular functions and the tool versions
__all__ = [
    'list_cities', 'query_zip_scores', 'get_zip_details', 'get_geojson_for_city',
    'list_cities_tool', 'query_zip_scores_tool', 'get_zip_details_tool', 'get_geojson_for_city_tool'
] 