import requests
from hep_recommender_app.inspirehep_api_wrapper.datamodel.literature_response import (
    LiteratureResponse,
)


class InspireAPI:
    """
    Simple wrapper around the inspire api

    methods:
       literature: gives access to the literature endpoint
    """

    LITERATURE = "https://labs.inspirehep.net/api/literature/"

    def __init__(self):
        pass

    def literature(self, record_id: str) -> LiteratureResponse:
        """
        Returns api response for a given record_id
        """
        url = self.LITERATURE + record_id
        return LiteratureResponse(requests.get(url))

    def data(self, record_id):
        return {"id": record_id, "record": self.literature(record_id).to_record()}