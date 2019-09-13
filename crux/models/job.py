"""Module contains AbstractJob, Job, LoadJob Model."""

from typing import Dict  # noqa: F401

from crux._client import CruxClient
from crux._config import CruxConfig
from crux.models.model import CruxModel


class AbstractJob(CruxModel):
    """AbstractJob Model."""


class Job(AbstractJob):
    """Job Model."""

    def __init__(self, raw_model=None, connection=None):
        # type: (Dict, CruxClient) -> None
        """
        Attributes:
            raw_model (dict): Identity raw dictionary. Defaults to None.
            connection (CruxClient): Connection Object. Defaults to None.
        """
        self.raw_model = raw_model if raw_model is not None else {}
        self.connection = (
            connection if connection is not None else CruxClient(CruxConfig(api_key=""))
        )

    @property
    def job_id(self):
        """str: Gets the Job Id."""
        return self.raw_model["jobId"]

    @property
    def status(self):
        """str: Gets the Job Status."""
        return self.raw_model["status"]

    @property
    def statistics(self):
        """str: Gets the Job Statistics."""
        return self.raw_model["statistics"]

    @classmethod
    def from_dict(cls, a_dict, connection=None):
        # type: (Dict[str, str], CruxClient) -> Job
        """Transforms Job Dictionary to Job object.

        Args:
            a_dict (dict): Job Dictionary.
            connection (CruxClient): Connection Object. Defaults to None.

        Returns:
            crux.models.Job: Job Object.
        """
        return cls(raw_model=a_dict, connection=connection)


class StitchJob(AbstractJob):
    """Stitch Job Model."""

    def __init__(self, raw_model=None, connection=None):
        # type: (Dict, CruxClient) -> None
        """
        Attributes:
            raw_model (dict): Identity raw dictionary. Defaults to None.
            connection (CruxClient): Connection Object. Defaults to None.
        """
        self.raw_model = raw_model if raw_model is not None else {}
        self.connection = (
            connection if connection is not None else CruxClient(CruxConfig(api_key=""))
        )

    @property
    def job_id(self):
        """str: Gets the Job Id."""
        return self.raw_model["jobId"]

    @property
    def status(self):
        """str: Gets the Job Status."""
        return self.raw_model["status"]

    @classmethod
    def from_dict(cls, a_dict, connection=None):
        # type: (Dict[str, str], CruxClient) -> StitchJob
        """Transforms Stitch Job Dictionary to Stitch Job object.

        Args:
            a_dict (dict): Stitch Job Dictionary.
            connection (CruxClient): Connection Object. Defaults to None.

        Returns:
            crux.models.job.StitchJob: Stitch Job Object.
        """
        return cls(raw_model=a_dict, connection=connection)
