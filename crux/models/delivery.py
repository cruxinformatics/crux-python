from crux.models.model import CruxModel
from crux.models._factory import get_resource_object


class Delivery(CruxModel):
    def __init__(
        self,
        id=None,
        dataset_id=None,
        connection=None
    ):
        self._id = id

        self.connection = connection
        self.dataset_id = dataset_id

    @property
    def id(self):
        return self._id

    @classmethod
    def from_dict(cls, id):
        id = id

        return cls(
            id=id,
        )

    def summary(self):
        response = self.connection.api_call(
            "GET",
            ["deliveries", self.dataset_id, self.id]
        )

        return response.json()

    def data(self, file_format=None, lookback=None):
        delivery_resources = []
        params = {}

        if file_format:
            params["delivery_resource_format"] = file_format

        if lookback:
            params["delivery_lookback"] = lookback


        response = self.connection.api_call(
            "GET",
            ["deliveries", self.dataset_id, self.id, "data"],
            params=params
        )

        resource_list = response.json()["resources"]

        if resource_list:
            for resource in resource_list:
                delivery_resources.append(self._resource_object(resource["resource_id"]))
            return delivery_resources

        return None

    def _resource_object(self, resource_id):
        response = self.connection.api_call("GET", ["resources", resource_id])
        raw_resource = response.json()

        resource = get_resource_object(
            resource_type=raw_resource.get("type"), data=raw_resource
        )
        resource.connection = self.connection
        resource.raw_response = raw_resource
        return resource
