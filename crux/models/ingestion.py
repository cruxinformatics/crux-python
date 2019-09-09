"""Module contains Ingestion model."""

from typing import Any, Dict, Iterator

from crux._client import CruxClient
from crux._config import CruxConfig
from crux._utils import create_logger
from crux.models.delivery import Delivery
from crux.models.model import CruxModel
from crux.models.resource import MediaType, Resource

log = create_logger(__name__)


class Ingestion(CruxModel):
    """Ingestion Model."""

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

    @property
    def id(self):
        """str: Gets the Ingestion ID."""
        return self.raw_model["ingestionId"]

    @property
    def dataset_id(self):
        """str: Gets the Dataset ID."""
        return self.raw_model["datasetId"]

    @property
    def versions(self):
        """list: Gets the list of versions."""
        return sorted(self.raw_model["versions"])

    @classmethod
    def from_dict(cls, a_dict):
        # type: (Dict[str, Any]) -> Ingestion
        """Transforms Ingestion Dictionary to Ingestion object.

        Args:
            a_dict (dict): Ingestion Dictionary.

        Returns:
            crux.models.Ingestion: Ingestion Object.
        """
        return cls(raw_model=a_dict)

    def get_data(
        self,
        version=None,  # type: int
        file_format=MediaType.AVRO.value,  # type: str
        accepted_status=None,  # type: list
    ):
        # type: (...) -> Iterator[Resource]
        """Get the processed delivery data

        Args:
            version (int): Version of the delivery.
            file_format (str): File format of delivery.
            accepted status (:obj:`list` of :obj:`str`): List of acceptable statuses.
                Defaults to None.

        Returns:
            list (:obj:`crux.models.Resource`): List of resources.
        """
        if version is None:
            version = max(self.versions)

        if accepted_status is None:
            accepted_status = ["DELIVER_SUCCEEDED"]

        delivery_id = "{}.{}".format(self.id, version)

        delivery_object = Delivery.from_dict(
            {"deliveryId": delivery_id, "datasetId": self.dataset_id}
        )
        delivery_object.connection = self.connection

        if delivery_object.status not in accepted_status:
            log.info(
                "Delivery %s has unacceptable status %s",
                delivery_object.id,
                delivery_object.status,
            )
            return iter([])

        return delivery_object.get_data(file_format=file_format)

    def get_raw(self, version=None):
        # type: (...) -> Iterator[Resource]
        """Get the raw delivery data

        Args:
            version (int): Version of the delivery.

        Returns:
            list (:obj:`crux.models.Resource`): List of resources.
        """
        if version is None:
            version = max(self.versions)

        delivery_id = "{}.{}".format(self.id, version)

        delivery_object = Delivery.from_dict(
            {"delivery_id": delivery_id, "dataset_id": self.dataset_id}
        )
        delivery_object.connection = self.connection

        return delivery_object.get_raw()
