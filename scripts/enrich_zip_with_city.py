import geopandas as gpd
import os

# Paths
zip_fp = "outputs/zip_ev_score.geojson"
admin_fp = "data/overture/admin_tx.parquet"
output_fp = "outputs/zip_ev_score_enriched.geojson"

# Load data
print("📦 Loading ZIP and admin boundaries...")
zips = gpd.read_file(zip_fp).to_crs("EPSG:4326")
admin = gpd.read_parquet(admin_fp).to_crs("EPSG:4326")

# Filter to city/locality-level polygons
cities = admin[admin["subtype"] == "locality"]

# Spatial join: assign city name to each ZIP
print("🔗 Performing spatial join to assign city names...")
joined = gpd.sjoin(zips, cities[["name", "geometry"]], how="left", predicate="intersects")
joined.rename(columns={"name": "city"}, inplace=True)

# Save result
print("💾 Saving enriched ZIPs with city name...")
os.makedirs("outputs", exist_ok=True)
joined.to_file(output_fp, driver="GeoJSON")
print(f"✅ Saved: {output_fp}")
