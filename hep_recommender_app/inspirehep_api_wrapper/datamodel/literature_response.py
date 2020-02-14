from requests import Response
from hep_recommender_app.inspirehep_api_wrapper.datamodel.literature_record import (
    LiteratureRecord,
)
from typing import Dict, Any


class LiteratureResponse:
    """
    Contains the response from the literature endpoint
    """

    REFERENCES = "references"
    AUTHORS = "authors"
    TITLES = "titles"
    PREPRINT_DATE = "preprint_date"

    def __init__(self, api_literature_response: Response):
        self.api_literature_response = api_literature_response

    @property
    def data(self) -> Dict[str, Any]:
        response = self.api_literature_response.json()
        if response.get("metadata"):
            response = response["metadata"]
            response = {
                self.REFERENCES: response.get(self.REFERENCES, []),
                self.AUTHORS: response.get(self.AUTHORS, ""),
                self.TITLES: response.get(self.TITLES, ""),
                self.PREPRINT_DATE: response.get(self.PREPRINT_DATE, ""),
            }
        else:
            response = {
                self.REFERENCES: [],
                self.AUTHORS: "",
                self.TITLES: "",
                self.PREPRINT_DATE: "",
            }
        return response

    def to_record(self) -> LiteratureRecord:
        return LiteratureRecord(self.data)
