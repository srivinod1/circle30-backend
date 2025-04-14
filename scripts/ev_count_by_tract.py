import geopandas as gpd
import os

# Paths
tracts_fp = "data/census/merged_tracts_tx.geojson"
ev_fp = "data/orbis/ev_charging_location.parquet"
output_fp = "outputs/ev_count_by_tract.geojson"

# Load datasets
tracts = gpd.read_file(tracts_fp).to_crs("EPSG:4326")
ev = gpd.read_parquet(ev_fp).to_crs("EPSG:4326")

# Join EVs to tracts
print("🔗 Joining EV POIs to census tracts...")
joined = gpd.sjoin(ev, tracts, predicate="within")

# Count EVs per tract
ev_counts = joined.groupby("GEOID").size().reset_index(name="ev_poi_count")
tracts = tracts.merge(ev_counts, on="GEOID", how="left")
tracts["ev_poi_count"] = tracts["ev_poi_count"].fillna(0).astype(int)

# Save
os.makedirs("outputs", exist_ok=True)
tracts.to_file(output_fp, driver="GeoJSON")
print(f"✅ Saved: {output_fp}")
