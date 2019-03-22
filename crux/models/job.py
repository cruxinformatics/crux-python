"""Module contains AbstractJob, Job, LoadJob Model."""

from typing import Dict  # noqa: F401

from crux.models.model import CruxModel


class AbstractJob(CruxModel):
    """AbstractJob Model."""


class LoadJob(AbstractJob):
    """LoadJob Model."""

    def __init__(self, job_id=None, job_url=None):
        # type(str, str) -> None
        """
        Attributes:
            job_id (str): Job ID. Defaults to None.
            job_url (str): Job Url. Defaults to None.
        """

        self._job_id = job_id
        self._job_url = job_url

    @property
    def job_id(self):
        """str: Gets the Job Id."""
        return self._job_id

    @property
    def job_url(self):
        """str: Gets the Job URL."""
        return self._job_url

    @classmethod
    def from_dict(cls, a_dict):
        # type: (Dict[str, str]) -> LoadJob
        """Transforms LoadJob Dictionary to LoadJob object.

        Args:
            a_dict (dict): LoadJob Dictionary.

        Returns:
            crux.models.LoadJob: LoadJob Object.
        """
        job_id = a_dict["jobId"]
        job_url = a_dict["jobUrl"]

        return cls(job_id=job_id, job_url=job_url)


class Job(AbstractJob):
    """Job Model."""

    def __init__(self, job_id=None, status=None, statistics=None, connection=None):
        # type: (str, Status, Statistics, str) -> None
        """
        Attributes:
            job_id (str): Job ID. Defaults to None.
            status (Status): Status Object. Defaults to None.
            statistics (Statistics): Statistics Object. Defaults to None.
        """
        self.job_id = job_id
        self.status = status
        self.statistics = statistics
        self.connection = connection

    @classmethod
    def from_dict(cls, a_dict):
        # type: (Dict[str, str]) -> Job
        """Transforms Job Dictionary to Job object.

        Args:
            a_dict (dict): Job Dictionary.

        Returns:
            crux.models.Job: Job Object.
        """
        job_id = a_dict["jobId"]
        status = Status.from_dict(a_dict["status"])  # type: ignore
        statistics = Statistics.from_dict(a_dict["statistics"])  # type: ignore

        return cls(job_id=job_id, status=status, statistics=statistics)


class Status(object):
    """Job Status Model."""

    def __init__(self, state=None):
        # type: (str) -> None
        """
        Attributes:
            state (str): State. Defaults to None.
        """
        self.state = state

    @classmethod
    def from_dict(cls, a_dict):
        # type: (Dict[str, str]) -> Status
        """Transforms Job Status Dictionary to Job Status object.

        Args:
            a_dict (dict): Job Status Dictionary.

        Returns:
            crux.models.job.Status: Job Status Object.
        """
        state = a_dict["state"]

        return cls(state=state)


class Statistics(object):
    """Job Statistic Model."""

    def __init__(self, creation_time=None, start_time=None, end_time=None, load=None):
        # type(str, str, str, Load) -> None
        """
        Attributes:
            creation_time (str): Creation Time. Defaults to None.
            start_time (str): Start Time. Defaults to None.
            end_time (str): End Time. Defaults to None.
            load (Load): Load Object. Defaults to None.
        """
        self.creation_time = creation_time
        self.start_time = start_time
        self.end_time = end_time
        self.load = load

    @classmethod
    def from_dict(cls, a_dict):
        # type: (Dict[str, str]) -> Statistics
        """Transforms Job Statistics Dictionary to Job Statistics object.

        Args:
            a_dict (dict): Job Statistics Dictionary.

        Returns:
            crux.models.job.Statistics: Job Statistics Object.
        """
        creation_time = a_dict["creationTime"]
        start_time = a_dict["startTime"]
        end_time = a_dict["endTime"]
        load = Load.from_dict(a_dict["load"])  # type: ignore

        return cls(
            creation_time=creation_time,
            start_time=start_time,
            end_time=end_time,
            load=load,
        )


class Load(object):
    """ Job Load Model """

    def __init__(
        self,
        input_files=None,  # type: str
        input_file_bytes=None,  # type: str
        output_rows=None,  # type: str
        output_bytes=None,  # type: str
        bad_records=None,  # type: str
    ):
        # type(...) -> None
        """
        Attributes:
            input_files (str): Input files. Defaults to None.
            input_file_bytes (str): Input files bytes. Defaults to None.
            output_rows (str): Output rows. Defaults to None.
            output_bytes (str): Output Bytes. Defaults to None.
            bad_records (str): Bad Records. Defaults to None.
        """
        self.input_files = input_files
        self.input_file_bytes = input_file_bytes
        self.output_rows = output_rows
        self.output_bytes = output_bytes
        self.bad_records = bad_records

    @classmethod
    def from_dict(cls, a_dict):
        # type: (Dict[str, str]) -> Load
        """Transforms Job Load Dictionary to Job Load object.

        Args:
            a_dict (dict): Job Load Dictionary.

        Returns:
            crux.models.job.Load: Job Load Object.
        """
        input_files = a_dict["inputFiles"]
        input_file_bytes = a_dict["inputFileBytes"]
        output_rows = a_dict["outputRows"]
        output_bytes = a_dict["outputBytes"]
        bad_records = a_dict["badRecords"]

        return cls(
            input_files=input_files,
            input_file_bytes=input_file_bytes,
            output_rows=output_rows,
            bad_records=bad_records,
            output_bytes=output_bytes,
        )


class StitchJob(AbstractJob):
    """Stitch Job Model."""

    def __init__(self, job_id=None, status=None):
        # type(str, str) -> None
        """
        Attributes:
            job_id (str): Job ID. Defaults to None.
            status (str): Status. Defaults to None.
        """
        self.job_id = job_id
        self.status = status

    @classmethod
    def from_dict(cls, a_dict):
        # type: (Dict[str, str]) -> StitchJob
        """Transforms Stitch Job Dictionary to Stitch Job object.

        Args:
            a_dict (dict): Stitch Job Dictionary.

        Returns:
            crux.models.job.StitchJob: Stitch Job Object.
        """
        job_id = a_dict["jobId"]
        status = a_dict["status"]

        return cls(job_id=job_id, status=status)
