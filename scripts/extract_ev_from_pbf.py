import gzip
import os
import json
from mapbox_vector_tile import decode
from shapely.geometry import shape, mapping
import geopandas as gpd
from pathlib import Path

# Set your path to .pbf tile(s)
tile_path = "/Users/srikanth/Downloads/Orbis-CA/US-TX/orbis_sectioned_25150_000_global_us-tx.osm.pbf"  # replace with real one
output_path = "data/orbis/ev_charging_austin.geojson"
layer_name = "Charging Location"

# Read the .pbf file (may be brotli or gzip encoded)
with open(tile_path, "rb") as f:
    tile_data = f.read()

# Decode tile to extract all layers
tile = decode(tile_data)

# Check available layers
if layer_name not in tile:
    print(f"❌ Layer '{layer_name}' not found in tile.")
    print(f"Available layers: {list(tile.keys())}")
    exit()

features = tile[layer_name]

# Extract features with amenity=charging_location
ev_features = []
for feature in features:
    props = feature["properties"]
    if props.get("amenity") == "charging_location":
        geom = shape(feature["geometry"])
        ev_features.append({
            "type": "Feature",
            "geometry": mapping(geom),
            "properties": props
        })

print(f"✅ Found {len(ev_features)} EV charging stations in this tile.")

# Write to GeoJSON
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w") as f:
    geojson = {
        "type": "FeatureCollection",
        "features": ev_features
    }
    json.dump(geojson, f)

print(f"💾 Saved to {output_path}")
