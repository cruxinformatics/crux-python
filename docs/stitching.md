# Stitching

Stitch Avro resources in Crux Dataset.

```python
from crux import Crux

conn = Crux()


dataset_object = conn.get_dataset(id="567890")

destination_file = dataset_object.create_file(
    path="/test_destination_file.avro",
    description="test_destination_description",
    tags=["tags1", "tags2"]
)

file_object = dataset_object.upload_file(
    tags=["test_tag1"],
    description="test_description",
    path="/twitter.avro",
    local_path="/tmp/twitter.avro"
    )

file_object2 = dataset_object.upload_file(
    tags=["test_tag1"],
    description="test_description",
    path="/twitter2.avro",
    local_path="/tmp/twitter2.avro"
    )


file_obj, job_id = dataset_object.stitch(
    source_resources = [
        "/twitter.avro",
        "/twitter2.avro"
    ],
    destination_resource = "/test_destination_file.avro",
    labels = {
        "test_label1": "test_value1"
    }
)

# OR

file_obj, job_id = dataset_object.stitch(
    source_resources = [
        file_object,
        file_object2
    ],
    destination_resource = destination_file,
    labels = {
        "test_label1": "test_value1"
    }
)

if file_obj.download(local_path="/tmp/stitched_twitter.avro", content_type="avro/binary"):
    print("Downloaded the file")

job = datast_object.get_stitch_job(job_id)
print(job.status)
```
