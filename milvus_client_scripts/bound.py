from pymilvus import MilvusClient, Function, FunctionType
import random

client = MilvusClient(uri="http://localhost:19530")

client.drop_collection("test")
client.create_collection(
    collection_name="test",
    dimension=1024,  # The vectors we will use in this demo has 768 dimensions
    auto_id=True,
)
docs = [
    "Artificial intelligence was founded as an academic discipline in 1956.",
    "Alan Turing was the first person to conduct substantial research in AI.",
    "Born in Maida Vale, London, Turing was raised in southern England.",
]
# # Use fake representation with random vectors (768 dimension).
vectors = [[random.uniform(-1, 1) for _ in range(1024)] for _ in docs]
data = [
    {
        "vector": vectors[i],
        "text": docs[i],
        "metadata": {"domain": "history"},
    }
    for i in range(len(vectors))
]

for i in range(1000):
    res = client.insert(collection_name="test", data=data)
print(res)

results = client.query(collection_name="test", output_fields=["count(*)"])
# Extract the count from the query results
print(results[0]["count(*)"])

client.flush(collection_name="test")
print(client.get_collection_stats("test"))