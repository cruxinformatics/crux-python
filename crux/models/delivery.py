"""Module contains Delivery model."""

from typing import Dict, Iterator

from crux._client import CruxClient
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
        self._summary = None
        super(Delivery, self).__init__(raw_model, connection)

    @property
    def id(self):
        """str: Gets the Delivery ID."""
        return self.raw_model["delivery_id"]

    @property
    def dataset_id(self):
        """str: Gets the Dataset ID."""
        return self.raw_model["dataset_id"]

    @property
    def ingestion_time(self):
        """str: Gets ingestion time of delivery."""
        return self.summary["ingestion_time"]

    @property
    def status(self):
        """str: Gets the Status of delivery."""
        return self.summary["latest_health_status"]

    @property
    def schedule_datetime(self):
        """str: Gets schedule datetime of delivery."""
        return self.summary["schedule_dt"]

    @property
    def summary(self):
        """dict: Gets the Delivery Summary"""
        if self._summary is None:
            response = self.connection.api_call(
                "GET", ["deliveries", self.dataset_id, self.id]
            )
            self._summary = response.json()
        return self._summary

    def get_data(self, file_format=MediaType.AVRO.value, use_cache=None):
        # type: (str, bool) -> Iterator[Resource]
        """Get the processed delivery data

        Args:
            file_format (str): File format of delivery.
            use_cache (bool): Preference to set cached response

        Returns:
            list (:obj:`crux.models.Resource`): List of resources.
        """
        params = {}
        params["delivery_resource_format"] = file_format
        if use_cache is not None:
            params["useCache"] = use_cache

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

    def get_raw(self, use_cache=None):
        # type: (bool) -> Iterator[Resource]
        """Get the raw delivery data

        Args:
            use_cache (bool): Preference to set cached response

        Returns:
            list (:obj:`crux.models.Resource`): List of resources.
        """
        params = {}
        if use_cache is not None:
            params["useCache"] = use_cache

        response = self.connection.api_call(
            "GET", ["deliveries", self.dataset_id, self.id, "raw"], params=params
        )

        resource_list = response.json()["resource_ids"]

        if resource_list:
            for resource in resource_list:
                obj = File(
                    raw_model={"resourceId": resource}, connection=self.connection
                )
                obj.refresh()
                yield obj

    def get_healthlog(self, use_cache=None):
        # type: (bool) -> Iterator[Resource]
        """Get delivery healthlog information

        Args:
            use_cache (bool): Preference to set cached response

        Returns:
            dict: Healthlog Json Object.
        """
        params = {}
        if use_cache is not None:
            params["useCache"] = use_cache

        response = self.connection.api_call(
            "GET", ["deliveries", self.id, "log"], params=params
        )

        healthlog_list = response.json()
        return healthlog_list
