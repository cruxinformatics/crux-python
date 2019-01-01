# Tables

**TABLES ARE A DEPRECATED FEATURE, DO NOT USE**

## Create, load, and query a table

Create a table, load data into it from a local file, create a query, and run the query.

```python
from crux import Crux

conn = Crux()

dataset = conn.create_dataset(
    name="Example",
    description="A dataset full of examples",
)

file = dataset.upload_file(
    path="/path/to/remote/file.csv",
    local_path="/tmp/local_file.csv"
)

table_config = {
    "schema": [
        {
            "name": "bank",
            "type": "string",
        },
        {
            "name": "location",
            "type": "string",
        },
    ]
}

table = dataset.create_table(
    path="/path/to/table",
    config=table_config
)

job = dataset.load_table_from_file(
    source_file=file,
    dest_table=table,
    append=False
)

print(job.job_id, job.job_url)

query_config = {
    "query": "SELECT * FROM bank_table",
}

query = dataset.create_query(
    path="/path/to/query",
    config=query_config
)

data = query.run(format="csv", chunk_size=1024, decode_unicode=True)

for chunk in data:
    print(chunk)
```

## Run an existing query

Get and run an existing query.

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")
query = dataset.get_query(path="/path/to/query")
data = query.run(format="csv", chunk_size=1024, decode_unicode=True)

for chunk in data:
    print(chunk)
```

## Upload query and download results

Upload a .sql file as a query, and download the contents as a file.

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")

query = dataset.upload_query(
    path="/path/to/query",
    sql_file="/tmp/query.sql"
)

downloaded = query.download(local_path="/tmp/downloaded_query.csv")

if downloaded:
    print("Query output downloaded successfully")
```
