# Downloading

Downloading resources from Crux.

## Simple file downloading

Download a file to a local path.

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset("A_DATASET_ID")
file = dataset.get_file("/path/to/file.csv")
file.download("/tmp/file.csv")
```

## Use resource ID to download file

Crux files have a resource ID (accessible with `File.id`). That resource ID can be used to get a `File` object. Getting files by resource ID is more efficient than getting them by path.

```python
from crux import Crux

conn = Crux()

file = conn.get_resource("A_CRUX_FILE_RESOURCE_ID")
file.download("/tmp/file.csv")
```

## Download streaming chunks

Download a file in chunks of bytes, for example to stream out while downloading.

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")
file = dataset.get_file(path="/path/to/file.csv")
ten_mb = 10 * 1024 * 1024
stream = file.iter_content(chunk_size=ten_mb)
try:
    with open("/tmp/save", "wb") as fh:
        for chunk in stream:
            fh.write(chunk)
finally:
    stream.close()
```

## Download all files in a folder

Download all files in a Crux dataset folder to a local directory.

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")

downloaded_file_list = dataset.download_files(
    folder="/some_folder",
    local_path="/tmp/data_directory"
)

for file_path in downloaded_file_list:
    print(file_path)
```
