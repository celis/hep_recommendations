from typing import Any, List, Dict


class LiteratureRecord:
    """
    Datamodel class for handling a literature record data
    """

    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @property
    def metadata(self) -> Dict[str, Any]:
        if "metadata" in self.data:
            return self.data["metadata"]

    @property
    def references(self) -> List[str]:
        if self.metadata and self.metadata.get("references"):
            return [
                element["record"]["$ref"].split("/")[-1]
                for element in self.metadata["references"]
                if element.get("record")
            ]

    @property
    def authors(self) -> List[str]:
        """
        returns the article authors.
        """
        if "authors" in self.metadata:
            return [author.get("full_name") for author in self.metadata["authors"]]

    @property
    def doi(self) -> str:
        """
        Returns the article DOI code
        """
        if "dois" in self.metadata:
            return self.metadata["dois"][0].get("value")

    @property
    def arxiv(self) -> Dict[str, str]:
        """
        returns the article data
        """
        if "arxiv_eprints" in self.metadata:
            return {
                "eprint": self.metadata["arxiv_eprints"][0].get("value"),
                "url": "https://arxiv.org/abs/"
                + self.metadata["arxiv_eprints"][0].get("value"),
            }

    @property
    def title(self) -> str:
        """
        Returns title as it appears on inspire
        """
        if "titles" in self.metadata:
            return self.metadata["titles"][0].get("title")

    @property
    def journal(self) -> Dict[str, Any]:
        """
        returns journal information
        """
        if "publication_info" in self.metadata:
            return {
                "title": self.metadata["publication_info"][0].get("journal_title"),
                "volume": self.metadata["publication_info"][0].get("journal_volume"),
                "page_start": self.metadata["publication_info"][0].get("page_start"),
                "year": self.metadata["publication_info"][0].get("year"),
            }
