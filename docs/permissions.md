# Dataset permissions

## Add permissions to a dataset


```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")

added = dataset.add_permission(
    "_subscribed_",
    "Read"
)

print(permission.target_id, permission.identity_id, permission.permission_name)
conn.close()
```

## List dataset permissions

List all permissions on a dataset.

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")
permission_list = dataset.list_permissions()

for permission in permission_list:
    print(permission.target_id, permission.identity_id, permission.permission_name)
conn.close()
```

## Delete permission on dataset

Delete permission on a dataset.

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")
deleted = dataset.delete_permission(
    "_subscribed_", 
    "Read"
)

if deleted:
    print("Permission deleted")
conn.close()
```


# Resource permissions

Permissions can be set on resources, files are the main type of resource. Permissions can be set on individual resources, a list of resources, all resources in a folder, or all resources in a dataset.

## Add permissions to a list of resources

Using resource paths:

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID"))

added = dataset.add_permission_to_resources(
    "_subscribed_",
    "Read",
    resource_paths=[
        "/path/to/file/in/folder/file1.csv",
        "/path/to/another/file2.csv",
    ]
)

if added:
    print("Permission applied")
conn.close()
```

Using `Resource`/`File` objects:

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")
file = dataset.get_file(path="/path/to/file/in/folder/file1.csv")
file2 = dataset.get_file(path="/path/to/another/file2.csv")

added = dataset.add_permission_to_resources(
    "_subscribed_",
    "Read",
    resource_objects=[file, file2]
)

if added:
    print("Permission applied")
conn.close()
```

Using resource IDs:

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")
file = dataset.get_file(path="/path/to/file/in/folder/file1.csv")
file2 = dataset.get_file(path="/path/to/another/file2.csv")

added = dataset.add_permission_to_resources(
    "_subscribed_",
    "Read",
    resource_ids=[file.id, file2.id]
)

if deleted:
    print("Permission deleted")
conn.close()
```

## Delete permissions from a list of resources

Using resource paths:

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID"))

deleted = dataset.delete_permission_from_resources(
    "_subscribed_",
    "Read",
    resource_paths=[
        "/path/to/file/in/folder/file1.csv",
        "/path/to/another/file2.csv",
    ]
)

if deleted:
    print("Permission deleted")
conn.close()
```

Using `Resource`/`File` objects:

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")
file = dataset.get_file(path="/path/to/file/in/folder/file1.csv")
file2 = dataset.get_file(path="/path/to/another/file2.csv")

deleted = dataset.delete_permissions_from_resource(
    "_subscribed_",
    "Read",
    resource_objects=[file, file2]
)

if deleted:
    print("Permission deleted")
conn.close()
```

Using resource IDs:

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")
file = dataset.get_file(path="/path/to/file/in/folder/file1.csv")
file2 = dataset.get_file(path="/path/to/another/file2.csv")

deleted = dataset.delete_permission_from_resources(
    "_subscribed_",
    "Read",
    resource_ids=[filet.id, file2.id]
)

if deleted:
    print("Permission deleted")
conn.close()
```

## Add permissions to folder recursively

Add permissions recursively to all resources in a folder, using a `Folder` object.

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")
folder = dataset.get_folder(path="/some/folder")

added = folder.add_permission(
    "_subscribed_",
    "Read",
    recursive=True
)

if added:
    print("Permission recursively applied to the folder")
conn.close()
```

## Remove permissions from folder recursively

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")
folder = dataset.get_folder(path="/some/folder")

deleted = folder.delete_permission(
    "_subscribed_",
    "Read",
    recursive=True
)

if deleted:
    print("Permission recursively deleted from the folder")
conn.close()
```

## Apply permissions to single resource

Add permissions to a single resource, using a `File` object.

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")
file = dataset.get_file(path="/path/to/file.csv")

permission = file.add_permission(
    "_subscribed_",
    "Read"
)

print(permission.target_id, permission.identity_id, permission.permission_name)
conn.close()
```

## List resource permissions

List all permissions on a resource.

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")
file = dataset.get_file(path="/path/to/file.csv")
permission_list = file.list_permissions()

for permission in permission_list:
    print(permission.target_id, permission.identity_id, permission.permission_name)
conn.close()
```

## Delete permission on resource

Delete permission on a resource.

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")
file = dataset.get_file(path="/path/to/file.csv")
deleted = file.delete_permission(
    "_subscribed_", 
    "Read"
)

if deleted:
    print("Permission deleted")
conn.close()
```
