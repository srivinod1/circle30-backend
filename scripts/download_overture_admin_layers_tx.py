import duckdb
import os

# ✅ Ensure output folder exists
os.makedirs("data/overture", exist_ok=True)

# ✅ Define Texas bounding box
bbox = {
    "min_lon": -106.65,
    "max_lon": -93.51,
    "min_lat": 25.84,
    "max_lat": 36.5
}

# ✅ Load required extensions
duckdb.sql("""
INSTALL httpfs;
INSTALL spatial;
INSTALL azure;

LOAD httpfs;
LOAD spatial;
LOAD azure;
""")

duckdb.sql("SET s3_region='us-west-2';")
duckdb.sql("SET azure_storage_connection_string = 'DefaultEndpointsProtocol=https;AccountName=overturemapswestus2;AccountKey=;EndpointSuffix=core.windows.net';")

# ✅ Download Admin Divisions for Texas
print("🗺️  Downloading admin divisions for Texas...")
duckdb.sql(f"""
COPY (
    SELECT
        id,
        division_id,
        names.primary AS name,
        subtype,
        geometry,
        bbox.xmin AS longitude,
        bbox.ymin AS latitude
    FROM read_parquet(
        's3://overturemaps-us-west-2/release/2025-03-19.0/theme=divisions/type=division_area/*',
        filename=true,
        hive_partitioning=1
    )
    WHERE country = 'US'
      AND region = 'US-TX'
      AND bbox.xmin BETWEEN {bbox['min_lon']} AND {bbox['max_lon']}
      AND bbox.ymin BETWEEN {bbox['min_lat']} AND {bbox['max_lat']}
) TO 'data/overture/admin_tx.parquet' (FORMAT 'parquet');
""")

print("✅ Saved: admin_tx.parquet")
