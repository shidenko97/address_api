import csv
from io import BytesIO
from os import path
from urllib.request import urlopen
from zipfile import ZipFile

from config import UPLOADS_DIR
from logic.entities import (
    Area,
    Country,
    District,
    House,
    Locality,
    Region,
    Street,
)
from source.base_source import BaseSource


class Ukrposhta(BaseSource):
    """Ukrposhta address source."""

    _url: str = "http://services.ukrposhta.com/postindex_new/upload/houses.zip"
    _filename: str = UPLOADS_DIR + path.sep + "houses.csv"
    _country: Country = Country(name="Україна", code="UA")

    def get_address_rows(self) -> dict:
        """
        Generator of address rows.

        :raises: ValueError - problem with file downloading
        :return: Dict of address row
        :rtype: dict
        """

        if not self._download_file():
            raise ValueError("Problem with file downloading")

        for row in self._get_rows():
            yield self._format_row(row=row)

    def _download_file(self) -> bool:
        """
        Download source file.

        :return: Is it successfully downloaded
        :rtype: bool
        """

        with urlopen(self._url) as downloaded_file:
            with ZipFile(BytesIO(downloaded_file.read())) as zip_file:
                zip_file.extractall(UPLOADS_DIR)

        return path.isfile(self._filename)

    def _get_rows(self) -> dict:
        """
        Generator of raw source rows.

        :return: Dict of raw source row
        :rtype: dict
        """

        with open(self._filename, encoding="cp1251") as csv_file:
            csv_lines = csv.reader(csv_file, delimiter=";")
            next(csv_lines)  # Just skip first (header) line
            for row in csv_lines:
                houses = row[5].split(",")
                for house in houses:
                    yield {
                        "region": row[0],
                        "area": row[1],
                        "locality": row[2],
                        "street": row[4],
                        "index": row[3],
                        "house": house,
                    }

    def _format_row(self, *, row: dict) -> dict:
        """
        Format raw row to formatted.

        :param row: Raw source row
        :type row: dict
        :return: Formatted row
        :rtype: dict
        """

        return {
            "Country": self._country,
            "Region": Region(name=row.get("region")),
            "Area": Area(name=row.get("area")),
            "Locality": Locality(name=row.get("locality")),
            "District": District(name="-"),
            "Street": Street(name=row.get("street")),
            "House": House(number=row.get("house"), index=row.get("index")),
        }
