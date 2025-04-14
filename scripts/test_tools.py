import sys
import os

# Add the circle30-backend folder to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools import list_cities, query_zip_scores, get_geojson_for_city, get_zip_details

# Test list_cities tool
cities = list_cities.invoke(input="")  # Provide empty string if no input is required
print("Cities:", cities)

# Test query_zip_scores for Austin (Top 3)
zip_scores = query_zip_scores.invoke(input="Austin, 3")  # Pass city and top_n as input
print("Austin Zip Scores:", zip_scores)

# Test get_geojson_for_city for Austin
geojson = get_geojson_for_city.invoke(input="Austin")  # Just pass the city
print("Austin GeoJSON:", geojson)

# Test get_zip_details for a specific ZIP
zip_details = get_zip_details.invoke(input="78701")  # Replace with a valid ZIP code
print("Zip Details for 78701:", zip_details)
