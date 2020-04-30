# Delivery

## Fetching the latest scheduled delivery and downloading files for all the delivery frames

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

    delivery = dataset.get_latest_scheduled_delivery()

    media_type = MediaType.CSV.value
    log.info("Fetching latest %s delivery file schedule_datetime=%s", media_type, delivery.schedule_datetime)
    for delivery_file in delivery.get_data(
            file_format=media_type
    ):  # A delivery has one or more frames
        local_file_path = os.path.join(
            tempfile.gettempdir(),
            delivery_file.name,
        )
        log.info("   Download %s size=%s frame_id=%s", local_file_path, delivery_file.size, delivery_file.frame_id)
        delivery_file.download(local_file_path)

main()
```
## Fetching scheduled deliveries for selected time range and downloading files for all the delivery frames

```python
from datetime import datetime, timedelta, timezone
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

    start_date = (datetime.now(timezone.utc) - timedelta(days=8)).isoformat()
    end_date = datetime.now(timezone.utc).isoformat()

    deliveries = dataset.get_scheduled_deliveries(start_date=start_date, end_date=end_date)

    for delivery in deliveries:
        media_type = MediaType.CSV.value
        log.info("Fetching %s delivery files schedule_datetime=%s", media_type, delivery.schedule_datetime)
        for delivery_file in delivery.get_data(
                file_format=media_type
        ):  # A delivery has one or more frames
            local_file_path = os.path.join(
                tempfile.gettempdir(),
                delivery_file.name,
            )
            log.info("   Download %s size=%s frame_id=%s", local_file_path, delivery_file.size, delivery_file.frame_id)
            delivery_file.download(local_file_path)

main()
```
