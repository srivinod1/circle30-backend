import os
import geopandas as gpd
from typing import List, Union
from langchain.tools import tool
from .storage import storage
import logging

logger = logging.getLogger(__name__)

# Global cache (so tools don't reload on every call)
ZIP_DATA_PATH = "zip_ev_score.geojson"  # Updated file path
_gdf = None

def load_data():
    global _gdf
    if _gdf is None:
        logger.info(f"Loading data from S3: {ZIP_DATA_PATH}")
        local_path = storage.get_file(ZIP_DATA_PATH)
        if not local_path:
            logger.error(f"ERROR: Could not load data file from S3")
            return None
        try:
            logger.info("Reading GeoJSON file with GeoPandas...")
            _gdf = gpd.read_file(local_path)
            logger.info(f"Data loaded successfully. Shape: {_gdf.shape}")
            logger.info(f"Available columns: {_gdf.columns.tolist()}")
            logger.info(f"Available cities: {sorted(_gdf['city'].dropna().unique().tolist())[:5]} ...")
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
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
@tool
def query_zip_scores(city: str) -> str:
    """
    Return ZIP codes for a given city with population > 10,000, sorted by EV count per capita (lowest to highest).
    Args:
        city: The name of the city to query
    """
    try:
        logger.info(f"Querying ZIP scores for city: {city}")
        gdf = load_data()
        if gdf is None:
            logger.error("Failed to load data")
            return "ERROR: Could not load data file"
        
        # Normalize city names (case insensitive matching)
        city = city.strip().lower()
        logger.info(f"Normalized city name: {city}")
        
        # Filter the dataset for the city
        df = gdf[gdf["city"].str.lower() == city]
        logger.info(f"Found {len(df)} ZIP codes for {city}")
        
        if df.empty:
            logger.warning(f"No ZIPs found for city: {city}")
            return f"No ZIPs found for city: {city}"

        # Filter out ZIP codes with population ≤ 10,000
        df = df[df["population"] > 10000]
        logger.info(f"Found {len(df)} ZIP codes with population > 10,000")
        
        if df.empty:
            logger.warning(f"No ZIPs found for city: {city} with population > 10,000")
            return f"No ZIPs found for city: {city} with population > 10,000"

        # Calculate EV count per capita
        df["evs_per_capita"] = df["ev_poi_count"] / (df["population"] + 1)
        
        # Sort by EV count per capita (lowest to highest) and get top 5 rows
        top = df.sort_values("evs_per_capita", ascending=True).head(5)
        logger.info(f"Top underserved ZIP codes:")
        logger.info(top[["ZIP", "population", "ev_poi_count", "evs_per_capita"]].to_string())
        
        return top[["ZIP", "population", "ev_poi_count", "evs_per_capita"]].to_markdown(index=False)
    except Exception as e:
        logger.error(f"Error in query_zip_scores: {str(e)}")
        return f"Error: {str(e)}"

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
get_geojson_for_city_tool = tool(get_geojson_for_city)
get_zip_details_tool = tool(get_zip_details)

# Expose both the regular functions and the tool versions
__all__ = [
    'list_cities', 'query_zip_scores', 'get_zip_details', 'get_geojson_for_city',
    'list_cities_tool', 'get_zip_details_tool', 'get_geojson_for_city_tool'
] 