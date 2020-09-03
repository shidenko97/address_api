from abc import ABC, abstractmethod


class BaseSource(ABC):
    """Base source class."""

    @abstractmethod
    def get_address_rows(self) -> dict:
        """Generator of address rows."""
