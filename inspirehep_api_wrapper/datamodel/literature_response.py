from requests import Response
from inspirehep_api_wrapper.datamodel.literature_record import LiteratureRecord
from typing import Dict, Any


class LiteratureResponse:
    """
    Contains the response from the literature endpoint
    """

    def __init__(self, api_literature_response: Response):
        self.api_literature_response = api_literature_response

    @property
    def data(self) -> Dict[str, Any]:
        return self.api_literature_response.json()

    def to_record(self) -> LiteratureRecord:
        return LiteratureRecord(self.data)
