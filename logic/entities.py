class AddressEntity:
    """Base class for address types."""

    def __init__(self, *, name: str):
        self.name = name

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"


class Country(AddressEntity):
    """Country address type."""

    def __init__(self, *, name: str, code: str):
        super().__init__(name=name)
        self.code = code


class Region(AddressEntity):
    """Region address type."""

    def __init__(self, *, name: str, geoip_name: str = ""):
        super().__init__(name=name)
        self.country_id = None
        self.geoip_name = geoip_name


class Area(AddressEntity):
    """Area address type."""

    def __init__(self, *, name: str):
        super().__init__(name=name)
        self.region_id = None


class Locality(AddressEntity):
    """Locality address type."""

    def __init__(self, *, name: str):
        super().__init__(name=name)
        self.area_id = None


class District(AddressEntity):
    """District address type."""

    def __init__(self, *, name: str):
        super().__init__(name=name)
        self.locality_id = None


class Street(AddressEntity):
    """Street address type."""

    def __init__(self, *, name: str):
        super().__init__(name=name)
        self.district_id = None


class House:
    """House address type."""

    def __init__(self, *, number: str, index: str = ""):
        self.number = number
        self.street_id = None
        self.index = index

    def __repr__(self) -> str:
        return f"<{__class__.__name__}: {self.number}>"
