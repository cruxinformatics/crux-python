from crux.models.model import CruxModel
from crux.models.delivery import Delivery



class Ingestion(CruxModel):
    def __init__(
        self,
        id=None,
        versions=None,
        connection=None,
        dataset_id=None
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
    def from_dict(cls, id, versions, dataset_id):

        return cls(
            id,
            versions,
            dataset_id
        )

    def get_data(
        self,
        version=None,
        file_format=None,
        ):

        if version is None:
            version = max(self.versions)

        delivery_id = "{}.{}".format(self.id, version)

        delivery_object = Delivery.from_dict(delivery_id, self.dataset_id)
        delivery_object.connection = self.connection

        return delivery_object.get_data(file_format=file_format)

    def get_raw(
        self,
        version=None,
        ):

        if version is None:
            version = max(self.versions)

        delivery_id = "{}.{}".format(self.id, version)

        delivery_object = Delivery.from_dict(delivery_id, self.dataset_id)
        delivery_object.connection = self.connection

        return delivery_object.get_raw()
