"""Module contains Delivery model."""

from typing import Any, Dict, Iterator

from crux._client import CruxClient
from crux._config import CruxConfig
from crux.models.file import File
from crux.models.model import CruxModel
from crux.models.resource import MediaType, Resource


class Delivery(CruxModel):
    """Delivery Model."""

    def __init__(self, raw_model=None, connection=None):
        # type: (Dict, CruxClient) -> None
        """
        Attributes:
            raw_model (dict): Ingestion raw dictionary, Defaults to None.
            connection (CruxClient): Connection Object. Defaults to None.
        """
        self.raw_model = raw_model if raw_model is not None else {}
        self.connection = (
            connection if connection is not None else CruxClient(CruxConfig())
        )
        self.meta = None

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
        if self.meta is None:
            self.meta = self.summary()

        acceptable_status = [
            "DELIVERY_SUCCEEDED",
            "DELIVERY_OBSOLETE",
            "DELIVERY_FAILED",
            "DELIVERY_IN_PROGRESS",
        ]
        if self.meta["latest_health_status"] not in acceptable_status:
            raise ValueError("Invalid Status")

        return self.meta["latest_health_status"]

    @property
    def schedule_datetime(self):
        """str: Gets schedule datetime of delivery."""
        if self.meta is None:
            self.meta = self.summary()
        return self.meta["schedule_dt"]

    @classmethod
    def from_dict(cls, a_dict):
        # type: (Dict[str, Any]) -> Delivery
        """Transforms Delivery Dictionary to Delivery object.

        Args:
            a_dict (dict): Delivery Dictionary.

        Returns:
            crux.models.Delivery: Delivery Object.
        """
        return cls(raw_model=a_dict)

    def summary(self):
        # type: () -> Dict[Any, Any]
        """Get the Delivery summary

        Returns:
            dict: Dictionary containing delivery summary.
        """
        response = self.connection.api_call(
            "GET", ["deliveries", self.dataset_id, self.id]
        )

        return response.json()

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
                obj = File(id=resource["resource_id"])
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
                obj = File(id=resource)
                obj.connection = self.connection
                obj.refresh()
                yield obj
