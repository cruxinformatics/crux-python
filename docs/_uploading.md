# Uploading

Uploading resources to Crux.

## Upload single file

Upload a local file to Crux.

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset("A_DATASET_ID")
file = dataset.upload_file(
    "/tmp/local/file.avro",
    "/crux/path/file.avro",
)
```

## Upload files in a directory

Upload all files in a local directory to a folder in a dataset on Crux.

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")

uploaded_file_objects = dataset.upload_files(
    local_path="/tmp/local_directory",
    folder="/some_folder"
)

for file_object in uploaded_file_objects:
    print(file_object.name)
```
