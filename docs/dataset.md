# Dataset

## Get the latest Dataset file frames.

```python
import os
import logging
import tempfile

from crux import Crux
from crux.models.resource import MediaType

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


if not os.getenv("CRUX_API_KEY"):
    raise ValueError("CRUX_API_KEY is unset")

if not os.getenv("CRUX_DSID"):
    raise ValueError("CRUX_DSID is unset")

CRUX_CLIENT = Crux(api_key=os.getenv("CRUX_API_KEY"))


def main():
    """Main Function"""

    logging.basicConfig(level=logging.INFO)

    dataset_id = os.getenv("CRUX_DSID")
    dataset = CRUX_CLIENT.get_dataset(dataset_id)
    log.info("Dataset: %s", dataset.name)

    file_set = dataset.get_latest_files(
        frames=None,  # optional str or list[str]
        file_format=MediaType.CSV.value
    )

    for file in file_set:
        local_file_path = os.path.join(tempfile.gettempdir(), file.name)
        log.info("   Download %s size=%s", local_file_path, file.size)
        file.download(local_file_path)


main()
```

## Fetch Dataset file frames for a selected time range

```python
import os
import logging
import tempfile

from crux import Crux
from crux.models.resource import MediaType

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


if not os.getenv("CRUX_API_KEY"):
    raise ValueError("CRUX_API_KEY is unset")

if not os.getenv("CRUX_DSID"):
    raise ValueError("CRUX_DSID is unset")

CRUX_CLIENT = Crux(api_key=os.getenv("CRUX_API_KEY"))


def main():
    """Main Function"""

    logging.basicConfig(level=logging.INFO)

    dataset_id = os.getenv("CRUX_DSID")
    dataset = CRUX_CLIENT.get_dataset(dataset_id)
    log.info("Dataset: %s", dataset.name)

    file_set = dataset.get_files_range(
        start_date="2/1/2020",
        end_date="2/28/2020",
        frames=None,  # optional str or list[str]
        file_format=MediaType.AVRO.value
    )

    for file in file_set:
        local_file_path = os.path.join(tempfile.gettempdir(), file.name)
        log.info("   Download %s size=%s", local_file_path, file.size)
        file.download(local_file_path)


main()
```
