import geopandas as gpd
from typing import List, Union
from langchain.tools import tool
import os

# Global cache (so tools don't reload on every call)
ZIP_DATA_PATH = "outputs/zip_ev_score_enriched.geojson"
_gdf = None

def load_data():
    global _gdf
    if _gdf is None:
        print(f"Loading data from: {os.path.abspath(ZIP_DATA_PATH)}")
        if not os.path.exists(ZIP_DATA_PATH):
            print(f"ERROR: Data file not found at {ZIP_DATA_PATH}")
            return None
        try:
            _gdf = gpd.read_file(ZIP_DATA_PATH)
            print(f"Data loaded successfully. Shape: {_gdf.shape}")
            print(f"Available columns: {_gdf.columns.tolist()}")
            print(f"Available cities: {sorted(_gdf['city'].dropna().unique().tolist())[:5]} ...")
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return None
    return _gdf

# 1️⃣ List all unique cities
@tool
def list_cities() -> List[str]:
    """List all available cities in the ZIP-level EV data."""
    gdf = load_data()
    if gdf is None:
        return ["ERROR: Could not load data file"]
    return sorted(gdf["city"].dropna().unique().tolist())

# 2️⃣ Query underserved ZIPs in a city
@tool
def query_zip_scores(city: str) -> str:
    """
    Return ZIP codes for a given city with population > 10,000, sorted by EV count per capita (lowest to highest).
    Args:
        city: The name of the city to query
    """
    gdf = load_data()
    if gdf is None:
        return "ERROR: Could not load data file"
    
    # Normalize city names (case insensitive matching)
    city = city.strip().lower()  # Ensure leading/trailing spaces are removed and it's lowercase
    print(f"Querying for city: {city}")
    
    # Filter the dataset for the city
    df = gdf[gdf["city"].str.lower() == city]
    print(f"Found {len(df)} ZIP codes for {city}")
    
    if df.empty:
        return f"No ZIPs found for city: {city}"

    # Filter out ZIP codes with population ≤ 10,000
    df = df[df["population"] > 10000]
    print(f"Found {len(df)} ZIP codes with population > 10,000")
    
    if df.empty:
        return f"No ZIPs found for city: {city} with population > 10,000"

    # Calculate EV count per capita
    df["evs_per_capita"] = df["ev_poi_count"] / (df["population"] + 1)
    
    # Sort by EV count per capita (lowest to highest) and get top 5 rows
    top = df.sort_values("evs_per_capita", ascending=True).head(5)
    print(f"Top underserved ZIP codes:")
    print(top[["ZIP", "population", "ev_poi_count", "evs_per_capita"]].to_string())
    
    return top[["ZIP", "population", "ev_poi_count", "evs_per_capita"]].to_markdown(index=False)

# 3️⃣ Get ZIP boundaries for a city (GeoJSON string)
@tool
def get_geojson_for_city(city: str) -> str:
    """
    Return a GeoJSON feature collection of ZIP codes for the given city.
    Useful for displaying maps.
    """
    gdf = load_data()
    
    # Normalize city names (case insensitive matching)
    city = city.strip().lower()  # Ensure leading/trailing spaces are removed and it's lowercase
    
    # Filter the dataset for the city
    city_gdf = gdf[gdf["city"].str.lower() == city]
    
    if city_gdf.empty:
        return f"No ZIPs found for city: {city}"

    return city_gdf.to_json()

# 4️⃣ Show all stats for a given ZIP
@tool
def get_zip_details(zipcode: Union[str, int]) -> str:
    """
    Return detailed statistics for a specific ZIP code.
    Args:
        zipcode: The ZIP code to get details for
    """
    gdf = load_data()
    if gdf is None:
        return "ERROR: Could not load data file"
        
    print(f"Getting details for ZIP: {zipcode}")
    row = gdf[gdf["ZIP"].astype(str) == str(zipcode)]
    
    if row.empty:
        print(f"No data found for ZIP code: {zipcode}")
        return f"No data found for ZIP code: {zipcode}"
    
    # Check if population is > 10,000
    if row["population"].iloc[0] <= 10000:
        print(f"ZIP {zipcode} excluded: population ≤ 10,000")
        return f"ZIP code {zipcode} has population ≤ 10,000 and is excluded from analysis"
    
    fields = ["ZIP", "city", "population", "ev_poi_count", "evs_per_capita"]
    return row[fields].to_markdown(index=False)
