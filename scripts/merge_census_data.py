import geopandas as gpd
import pandas as pd
import os

# === Filepaths ===
zip_fp = "data/census/tl_2024_us_zcta520.shp"
population_fp = "data/census/ACS_B01003_TX.csv"
output_fp = "data/census/merged_zips_tx.geojson"

# === Load shapefile ===
print("📦 Loading ZIP geometries...")
zips = gpd.read_file(zip_fp).to_crs("EPSG:4326")
zips = zips.rename(columns={"ZCTA5CE20": "ZIP"})

# === Load population CSV ===
print("👥 Loading population data...")
population = pd.read_csv(population_fp, dtype=str)
population = population[population["GEO_ID"].str.contains("1400000US") == False]
population["ZIP"] = population["GEO_ID"].str[-5:]
population["population"] = pd.to_numeric(population["B01003_001E"], errors="coerce").fillna(0).astype(int)

# === Merge ===
print("🔗 Merging population with ZIPs...")
merged = zips.merge(population[["ZIP", "population"]], on="ZIP", how="left")
merged["population"] = merged["population"].fillna(0).astype(int)

# === Save ===
print("💾 Saving merged file...")
os.makedirs("data/census", exist_ok=True)
merged.to_file(output_fp, driver="GeoJSON")
print(f"✅ Done: {output_fp}")
