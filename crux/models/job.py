"""Module contains AbstractJob, Job, LoadJob Model."""

from crux.models.model import CruxModel


class AbstractJob(CruxModel):
    """AbstractJob Model."""


class Job(AbstractJob):
    """Job Model."""

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


class StitchJob(AbstractJob):
    """Stitch Job Model."""

    @property
    def job_id(self):
        """str: Gets the Job Id."""
        return self.raw_model["jobId"]

    @property
    def status(self):
        """str: Gets the Job Status."""
        return self.raw_model["status"]
