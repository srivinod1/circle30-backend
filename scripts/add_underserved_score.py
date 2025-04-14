import geopandas as gpd
import os
import pandas as pd

# Input files
tract_fp = "outputs/ev_count_by_tract.geojson"
admin_fp = "outputs/admin_ev_demographics.geojson"

# Output files
tract_out = "outputs/ev_tracts_with_score.geojson"
admin_out = "outputs/admin_with_score.geojson"

# === TRACT-LEVEL PROCESSING ===
print("📍 Processing tract-level underserved scores...")
tracts = gpd.read_file(tract_fp)

# Fill missing with 0s
tracts["population"] = tracts["population"].fillna(0)
tracts["median_income"] = tracts["median_income"].fillna(0)
tracts["ev_poi_count"] = tracts["ev_poi_count"].fillna(0)

# Score 1: Access relative to population (lower = underserved)
tracts["population_score"] = (tracts["ev_poi_count"] + 1) / (tracts["population"].replace(0, 1) + 1)

# Score 2: Access relative to income (lower = underserved, more equitable need)
tracts["equity_score"] = (tracts["median_income"] + 1) / (tracts["ev_poi_count"] + 1)

# Round scores
tracts["population_score"] = tracts["population_score"].round(4)
tracts["equity_score"] = tracts["equity_score"].round(4)

# Save
os.makedirs("outputs", exist_ok=True)
tracts.to_file(tract_out, driver="GeoJSON")
print(f"✅ Tract scores saved to: {tract_out}")


# === ADMIN-LEVEL PROCESSING ===
print("📍 Processing admin-level underserved scores...")
admin = gpd.read_file(admin_fp)

# Fill missing with 0s
admin["total_population"] = admin["total_population"].fillna(0)
admin["average_income"] = admin["average_income"].fillna(0)
admin["ev_poi_count"] = admin["ev_poi_count"].fillna(0)

# Score 1: Access relative to population
admin["population_score"] = (admin["ev_poi_count"] + 1) / (admin["total_population"].replace(0, 1) + 1)

# Score 2: Access relative to income
admin["equity_score"] = (admin["average_income"] + 1) / (admin["ev_poi_count"] + 1)

# Round scores
admin["population_score"] = admin["population_score"].round(4)
admin["equity_score"] = admin["equity_score"].round(4)

# Save
admin.to_file(admin_out, driver="GeoJSON")
print(f"✅ Admin scores saved to: {admin_out}")
