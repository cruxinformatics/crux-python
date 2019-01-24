# Labels

## Add Label to Existing Dataset

```python
from crux import Crux
from crux.exceptions import CruxAPIException, CruxClientException

# Set the `CRUX_API_KEY`, `CRUX_API_HOST` environment variables.
# By default `CRUX_API_HOST` will point to Production environment
conn = Crux()

# Custom connection attributes can be set via following

conn = Crux(api_key="123456789", api_host="https://api.example.com")

try:
    dataset_object = conn.get_dataset(id="567890")

    if dataset_object.add_label("test_label1", "test_value1"):
        print("Label added to Dataset")

except CruxAPIException as err:
    print(err.status_code, err.error_message)
except CruxClientException as err:
    print(err.message)
```

## Get Label from Dataset

```python
from crux import Crux
from crux.exceptions import CruxAPIException, CruxClientException

# Set the `CRUX_API_KEY`, `CRUX_API_HOST` environment variables.
# By default `CRUX_API_HOST` will point to Production environment
conn = Crux()

# Custom connection attributes can be set via following

conn = Crux(api_key="123456789", api_host="https://api.example.com")

try:
    dataset_object = conn.get_dataset(id="567890")

    label = dataset_object.get_label("test_label1")

    print(label.label_key, label.label_value)

except CruxAPIException as err:
    print(err.status_code, err.error_message)
except CruxClientException as err:
    print(err.message)
```

## Delete Label from Dataset

```python
from crux import Crux
from crux.exceptions import CruxAPIException, CruxClientException

# Set the `CRUX_API_KEY`, `CRUX_API_HOST` environment variables.
# By default `CRUX_API_HOST` will point to Production environment
conn = Crux()

# Custom connection attributes can be set via following

conn = Crux(api_key="123456789", api_host="https://api.example.com")

try:
    dataset_object = conn.get_dataset(id="567890")

    if dataset_object.delete_label("test_label1"):
        print("Label Deleted from Dataset")

except CruxAPIException as err:
    print(err.status_code, err.error_message)
except CruxClientException as err:
    print(err.message)
```

## Search Resources in Dataset by Label

```python
from crux import Crux
from crux.exceptions import CruxAPIException, CruxClientException

# Set the `CRUX_API_KEY`, `CRUX_API_HOST` environment variables.
# By default `CRUX_API_HOST` will point to Production environment
conn = Crux()

# Custom connection attributes can be set via following

conn = Crux(api_key="123456789", api_host="https://api.example.com")

try:
    dataset_object = conn.get_dataset(id="567890")

    predicates=[
        {"op":"eq","key":"test_label1","val":"test_value1"}
    ]

    resource_list = dataset_object.find_resources_by_label(predicates=predicates)

    for resource in resource_list:
        resource.download(local_path="/tmp/{file_name}".format(resource.name))

except CruxAPIException as err:
    print(err.status_code, err.error_message)
except CruxClientException as err:
    print(err.message)
```

## Add Label to Resource

```python
from crux import Crux
from crux.exceptions import CruxAPIException, CruxClientException

# Set the `CRUX_API_KEY`, `CRUX_API_HOST` environment variables.
# By default `CRUX_API_HOST` will point to Production environment
conn = Crux()

# Custom connection attributes can be set via following

conn = Crux(api_key="123456789", api_host="https://api.example.com")

try:
    dataset_object = conn.get_dataset(id="567890")

    file_object = dataset_object.upload_file(
            tags=["test_tag1"],
            description="test_description",
            path="/test_folder1/test_folder2/test_file.csv",
            local_path="/tmp/test_file.csv"
            )

    file_object2 = dataset_object.upload_file(
        tags=["test_tag1"],
        description="test_description",
        path="/test_folder1/test_folder2/test_file2.csv",
        local_path="/tmp/test_file.csv"
        )

    if file_object.add_label("test_label1", "test_value1"):
        print("Label added to resource")
    if file_object2.add_label("test_label1", "test_value1"):
        print("Label added to resource")

except CruxAPIException as err:
    print(err.status_code, err.error_message)
except CruxClientException as err:
    print(err.message)
```

## Get Label from Resource

```python
from crux import Crux
from crux.exceptions import CruxAPIException, CruxClientException

# Set the `CRUX_API_KEY`, `CRUX_API_HOST` environment variables.
# By default `CRUX_API_HOST` will point to Production environment
conn = Crux()

# Custom connection attributes can be set via following

conn = Crux(api_key="123456789", api_host="https://api.example.com")

try:
    dataset_object = conn.get_dataset(id="567890")

    file_object = dataset_object.get_file(path="/test_folder1/test_folder2/test_file.csv")
    file_object2 = dataset_object.get_file(path="/test_folder1/test_folder2/test_file2.csv")

    print(file_object.labels.get("test_label1"))
    print(file_object2.labels.get("test_label1))

except CruxAPIException as err:
    print(err.status_code, err.error_message)
except CruxClientException as err:
    print(err.message)
```

## Delete Label from Resource

```python
from crux import Crux
from crux.exceptions import CruxAPIException, CruxClientException

# Set the `CRUX_API_KEY`, `CRUX_API_HOST` environment variables.
# By default `CRUX_API_HOST` will point to Production environment
conn = Crux()

# Custom connection attributes can be set via following

conn = Crux(api_key="123456789", api_host="https://api.example.com")

try:
    dataset_object = conn.get_dataset(id="567890")

    file_object = dataset_object.get_file(path="/test_folder1/test_folder2/test_file.csv")
    file_object2 = dataset_object.get_file(path="/test_folder1/test_folder2/test_file2.csv")

    if file_object.delete_label("test_label1"):
        print("Label Deleted from Resource")
    if file_object2.delete_label("test_label1"):
        print("Label Deleted from Resource")

except CruxAPIException as err:
    print(err.status_code, err.error_message)
except CruxClientException as err:
    print(err.message)
```

## Fetch All Labels of Resource

```python
from crux import Crux
from crux.exceptions import CruxAPIException, CruxClientException

# Set the `CRUX_API_KEY`, `CRUX_API_HOST` environment variables.
# By default `CRUX_API_HOST` will point to Production environment
conn = Crux()

# Custom connection attributes can be set via following

conn = Crux(api_key="123456789", api_host="https://api.example.com")

try:
    dataset_object = conn.get_dataset(id="567890")

    file_object = dataset_object.get_file(path="/test_folder1/test_folder2/test_file.csv")


    if file_object.add_label("test_label1","test_value1"):
        print("Label Added to the Resource")
    if file_object.add_label("test_label2","test_value2"):
        print("Label Added to the Resource")

    for label in file_object.labels:
        print(label, file_object.labels.get(label))

except CruxAPIException as err:
    print(err.status_code, err.error_message)
except CruxClientException as err:
    print(err.message)
