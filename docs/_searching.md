# Searching

## Search for files by label

Search for files and download them.

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset("A_DATASET_ID")

predicates=[
    {"op":"eq", "key":"SOME_KEY", "val":"SOME_VALUE"}
]

resources = dataset.find_resources_by_label(predicates=predicates)

for resource in resources:
    resource.download("/tmp/{file_name}".format(resource.name))
```
