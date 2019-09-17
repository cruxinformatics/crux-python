"""Module contains Crux object to interact with root APIs."""

from typing import List, MutableMapping, Optional, Text, Union  # noqa: F401

from crux._client import CruxClient
from crux._config import CruxConfig
from crux._utils import Headers
from crux.models import Dataset, File, Folder, Identity, Job
from crux.models._factory import get_resource_object


class Crux(object):
    """Crux APIs."""

    def __init__(
        self,
        api_key=None,  # type: Optional[str]
        api_host=None,  # type: str
        proxies=None,  # type: Optional[MutableMapping[Text, Text]]
        user_agent=None,  # type: str
        api_prefix=None,  # type: str
        only_use_crux_domains=None,  # type: bool
    ):
        # type: (...) -> None
        crux_config = CruxConfig(
            api_key=api_key,
            api_host=api_host,
            proxies=proxies,
            user_agent=user_agent,
            api_prefix=api_prefix,
            only_use_crux_domains=only_use_crux_domains,
        )

        self.api_client = CruxClient(crux_config=crux_config)

    def close(self):
        """Closes the Connection."""
        self.api_client.close()

    def whoami(self):
        # type: () -> Identity
        """Returns the Identity of Current User.

        Returns:
            crux.models.Identity: Identity object.
        """
        headers = Headers(
            {"accept": "application/json"}
        )  # type: Optional[MutableMapping[Text, Text]]
        return self.api_client.api_call(
            "GET", ["identities", "whoami"], model=Identity, headers=headers
        )

    def create_dataset(self, name, description=None, tags=None):
        # type: (str, str, List[str]) -> Dataset
        """Creates the Dataset.

        Args:
            name (str): Sets whether to sort or not.
            description (str): Folder for which resource should be listed. Defaults to None.
            tags (:obj:`list` of :obj:`str`): Sets the offset. Defaults to None.

        Returns:
            crux.models.Dataset: Dataset object.
        """

        tags = tags if tags else []
        raw_model = {"name": name, "description": description, "tags": tags}
        dataset = Dataset(raw_model=raw_model, connection=self.api_client)
        dataset.create()
        return dataset

    def get_dataset(self, id):  # id name is by design pylint: disable=redefined-builtin
        # type: (str) -> Dataset
        """Fetches the Dataset.

        Args:
            id (str): Dataset ID which is to be fetched.

        Returns:
            crux.models.Dataset: Dataset object
        """
        headers = Headers(
            {"accept": "application/json"}
        )  # type: MutableMapping[Text, Text]
        return self.api_client.api_call(
            "GET", ["datasets", id], model=Dataset, headers=headers
        )

    def get_resource(self, id):  # id is by design pylint: disable=redefined-builtin
        # type: (str) -> Union[File, Folder]
        """Fetches the Resource by ID.

        Any supported resource can be fetched. The object returned will be an instance
        of the correct subclass, for example a ``crux.models.File`` instance will be
        returned for file resources.

        Args:
            id (str): Resource ID which is to be fetched.

        Returns:
            crux.models.Resource: Resource or its Child Object.
        """
        headers = Headers(
            {"accept": "application/json"}
        )  # type: MutableMapping[Text, Text]

        response = self.api_client.api_call("GET", ["resources", id], headers=headers)
        raw_resource = response.json()

        resource = get_resource_object(
            resource_type=raw_resource.get("type"),
            data=raw_resource,
            connection=self.api_client,
        )
        return resource

    def _call_drives_my(self):
        headers = Headers(
            {"accept": "application/json"}
        )  # type: MutableMapping[Text, Text]

        response = self.api_client.api_call(
            "GET", ["drives", "my"], model=None, headers=headers
        )

        return response.json()

    def list_datasets(self, owned=True, subscribed=True):
        # type: (bool, bool) -> List[Dataset]
        """Fetches a list of owned and/or subscribed Datasets.

        Args:
            owned (bool): Show datasets owned by the caller. Defaults to True.
            subscribed (bool): Show datasets the user has a subscription. Defaults to True.

        Returns:
            list(:obj:`crux.models.Dataset`): List of Dataset objects.
        """
        datasets = self._call_drives_my()
        dataset_list = []

        if owned:
            for dataset in datasets["owned"]:
                obj = Dataset.from_dict(dataset, connection=self.api_client)
                dataset_list.append(obj)

        if subscribed:
            for dataset in datasets["subscriptions"]:
                obj = Dataset.from_dict(dataset, connection=self.api_client)
                dataset_list.append(obj)

        return dataset_list

    def list_public_datasets(self):
        # type: () -> List[Dataset]
        """Fetches a list of public Datasets.

        Returns:
            list (:obj:`crux.models.Dataset`): List of Dataset objects.
        """
        headers = Headers(
            {"accept": "application/json"}
        )  # type: MutableMapping[Text, Text]
        return self.api_client.api_call(
            "GET", ["datasets", "public"], model=Dataset, headers=headers
        )

    def get_job(self, job_id):
        # type: (str) -> Job
        """Fetches the Job.

        Args:
            job_id (str): Job ID which is to be fetched.

        Returns:
            crux.models.Job: Job object.
        """
        headers = Headers(
            {"accept": "application/json"}
        )  # type: MutableMapping[Text, Text]
        return self.api_client.api_call(
            "GET", ["jobs", job_id], model=Job, headers=headers
        )

    def set_datasets_provenance(self, provenance):
        # type(Dict[Any, Any]) -> Dict[Any, Any]
        """ Sets the Dataset Provenance

        Args:
            provenance (dict): Provenance dictionary

        Returns:
            dict: Provenance response dictionary.

        Example:
            .. code-block:: python

                from crux import Crux

                conn = Crux()

                provenance = {
                    "dataset_id":[
                        {
                            "workflow_id": "test_id",
                            "pipeline_ids": ["test_id_1","test_id_2"],
                            "cron_spec": "0 0 1 1 0"
                            }
                        ]
                    }
                response = conn.set_datasets_provenance(provenance=provenance)
        """
        headers = Headers({"accept": "application/json"})

        response = self.api_client.api_call(
            "POST", ["datasets", "provenance"], headers=headers, json=provenance
        )
        return response.json()
