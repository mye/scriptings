import weaviate
import json

client = weaviate.Client(url = "http://[::]:8080")

f='/home/lo/local/pydocs/python-3.10.11-docs-text/library/json.json'
data = json.load(open(f))

with client.batch as batch:
    batch.batch_size = 100
    for i, d in enumerate(data):
        print(f"importing passage: {i+1}")

        properties = {
            "backlink": d["backlink"],
            "passage": d["passage"]
        }

        client.batch.add_data_object(properties, "pydoc")