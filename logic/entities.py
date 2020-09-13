class AddressEntity:
    """Base class for address types."""

    def __setattr__(self, key, value):
        """Trim string values in class attributes"""

        super().__setattr__(
            key, value.strip() if isinstance(value, str) else value
        )


class AddressEntityWithName(AddressEntity):
    """Base class for address types with name attribute."""

    def __init__(self, *, name: str):
        self.name = name

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"


class Country(AddressEntityWithName):
    """Country address type."""

    def __init__(self, *, name: str, code: str):
        super().__init__(name=name)
        self.code = code


class Region(AddressEntityWithName):
    """Region address type."""

    def __init__(self, *, name: str, geoip_name: str = ""):
        super().__init__(name=name)
        self.country_id = None
        self.geoip_name = geoip_name


class Area(AddressEntityWithName):
    """Area address type."""

    def __init__(self, *, name: str):
        super().__init__(name=name)
        self.region_id = None


class Locality(AddressEntityWithName):
    """Locality address type."""

    def __init__(self, *, name: str):
        super().__init__(name=name)
        self.area_id = None


class District(AddressEntityWithName):
    """District address type."""

    def __init__(self, *, name: str):
        super().__init__(name=name)
        self.locality_id = None


class Street(AddressEntityWithName):
    """Street address type."""

    def __init__(self, *, name: str):
        super().__init__(name=name)
        self.district_id = None


class House(AddressEntity):
    """House address type."""

    def __init__(self, *, number: str, index: str = ""):
        self.number = number
        self.street_id = None
        self.index = index

    def __repr__(self) -> str:
        return f"<{__class__.__name__}: {self.number}>"
