from tools import list_cities, query_zip_scores, get_geojson_for_city, get_zip_details

def test_tools():
    # Test 1: List all cities
    print("\n=== Testing list_cities() ===")
    cities = list_cities.invoke({})  # Empty dict for tools that don't need input
    print(f"Available cities: {cities}")
    
    # Test 2: Query ZIP scores for a city
    print("\n=== Testing query_zip_scores() ===")
    test_city = "Austin"  # You can change this to any city from the list above
    zip_scores = query_zip_scores.invoke({"city": test_city, "top_n": 3})
    print(f"Top 3 underserved ZIPs in {test_city}:")
    print(zip_scores)
    
    # Test 3: Get GeoJSON for a city
    print("\n=== Testing get_geojson_for_city() ===")
    geojson = get_geojson_for_city.invoke({"city": test_city})
    print(f"GeoJSON for {test_city} (first 200 chars):")
    print(geojson[:200] + "...")
    
    # Test 4: Get ZIP details
    print("\n=== Testing get_zip_details() ===")
    # Get a ZIP code from the previous results
    if "ZIP" in zip_scores:
        # Split the markdown table into lines
        lines = zip_scores.split('\n')
        if len(lines) >= 3:  # We need at least header, separator, and one data row
            # Get the first data row (index 2)
            first_row = lines[2]
            # Split by | and get the ZIP code (first column after header)
            test_zip = first_row.split('|')[1].strip()
            print(f"Testing with ZIP code: {test_zip}")
            zip_details = get_zip_details.invoke({"zipcode": test_zip})
            print(f"Details for ZIP {test_zip}:")
            print(zip_details)
        else:
            print("No ZIP codes found in the results")

if __name__ == "__main__":
    test_tools() 