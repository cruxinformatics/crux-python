# Labels

## Resources

### View labels

Resources have a `dict` for labels set as the `labels` property.

```python
from crux import Crux

conn = Crux()
dataset = conn.get_dataset("A_DATASET_ID")
file = dataset.get_file("/test_folder1/test_folder2/test_file.csv")

print(file.labels)
```

### Search resources in dataset by label

```python
from crux import Crux

conn = Crux()
dataset = conn.get_dataset("A_DATASET_ID")

predicates= [
    {"op":"eq", "key":"label_key1", "val":"label_value1"}
]
resource_list = dataset.find_resources_by_label(predicates=predicates)

for resource in resource_list:
    resource.download("/tmp/{file_name}".format(resource.name))
```

### Add label to resource

```python
from crux import Crux

conn = Crux()
dataset = conn.get_dataset("A_DATASET_ID")

file = dataset.upload_file(
    src="/tmp/test_file.csv",
    dest="/test_folder1/test_folder2/test_file.csv",
)

file.add_label("label_key1", "label_value1")
```

### Add multiple labels to resource

```python
from crux import Crux

conn = Crux()
dataset = conn.get_dataset("A_DATASET_ID")

file = dataset.upload_file(
    src="/tmp/test_file.csv",
    dest="/test_folder1/test_folder2/test_file.csv",
)

file.add_labels({"label_key1": "label_value1", "label_key2": "label_value2"})
```

### Delete label from resource

```python
from crux import Crux

conn = Crux()
dataset = conn.get_dataset("A_DATASET_ID")

file = dataset.get_file(path="/test_folder1/test_folder2/test_file.csv")

file.delete_label("label_key1")
```

## Datasets

### Add label to existing dataset

```python
from crux import Crux

conn = Crux()
dataset = conn.get_dataset("A_DATASET_ID")
dataset.add_label("label_key1", "label_value1")
```

### Get label from dataset

```python
from crux import Crux

conn = Crux()
dataset= conn.get_dataset("A_DATASET_ID")
label = dataset.get_label("label_key1")
```

### Delete label from dataset

```python
from crux import Crux

conn = Crux()
dataset = conn.get_dataset("A_DATASET_ID")
dataset.delete_label("label_key1")
```
