from pymilvus import connections, Collection, utility

# Step 1: Connect to the Milvus server
def connect_to_milvus(host='localhost', port='19530'):
    print("Connecting to Milvus...")
    connections.connect(host=host, port=port)
    print("Connected to Milvus!")

# Step 2: Count the number of entities in a collection using query
def count_entities(collection_name):
    # Check if the collection exists
    if not utility.has_collection(collection_name):
        print(f"Collection '{collection_name}' does not exist.")
        return

    # Load the collection
    collection = Collection(collection_name)
    collection.load()

    # Query to count all entities
    expr = "900000<=id<1000000"  # A filter that matches all entities
    results = collection.query(expr=expr, output_fields=["count(*)"])
    
    # Extract the count from the query results
    num_entities = results[0]["count(*)"]
    print(f"Number of entities in collection '{collection_name}': {num_entities}")

# Main function
if __name__ == "__main__":
    # Milvus connection parameters
    HOST = '10.104.24.90'  # Milvus server address
    PORT = '19530'      # Milvus server port

    # Collection name
    COLLECTION_NAME = 'fouram_igMEwJbQ'  # Replace with your collection name

    # Connect to Milvus
    connect_to_milvus(host=HOST, port=PORT)

    # Count entities in the collection using query
    count_entities(COLLECTION_NAME)
