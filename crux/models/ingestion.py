"""Module contains Ingestion model."""

from typing import Dict, Iterator

from crux._client import CruxClient
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
        self._delivery_objects = {}  # type: Dict[int, Delivery]
        super(Ingestion, self).__init__(raw_model, connection)

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

    def _get_delivery_object(self, version=None):
        if version not in self._delivery_objects:
            delivery_id = "{}.{}".format(self.id, version)
            delivery_object = Delivery.from_dict(
                {"delivery_id": delivery_id, "dataset_id": self.dataset_id},
                connection=self.connection,
            )
            self._delivery_objects[version] = delivery_object
        return self._delivery_objects[version]

    def get_data(
        self,
        version=None,  # type: int
        file_format=MediaType.AVRO.value,  # type: str
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
            for version_no in sorted(self.versions, reverse=True):
                delivery_object = self._get_delivery_object(version_no)
                if delivery_object.status == "DELIVERY_SUCCEEDED":
                    return delivery_object.get_data(file_format=file_format)
            log.info(
                "Delivery %s has no version with DELIVERY_SUCCEEDED status",
                delivery_object.id,
            )
            return iter([])

        delivery_object = self._get_delivery_object(version)
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
