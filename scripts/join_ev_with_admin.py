import geopandas as gpd
import pandas as pd
import os

# ✅ Load admin boundaries
admin_path = "data/overture/admin_tx.parquet"
admin = gpd.read_parquet(admin_path)
admin = admin.to_crs("EPSG:4326")  # Ensure it's lat/lon

# ✅ Load EV charging locations
ev_path = "data/orbis/ev_charging_location.parquet"
ev = gpd.read_parquet(ev_path)
ev = ev.set_geometry("geometry").to_crs("EPSG:4326")

# ✅ Spatial join (find which admin region each EV point belongs to)
print("🔗 Performing spatial join...")
joined = gpd.sjoin(ev, admin, how="inner", predicate="intersects")
print("📦 Joined columns:", joined.columns.tolist())


# ✅ Count EV stations per admin division
counts = joined.groupby("name_right").size().reset_index(name="ev_poi_count")
counts = counts.sort_values(by="ev_poi_count", ascending=False)

# ✅ Save as CSV for inspection
os.makedirs("outputs", exist_ok=True)
counts.to_csv("outputs/ev_count_by_region.csv", index=False)

print("✅ Saved: outputs/ev_count_by_region.csv")
print(counts.head())
