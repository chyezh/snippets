from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, utility
import time
import random

# Connect to Milvus
connections.connect("default", host="localhost", port="19530")

# Function to create, load, and release collections
def create_load_release_collections(num_collections):
    for i in range(num_collections):
        time.sleep(2)
        collection_name = f"collection_{i+50}"
        
        # Create a multi-shard collection
        shards_num = random.randint(1, 16)  # Random number of shards between 1 and 10
        # Define schema
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=128)
        ]
        schema = CollectionSchema(fields, description=f"Schema for {collection_name}")
        
        # Create collection
        collection = Collection(name=collection_name, schema=schema, shards_num=shards_num)
        print(f"Created collection: {collection_name}")
        
# Create, load, and release 10,000 collections
create_load_release_collections(1000)
