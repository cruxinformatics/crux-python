# Resource permissions

Permissions can be set on resources, files are the main type of resource. Permissions can be set on individual resources, a list of resources, all resources in a folder, or all resources in a dataset.

## Add permissions to a dataset

Recursively set permissions on all resources in a dataset.

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")

added = dataset.add_permission(
    identity_id="_subscribed_",
    permission="Read"
)

if added:
    print("Permission applied")
```

## Add permissions to a list of resources

Using resource paths:

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID"))

added = dataset.add_permission(
    identity_id="_subscribed_",
    permission="Read",
    resource_paths=[
        "/path/to/file/in/folder/file1.csv",
        "/path/to/another/file2.csv",
    ]
)

if added:
    print("Permission applied")
```

Using `Resource`/`File` objects:

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")
file = dataset.get_file(path="/path/to/file/in/folder/file1.csv")
file2 = dataset.get_file(path="/path/to/another/file2.csv")

added = dataset.add_permission(
    identity_id="_subscribed_",
    permission="Read",
    resource_objects=[file, file2]
)

if added:
    print("Permission applied")
```

Using resource IDs:

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")
file = dataset.get_file(path="/path/to/file/in/folder/file1.csv")
file2 = dataset.get_file(path="/path/to/another/file2.csv")

added = dataset.add_permission(
    identity_id="_subscribed_",
    permission="Read",
    resource_ids=[filet.id, file2.id]
)

if added:
    print("Permission applied")
```

## Add permissions to folder recursively

Add permissions recursively to all resources in a folder, using a `Folder` object.

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")
folder = dataset.get_folder(path="/some/folder")

added = folder.add_permission(
    identity_id="_subscribed_",
    permission="Read",
    recursive=True
)

if added:
    print("Permission recursively applied to the folder")
```

## Apply permissions to single resource

Add permissions to a single resource, using a `File` object.

```python
from crux import Crux

conn = Crux()

dataset = conn.get_dataset(id="A_DATASET_ID")
file = dataset.get_file(path="/path/to/file.csv")

permission = file.add_permission(
    identity_id="_subscribed_",
    permission="Read"
)

print(permission.target_id, permission.identity_id, permission.permission_name)
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
```
