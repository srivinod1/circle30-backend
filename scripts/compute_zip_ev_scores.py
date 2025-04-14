import geopandas as gpd
import pandas as pd
import os

# === Load ZIP shapefile with population ===
zip_fp = "outputs/merged_zips_tx.geojson"
zips = gpd.read_file(zip_fp).to_crs("EPSG:4326")

# === Load EV POIs ===
ev_fp = "data/orbis/ev_charging_location.parquet"
ev = gpd.read_parquet(ev_fp).to_crs("EPSG:4326")

# === Spatial join to count EVs per ZIP ===
print("🔗 Performing spatial join to count EVs...")
joined = gpd.sjoin(ev, zips, how="inner", predicate="within")
counts = joined.groupby("ZIP").size().reset_index(name="ev_poi_count")

# === Merge counts back into ZIPs ===
zips = zips.merge(counts, on="ZIP", how="left")
zips["ev_poi_count"] = zips["ev_poi_count"].fillna(0)

# === Compute underserved scores ===
zips["evs_per_capita"] = zips["ev_poi_count"] / (zips["population"] + 1)
zips["area_km2"] = zips.geometry.to_crs(epsg=3857).area / 1e6
zips["evs_per_km2"] = zips["ev_poi_count"] / (zips["area_km2"] + 1)

# Optional: Normalize or combine into a single score if needed
zips["underserved_score"] = 1 / (zips["evs_per_capita"] + 0.001) + 1 / (zips["evs_per_km2"] + 0.001)

# === Save result ===
os.makedirs("outputs", exist_ok=True)
zips.to_file("outputs/zip_ev_score.geojson", driver="GeoJSON")
zips.sort_values("underserved_score", ascending=False).to_csv("outputs/ev_zip_underserved_ranking.csv", index=False)

print("✅ Saved: outputs/zip_ev_score.geojson and CSV")
