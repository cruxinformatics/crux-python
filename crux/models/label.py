"""Module contains Label model."""

from crux.models.model import CruxModel


class Label(CruxModel):
    """Label Model."""

    @property
    def label_key(self):
        """str: Gets the Label Key."""
        return self.raw_model["labelKey"]

    @property
    def label_value(self):
        """str: Gets the Label Value."""
        return self.raw_model["labelValue"]
