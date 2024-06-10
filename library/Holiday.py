from datetime import date


class Holiday:
    """Representation of a public holiday"""

    def __init__(
        self,
        date: str,
        name: str,
        localName: str,
        countryCode: str,
        fixed: bool,
        types: list[str],
    ):
        self.date = date
        self.name = name
        self.localName = localName
        self.countryCode = countryCode
        self.fixed = fixed
        self.types = types
