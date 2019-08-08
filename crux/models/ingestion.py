from crux._utils import create_logger
from crux.models.model import CruxModel
from crux.models.delivery import Delivery


class Ingestion(CruxModel):
    def __init__(
        self,
        id=None,
        versions=None,
        dataset_id=None,
        connection=None
    ):
        self._id = id
        self._versions = versions

        self.dataset_id = dataset_id
        self.connection = connection

    @property
    def id(self):
        return self._id

    @property
    def versions(self):
        return sorted(self._versions)

    @classmethod
    def from_dict(cls, a_dict):

        id = a_dict["ingestion_id"]
        versions = a_dict["versions"]
        dataset_id = a_dict["dataset_id"]

        return cls(
            id,
            versions,
            dataset_id
        )

    def get_data(
        self,
        version=None,
        file_format=None,
        accepted_status=["DELIVERY_SUCCEEDED"]
        ):

        if version is None:
            version = max(self.versions)

        delivery_id = "{}.{}".format(self.id, version)

        delivery_object = Delivery.from_dict({"delivery_id": delivery_id, "dataset_id": self.dataset_id})
        delivery_object.connection = self.connection

        if delivery_object.status not in accepted_status:
            raise Exception("Ingestion not found in acceptable statuses {}".format(accepted_status))

        return delivery_object.get_data(file_format=file_format)

    def get_raw(
        self,
        version=None,
        ):

        if version is None:
            version = max(self.versions)

        delivery_id = "{}.{}".format(self.id, version)

        delivery_object = Delivery.from_dict({"delivery_id": delivery_id, "dataset_id": self.dataset_id})
        delivery_object.connection = self.connection

        return delivery_object.get_raw()
