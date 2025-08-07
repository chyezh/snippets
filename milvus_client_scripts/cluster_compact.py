from pymilvus import *
import numpy as np
import random
import string
import time
from pymilvus.grpc_gen import common_pb2

ConsistencyLevel = common_pb2.ConsistencyLevel

collection_name = "hello_milvus_float16"
# collection_name = "fouram_O6fYsaOS"
dim = 128
batch = 10000
batch_count = 20

client = MilvusClient()
connections.connect("default", host="localhost", port="19530")
# connections.connect("default", host="10.104.15.215", port="19530")
# client = MilvusClient("http://10.104.21.146:19530")


def prepare_collection():
    print("drop old collection...")
    client.drop_collection(collection_name)
    print("drop old collection done")

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name="timestamp", dtype=DataType.INT64, is_clustering_key=True),
        FieldSchema(name="float", dtype=DataType.FLOAT),
        FieldSchema(name="varchar", dtype=DataType.VARCHAR, max_length=1024,enable_match=True, enable_analyzer=True),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dim),
    ]
    schema = CollectionSchema(fields=fields, description=f"hello milvus", auto_id=False, enable_dynamic_field=True)
    index_params = client.prepare_index_params()
    index_params.add_index(
        field_name="vector",
        index_type="IVF_SQ8",
        index_name="vector",
        metric_type="L2",
    )

    client.create_collection(
        collection_name, dimension=dim, metric_type="L2", schema=schema, shards_num=1,
        consistency_level=ConsistencyLevel.Session, index_params=index_params,
    )


def insert():
    _len = int(20)
    _str = string.ascii_letters + string.digits + " "
    _s = _str
    print("_str size ", len(_str))

    for i in range(int(_len / len(_str))):
        _s += _str
        print("append str ", i)
    values = [''.join(random.sample(_s, _len - 1)) for _ in range(batch)]

    i = 0
    while i < batch_count:
        # insert data
        data = [
            [i*batch+j for j in range(batch)],  # id
            [j for j in range(batch)],  # timestamp
            [random.random() for _ in range(batch)], #float
            [[random.random() for _ in range(dim)] for _ in range(batch)],  # vector
        ]

        start = time.time()
        try:
            # _, vectors = gen_fp16_vectors(batch, dim)
            rows = [{"id": data[0][i], "vector": data[3][i], "timestamp": data[1][i], "float": data[2][i],
                     "varchar": f"FLrjqelpnB3b6ZKOWUZY9iV1JIb829iNyFH4V75CR7DzNKmTaUx5lgScA3QQXpazHsyAekk20uBMhhdfTPvomYDr1LvgPcoGW0E{data[0][i]}"}
                    for i in range(batch)]
            # rows = [{"id": data[0][i], "vector": data[1][i]} for i in range(batch)]

            insert_result = client.insert(collection_name, rows)
        except Exception as e:
            print("insert failed: ", e)
        dur = time.time() - start
        print("insert %d %d done in %f" % (i, batch, dur))
        i += 1
    client.flush(collection_name)
    print(f"Number of entities in Milvus: {client.get_collection_stats(collection_name)}")  # check the num_entites


def query_with_expr():
    start = time.time()
    query_expr = "id < 10"
    res = client.query(collection_name, query_expr, output_fields=["id"])
    print(query_expr)
    print(res)
    print("query cost", time.time() - start)


def search_with_expr():
    exprs = [
        "timestamp > 5",
        "timestamp + 1 > 5",
        # "timestamp > 5.5",
        # "timestamp + 1> 5.5",
        "float + 1 < 2",
        "timestamp + 1.1 == 2.1",
    ]
    vectors = [[random.random() for _ in range(dim)] for _ in range(10)]
    for search_expr in exprs:
        print(search_expr)
        res = client.search(collection_name, vectors, filter=search_expr, output_fields=["id", "timestamp"],
                            anns_field="vector")
        print(res)
        print("pytorch Tensor: ", torch.frombuffer(res[0][0].get("bfloat16_vector"), dtype=torch.bfloat16))


fp16_little = np.dtype('e').newbyteorder('<')


def gen_fp16_vectors(num, dim):
    raw_vectors = []
    fp16_vectors = []
    for _ in range(num):
        raw_vector = [random.random() for _ in range(dim)]
        raw_vectors.append(raw_vector)
        fp16_vector = np.array(raw_vector, dtype=fp16_little)
        fp16_vectors.append(fp16_vector)
    return raw_vectors, fp16_vectors


def gen_bf16_vectors(num, dim):
    raw_vectors = []
    bf16_vectors = []
    for _ in range(num):
        raw_vector = [random.random() for _ in range(dim)]
        raw_vectors.append(raw_vector)
        # Numpy itself does not support bfloat16, use TensorFlow extension instead.
        # PyTorch does not support converting bfloat16 vector to numpy array.
        # See:
        # - https://github.com/numpy/numpy/issues/19808
        # - https://github.com/pytorch/pytorch/issues/90574
        bf16_vector = tf.cast(raw_vector, dtype=tf.bfloat16).numpy()
        bf16_vectors.append(bf16_vector)
    return raw_vectors, bf16_vectors


if __name__ == "__main__":
    # prepare_collection()

    # insert()
    # index_params = client.prepare_index_params()
    # index_params.add_index(
    #     field_name="vector",
    #     index_type="IVF_SQ8",
    #     index_name="vector",
    #     metric_type="L2",
    # )
    # start = time.time()
    # client.create_index(collection_name, index_params=index_params)
    # end = time.time()
    # # print("index cost: ", end-start)
    # # time.sleep(5)
    client.compact(collection_name, is_clustering=True)
    # end2 = time.time()
    # print("clustering compaction cost: ", end2-end)

    # client.release_collection(collection_name)

    #
    # client.load_collection(collection_name)
    #
    # # query_with_expr()
    #
    # search_with_expr()

    # hybrid_search()
