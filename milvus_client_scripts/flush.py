from pymilvus import connections, Collection

def flush_collection(collection_name: str, host: str = "localhost", port: str = "19530"):
    """
    Flush a Milvus collection to ensure all data is persisted to disk.
    
    Args:
        collection_name (str): Name of the collection to flush
        host (str): Milvus server host
        port (str): Milvus server port
    """
    try:
        # Connect to Milvus server
        connections.connect(host=host, port=port)
        print(f"Connected to Milvus server at {host}:{port}")
        
        # Get the collection
        collection = Collection(collection_name)
        print(f"Got collection: {collection_name}")
        
        # Flush the collection
        collection.flush()
        print(f"Successfully flushed collection: {collection_name}")
        
    except Exception as e:
        print(f"Error flushing collection: {str(e)}")
    finally:
        # Disconnect from Milvus server
        connections.disconnect("default")
        print("Disconnected from Milvus server")

if __name__ == "__main__":
    # Example usage
    collection_name = "fouram_CaUszFZ8"  # Replace with your collection name
    flush_collection(collection_name, host="10.104.26.93")
