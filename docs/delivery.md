# Delivery

## Streaming all Deliveries with DELIVERY_SUCCEEDED and DELIVERY_OBSOLETE status

```python
import os
import logging
import multiprocessing

from crux import Crux
from botocore.config import Config
import boto3
import smart_open

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


if not os.getenv("CRUX_API_KEY"):
    raise ValueError("CRUX_API_KEY is unset")

if not os.getenv("CRUX_DSID"):
    raise ValueError("CRUX_DSID is unset")

if not os.getenv("DELIVERY_BUCKET"):
    raise ValueError("DELIVERY_BUCKET is unset")


CRUX_CLIENT = Crux(api_key=os.getenv("CRUX_API_KEY"))


def stream_file(delivery_file, delivery_bucket):
    """Streaming Function for File"""

    # Creating connection each time so that retries are per
    # connection
    config = Config(retries={"max_attempts": 10})
    transport_params = {
        "session": boto3.Session(),
        "resource_kwargs": {"config": config},
    }

    s3_file_path = os.path.join(
        "s3://",
        delivery_bucket,
        delivery_file.dataset_id,
        delivery_file.labels["workflow_id"],
        delivery_file.labels["pipeline_id"],
        # Other options for timestamp could be crux_available_dt, schedule_dt or asOf
        delivery_file.labels["supplier_modified_dt"],
        delivery_file.labels["ingestion_id"],
        delivery_file.labels["version_id"],
        delivery_file.name,
    )

    log.info("Streaming started for %s", s3_file_path)
    with smart_open.open(s3_file_path, "wb", transport_params=transport_params) as fout:
        for chunk in delivery_file.iter_content():
            fout.write(chunk)
    log.info("Streaming completed for %s", s3_file_path)


def main():
    """Main Function"""

    logging.basicConfig(level=logging.INFO)

    dataset_id = os.getenv("CRUX_DSID")
    dataset = CRUX_CLIENT.get_dataset(dataset_id)
    delivery_bucket = os.getenv("DELIVERY_BUCKET")

    ingestions = dataset.get_ingestions()

    # Stream latest version of all ingestions to S3
    for ingestion in ingestions:
        log.info("Fetching delivery files for ingestion %s", ingestion.id)

        processes = []

        for delivery_file in ingestion.get_data(
            accepted_status=[
                "DELIVERY_SUCCEEDED",
                "DELIVERY_OBSOLETE"
            ]
        ):
            process = multiprocessing.Process(
                target=stream_file, args=(delivery_file, delivery_bucket)
            )
            processes.append(process)

        # Start all processes
        for process in processes:
            process.start()

        # Make sure all processes have finished
        for process in processes:
            process.join()

main()
```
## Fetching Deliveries in a selected time frame and with particular format type

```python
from datetime import datetime, timedelta, timezone
import os
import logging
import multiprocessing

from crux import Crux
from crux.models.resource import MediaType
from botocore.config import Config
import boto3
import smart_open

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


if not os.getenv("CRUX_API_KEY"):
    raise ValueError("CRUX_API_KEY is unset")

if not os.getenv("CRUX_DSID"):
    raise ValueError("CRUX_DSID is unset")

if not os.getenv("DELIVERY_BUCKET"):
    raise ValueError("DELIVERY_BUCKET is unset")


CRUX_CLIENT = Crux(api_key=os.getenv("CRUX_API_KEY"))


def stream_file(delivery_file, delivery_bucket):
    """Streaming Function for File"""

    # Creating connection each time so that retries are per
    # connection
    config = Config(retries={"max_attempts": 10})
    transport_params = {
        "session": boto3.Session(),
        "resource_kwargs": {"config": config},
    }

    s3_file_path = os.path.join(
        "s3://",
        delivery_bucket,
        delivery_file.dataset_id,
        delivery_file.labels["workflow_id"],
        delivery_file.labels["pipeline_id"],
        # Other options for timestamp could be crux_available_dt, schedule_dt or asOf
        delivery_file.labels["supplier_modified_dt"],
        delivery_file.labels["ingestion_id"],
        delivery_file.labels["version_id"],
        delivery_file.name,
    )

    log.info("Streaming started for %s", s3_file_path)
    with smart_open.open(s3_file_path, "wb", transport_params=transport_params) as fout:
        for chunk in delivery_file.iter_content():
            fout.write(chunk)
    log.info("Streaming completed for %s", s3_file_path)


def main():
    """Main Function"""

    logging.basicConfig(level=logging.INFO)

    dataset_id = os.getenv("CRUX_DSID")
    dataset = CRUX_CLIENT.get_dataset(dataset_id)
    delivery_bucket = os.getenv("DELIVERY_BUCKET")

    start_date = (datetime.now(timezone.utc) - timedelta(weeks=5)).isoformat()
    # Current Time
    end_date = datetime.now(timezone.utc).isoformat()

    ingestions = dataset.get_ingestions(start_date=start_date, end_date=end_date)

    # Stream latest version of all ingestions to S3
    for ingestion in ingestions:
        log.info("Fetching delivery files for ingestion %s", ingestion.id)

        processes = []

        for delivery_file in ingestion.get_data(
            accepted_status=[
                "DELIVERY_SUCCEEDED",
                "DELIVERY_OBSOLETE"
            ],
            file_format=MediaType.CSV.value
        ):
            process = multiprocessing.Process(
                target=stream_file, args=(delivery_file, delivery_bucket)
            )
            processes.append(process)

        # Start all processes
        for process in processes:
            process.start()

        # Make sure all processes have finished
        for process in processes:
            process.join()

main()
```

## Fetching Raw data

```python
from datetime import datetime, timedelta, timezone
import os
import logging
import multiprocessing

from crux import Crux
from botocore.config import Config
import boto3
import smart_open

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


if not os.getenv("CRUX_API_KEY"):
    raise ValueError("CRUX_API_KEY is unset")

if not os.getenv("CRUX_DSID"):
    raise ValueError("CRUX_DSID is unset")

if not os.getenv("DELIVERY_BUCKET"):
    raise ValueError("DELIVERY_BUCKET is unset")


CRUX_CLIENT = Crux(api_key=os.getenv("CRUX_API_KEY"))


def stream_file(delivery_file, delivery_bucket):
    """Streaming Function for File"""

    # Creating connection each time so that retries are per
    # connection
    config = Config(retries={"max_attempts": 10})
    transport_params = {
        "session": boto3.Session(),
        "resource_kwargs": {"config": config},
    }

    s3_file_path = os.path.join(
        "s3://",
        delivery_bucket,
        delivery_file.dataset_id,
        delivery_file.labels["workflow_id"],
        delivery_file.labels["pipeline_id"],
        "raw",
        delivery_file.labels["ingestion_id"],
        delivery_file.labels["version_id"],
        delivery_file.name,
    )

    log.info("Streaming started for %s", s3_file_path)
    with smart_open.open(s3_file_path, "wb", transport_params=transport_params) as fout:
        for chunk in delivery_file.iter_content():
            fout.write(chunk)
    log.info("Streaming completed for %s", s3_file_path)


def main():
    """Main Function"""

    logging.basicConfig(level=logging.INFO)

    dataset_id = os.getenv("CRUX_DSID")
    dataset = CRUX_CLIENT.get_dataset(dataset_id)
    delivery_bucket = os.getenv("DELIVERY_BUCKET")

    start_date = (datetime.now(timezone.utc) - timedelta(weeks=5)).isoformat()
    # Current Time
    end_date = datetime.now(timezone.utc).isoformat()

    ingestions = dataset.get_ingestions(start_date=start_date, end_date=end_date)

    # Stream latest version of all ingestions to S3
    for ingestion in ingestions:
        log.info("Fetching delivery files for ingestion %s", ingestion.id)

        processes = []

        for delivery_file in ingestion.get_raw():
            process = multiprocessing.Process(
                target=stream_file, args=(delivery_file, delivery_bucket)
            )
            processes.append(process)

        # Start all processes
        for process in processes:
            process.start()

        # Make sure all processes have finished
        for process in processes:
            process.join()

main()
```
