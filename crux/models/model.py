"""Module defines abstract CruxModel."""

import pprint


class CruxModel(object):
    """Absract Crux Model."""

    def to_dict(self):
        """Absract to_dict method."""

    def to_str(self):
        # type: () -> str
        """Absract to_str method."""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        # type: () -> str
        """Absract __repr__ method."""
        return self.to_str()
