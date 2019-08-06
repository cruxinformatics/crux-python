from crux.models.resource import MediaType
from crux.models.file import File
from crux.models.model import CruxModel


class Delivery(CruxModel):
    def __init__(
        self,
        id=None,
        dataset_id=None,
        connection=None,
    ):
        self._id = id

        self.connection = connection
        self.dataset_id = dataset_id
        self.meta = None

    @property
    def id(self):
        return self._id

    @property
    def status(self):
        if self.meta is None:
            self.meta = self.summary()

        ACCEPTABLE_STATUS = [
            "DELIVERY_SUCCEEDED",
            "DELIVERY_OBSOLETE",
            "DELIVERY_FAILED",
            "DELIVERY_IN_PROGRESS"
        ]
        if self.meta["latest_health_status"] not in ACCEPTABLE_STATUS:
            raise ValueError("Invalid Status")

        return self.meta["latest_health_status"]

    @property
    def schedule_datetime(self):
        if self.meta is None:
            self.meta = self.summary()
        return self.meta["schedule_dt"]

    @classmethod
    def from_dict(cls, id, dataset_id):

        return cls(
            id=id,
            dataset_id=dataset_id
        )

    def summary(self):
        response = self.connection.api_call(
            "GET",
            ["deliveries", self.dataset_id, self.id]
        )

        return response.json()

    def get_data(self, file_format=MediaType.AVRO.value):
        delivery_resources = []
        params = {}

        params["delivery_resource_format"] = file_format

        response = self.connection.api_call(
            "GET",
            ["deliveries", self.dataset_id, self.id, "data"],
            params=params
        )

        resource_list = response.json()["resources"]

        if resource_list:
            for resource in resource_list:
                obj = File(id=resource["resource_id"])
                obj.connection = self.connection
                delivery_resources.append(obj)
            return delivery_resources

        return None

    def get_raw(self):
        delivery_resources = []

        response = self.connection.api_call(
            "GET",
            ["deliveries", self.dataset_id, self.id, "data"],
        )

        resource_list = response.json()["resource_ids"]

        if resource_list:
            for resource in resource_list:
                obj = File(id=resource)
                obj.connection = self.connection
                delivery_resources.append(obj)
            return delivery_resources

        return None
