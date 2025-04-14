import geopandas as gpd
import os

# Paths
tracts_fp = "data/census/merged_tracts_tx.geojson"
ev_fp = "data/orbis/ev_charging_location.parquet"
admin_fp = "data/overture/admin_tx.parquet"
output_fp = "outputs/admin_ev_demographics.geojson"

# Load data
tracts = gpd.read_file(tracts_fp).to_crs("EPSG:4326")
ev = gpd.read_parquet(ev_fp).to_crs("EPSG:4326")
admin = gpd.read_parquet(admin_fp).to_crs("EPSG:4326")

# Filter admin
admin = admin[admin["subtype"].isin(["city", "county", "municipality", "place"])]

# Join EVs → Tracts
ev_in_tracts = gpd.sjoin(ev, tracts, predicate="within")
ev_counts = ev_in_tracts.groupby("GEOID").size().reset_index(name="ev_poi_count")
tracts = tracts.merge(ev_counts, on="GEOID", how="left").fillna(0)

# Join Tracts → Admin
tracts_admin = gpd.sjoin(tracts, admin, predicate="intersects")
tracts_admin = tracts_admin[["GEOID", "population", "median_income", "ev_poi_count", "name", "subtype"]]

# Aggregate by admin region
summary = tracts_admin.groupby(["name", "subtype"]).agg(
    total_population=("population", "sum"),
    average_income=("median_income", "mean"),
    ev_poi_count=("ev_poi_count", "sum")
).reset_index()

admin_summary = admin.merge(summary, on=["name", "subtype"], how="left")
admin_summary["ev_poi_count"] = admin_summary["ev_poi_count"].fillna(0).astype(int)
admin_summary["total_population"] = admin_summary["total_population"].fillna(0).astype(int)
admin_summary["average_income"] = admin_summary["average_income"].fillna(0).round(2)

# Save
os.makedirs("outputs", exist_ok=True)
admin_summary.to_file(output_fp, driver="GeoJSON")
print(f"✅ Saved: {output_fp}")
