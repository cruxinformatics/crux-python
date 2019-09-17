"""Module contains Delivery model."""

from typing import Iterator

from crux.models.file import File
from crux.models.model import CruxModel
from crux.models.resource import MediaType, Resource


class Delivery(CruxModel):
    """Delivery Model."""

    @property
    def id(self):
        """str: Gets the Delivery ID."""
        return self.raw_model["delivery_id"]

    @property
    def dataset_id(self):
        """str: Gets the Dataset ID."""
        return self.raw_model["dataset_id"]

    @property
    def status(self):
        """str: Gets the Status of delivery."""
        return self.raw_model["latest_health_status"]

    @property
    def schedule_datetime(self):
        """str: Gets schedule datetime of delivery."""
        return self.raw_model["schedule_dt"]

    def get_data(self, file_format=MediaType.AVRO.value):
        # type: (str) -> Iterator[Resource]
        """Get the processed delivery data

        Args:
            file_format (str): File format of delivery.

        Returns:
            list (:obj:`crux.models.Resource`): List of resources.
        """
        params = {}

        params["delivery_resource_format"] = file_format

        response = self.connection.api_call(
            "GET", ["deliveries", self.dataset_id, self.id, "data"], params=params
        )

        resource_list = response.json()["resources"]

        if resource_list:
            for resource in resource_list:
                obj = File(raw_model={"resourceId": resource["resource_id"]})
                obj.connection = self.connection
                obj.refresh()
                yield obj

    def get_raw(self):
        # type: () -> Iterator[Resource]
        """Get the raw delivery data

        Returns:
            list (:obj:`crux.models.Resource`): List of resources.
        """
        response = self.connection.api_call(
            "GET", ["deliveries", self.dataset_id, self.id, "raw"]
        )

        resource_list = response.json()["resource_ids"]

        if resource_list:
            for resource in resource_list:
                obj = File(
                    raw_model={"resourceId": resource}, connection=self.connection
                )
                obj.refresh()
                yield obj
