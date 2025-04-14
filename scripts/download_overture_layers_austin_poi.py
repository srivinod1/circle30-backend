import duckdb
import os

# ✅ Ensure output folder exists
os.makedirs("data/overture", exist_ok=True)

# ✅ Define California bounding box
bbox = {
    "min_lon": -124.48,
    "max_lon": -114.13,
    "min_lat": 32.53,
    "max_lat": 42.01
}

# ✅ Load DuckDB extensions
duckdb.sql("""
INSTALL httpfs;
INSTALL spatial;

LOAD httpfs;
LOAD spatial;
""")

# ✅ Set S3 region
duckdb.sql("SET s3_region='us-west-2';")

# ✅ Download POIs for California
print("📍 Downloading POIs for California from Overture Maps...")
duckdb.sql(f"""
COPY (
    SELECT
        id,
        names.primary AS name,
        categories.primary AS category,
        confidence,
        geometry,
        bbox.xmin AS longitude,
        bbox.ymin AS latitude
    FROM read_parquet(
        's3://overturemaps-us-west-2/release/2025-03-19.0/theme=places/type=place/*',
        filename=true,
        hive_partitioning=1
    )
    WHERE bbox.xmin BETWEEN {bbox['min_lon']} AND {bbox['max_lon']}
      AND bbox.ymin BETWEEN {bbox['min_lat']} AND {bbox['max_lat']}
) TO 'data/overture/places_ca.parquet' (FORMAT 'parquet');
""")

print("✅ Saved: places_ca.parquet")
