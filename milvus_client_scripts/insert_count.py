from pymilvus import (
    connections,
    FieldSchema, CollectionSchema, DataType, Function, FunctionType,
    Collection,
    utility,
)
import random
import time
HOST = '127.0.0.1'
PORT = '19530'
import json
json_string = json.dumps(1)
print(json_string)


connections.connect(host=HOST, port=PORT)
print(utility.get_server_version())

collection_name = "AAAF"
dim = 2

fields = [
        FieldSchema(name="primary", dtype=DataType.VARCHAR, max_length = 100, is_primary=True, auto_id=False),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dim),
        FieldSchema(name="json", dtype=DataType.JSON), # 新增的 JSON 数据字段
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=1000, enable_analyzer=True),
        FieldSchema(name="sparse", dtype=DataType.SPARSE_FLOAT_VECTOR),
]

bm25_function = Function(
    name="text_bm25_emb", # Function name
    input_field_names=["text"], # Name of the VARCHAR field containing raw text data
    output_field_names=["sparse"], # Name of the SPARSE_FLOAT_VECTOR field reserved to store generated embeddings
    function_type=FunctionType.BM25, # Set to `BM25`
)

schema = CollectionSchema(fields, enable_dynamic_field=True, functions=[bm25_function])

# utility.drop_collection(collection_name)
collection = Collection(collection_name, schema) #
index_param = {'metric_type': 'COSINE', 'params': {'M': 30, 'efConstruction': 200}, 'index_type': 'HNSW'}
collection.create_index("vector", index_param)
collection.create_index("sparse", {
    "index_type": "SPARSE_INVERTED_INDEX",
    "metric_type": "BM25",
    "params": {
        "inverted_index_algo": "DAAT_MAXSCORE",
        "bm25_k1": 1.2,
        "bm25_b": 0.75
    }
})

collection.load()
data = [
    {
        "primary": str(i),
        "vector": [random.random() for _ in range(dim)],
        "json": {
            **({"key_5": "HellonWorld"} if random.random() < 0.4 else {"key_5":0} ),
        },
        "text": "This is a test string with some random content",
    }
    for i in range(0, 20000)
]
# for i in range(0, 10):
#     print(data[i])

# # Shuffle the JSON data
# for item in data:
#     json_keys = list(item["json"].keys())
#     random.shuffle(json_keys)
#     item["json"] = {key: item["json"][key] for key in json_keys}

for i in range(0, len(data), 100000):
        batch_data = data[i:i+10000]
        collection.insert(batch_data)
        # res = collection.query(expr='primary >= "0"', output_fields=["count(*)"], consistency_level="Strong")
        # print("Query result:", res)
        # res = collection.query(expr='', output_fields=["count(*)"], consistency_level="Strong")
        # print("Query result:", res)

collection.drop()

# collection.flush()
# time.sleep(3)

# res = collection.query(expr='1 == 1', output_fields=["count(*)"], consytency_level="Strong")
# print("Query result:", res)
