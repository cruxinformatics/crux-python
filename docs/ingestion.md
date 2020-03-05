# Ingestion

## Files from all ingesions

```python
import os
import logging

from crux import Crux

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

    ingestions = dataset.get_ingestions()

    for ingestion in ingestions:
        log.info("Fetching delivery files for ingestion %s", ingestion.id)

        for delivery_file in ingestion.get_data():
            local_file_path = os.path.join(
                "/tmp",
                delivery_file.dataset_id,
                # Other options for timestamp could be crux_available_dt, schedule_dt or asOf
                delivery_file.labels["supplier_modified_dt"],
                delivery_file.labels["ingestion_id"],
                delivery_file.labels["version_id"],
                delivery_file.labels["frame_id"],
                delivery_file.id,
                delivery_file.name,
            )
            delivery_file.download(local_file_path)
```

## Fetching ingestions in a selected time frame and with particular format type

```python
from datetime import datetime, timedelta, timezone
import os
import logging

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

    start_date = (datetime.now(timezone.utc) - timedelta(days=8)).isoformat()
    # Current Time
    end_date = datetime.now(timezone.utc).isoformat()

    ingestions = dataset.get_ingestions(start_date=start_date, end_date=end_date)

    for ingestion in ingestions:
        log.info("Fetching delivery files for ingestion %s", ingestion.id)

        for delivery_file in ingestion.get_data(
            media_type=MediaType.CSV.value
        ):
            local_file_path = os.path.join(
                "/tmp",
                delivery_file.dataset_id,
                # Other options for timestamp could be crux_available_dt, schedule_dt or asOf
                delivery_file.labels["supplier_modified_dt"],
                delivery_file.labels["ingestion_id"],
                delivery_file.labels["version_id"],
                delivery_file.labels["frame_id"],
                delivery_file.id,
                delivery_file.name,
            )
            delivery_file.download(local_file_path)

main()
```

## Fetching the latest successfully delivered ingestion

```python
import os
import logging

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

    ingestion = dataset.get_latest_ingestion()
    if not ingestion:
        raise Exception("Failed to find latest ingestion")

    for delivery_file in ingestion.get_data(
        media_type=MediaType.CSV.value
    ):
        local_file_path = os.path.join(
            "/tmp",
            delivery_file.dataset_id,
            # Other options for timestamp could be crux_available_dt, schedule_dt or asOf
            delivery_file.labels["supplier_modified_dt"],
            delivery_file.labels["ingestion_id"],
            delivery_file.labels["version_id"],
            delivery_file.labels["frame_id"],
            delivery_file.id,
            delivery_file.name,
        )
        delivery_file.download(local_file_path)

main()
```

## Fetching ingestion raw data

```python
from datetime import datetime, timedelta, timezone
import os
import logging

from crux import Crux

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

    start_date = (datetime.now(timezone.utc) - timedelta(days=8)).isoformat()
    # Current Time
    end_date = datetime.now(timezone.utc).isoformat()

    ingestions = dataset.get_ingestions(start_date=start_date, end_date=end_date)

    for ingestion in ingestions:
        log.info("Fetching delivery files for ingestion %s", ingestion.id)

        for delivery_file in ingestion.get_raw():
            local_file_path = os.path.join(
                "/tmp",
                delivery_file.dataset_id,
                "raw",
                delivery_file.labels["ingestion_id"],
                delivery_file.labels["version_id"],
                delivery_file.labels["frame_id"],
                delivery_file.id,
                delivery_file.name,
            )
            delivery_file.download(local_file_path)

main()
```


## Fetching particular Delivery

```python
import os
import logging

from crux import Crux

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


if not os.getenv("CRUX_API_KEY"):
    raise ValueError("CRUX_API_KEY is unset")

if not os.getenv("CRUX_DSID"):
    raise ValueError("CRUX_DSID is unset")

if not os.getenv("CRUX_DELIVERY_ID"):
    raise ValueError("CRUX_DELIVERY_ID is unset")

CRUX_CLIENT = Crux(api_key=os.getenv("CRUX_API_KEY"))

def main():
    """Main Function"""

    logging.basicConfig(level=logging.INFO)

    dataset_id = os.getenv("CRUX_DSID")
    delivery_id = os.getenv("CRUX_DELIVERY_ID")
    dataset = CRUX_CLIENT.get_dataset(dataset_id)

    delivery_object = dataset.get_delivery(delivery_id)

    for delivery_file in delivery_object.get_data():
        local_file_path = os.path.join(
                "/tmp",
                delivery_file.dataset_id,
                # Other options for timestamp could be crux_available_dt, schedule_dt or asOf
                delivery_file.labels["supplier_modified_dt"],
                delivery_file.labels["ingestion_id"],
                delivery_file.labels["version_id"],
                delivery_file.labels["frame_id"],
                delivery_file.id,
                delivery_file.name,
            )
            delivery_file.download(local_file_path)

main()
```
