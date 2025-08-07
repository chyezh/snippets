from pymilvus import connections, utility, Collection


# Release collection from memory
def release_collection(collection_name):
    if not utility.has_collection(collection_name):
        print(f"Collection '{collection_name}' does not exist.")
        return
    
    utility.load_state(collection_name)
    if utility.load_state(collection_name):
        collection = Collection(collection_name)
        collection.release()
        print(f"Collection '{collection_name}' released from memory.")
    else:
        print(f"Collection '{collection_name}' is not loaded in memory.")

def load_collection(collection_name):
    if not utility.has_collection(collection_name):
        print(f"Collection '{collection_name}' does not exist.")
        return
    
    utility.load_state(collection_name)
    collection = Collection(collection_name)
    collection.load()
    print(f"Collection '{collection_name}' loaded into memory.")

# Example usage
if __name__ == "__main__":
    # Connect to Milvus server
    connections.connect("default", host="10.104.26.93", port="19530")

    COLLECTION_NAME = "fouram_CaUszFZ8"  # Replace with your collection name
    release_collection(COLLECTION_NAME)
    load_collection(COLLECTION_NAME)

    # Disconnect from Milvus server
    connections.disconnect("default")
