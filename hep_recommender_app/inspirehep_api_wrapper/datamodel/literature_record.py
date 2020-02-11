from typing import Any, List, Dict


class LiteratureRecord:
    """
    Datamodel class for handling a literature record data
    """

    MAX_AUTHORS = 3

    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @property
    def references(self) -> List[str]:
        return [
            element["record"]["$ref"].split("/")[-1]
            for element in self.data["references"]
            if element.get("record")
        ]

    @property
    def authors_short(self) -> str:
        if len(self.data["authors"]) > self.MAX_AUTHORS:
            return "; ".join(
                [
                    author.get("full_name")
                    for author in self.data["authors"][: self.MAX_AUTHORS]
                ]
                + ["et. al."]
            )
        else:
            return "; ".join(
                [author.get("full_name") for author in self.data["authors"]]
            )

    @property
    def title(self) -> str:
        """
        Returns title as it appears on inspire
        """
        return self.data["titles"][0].get("title")

    @property
    def preprint_year(self) -> str:
        """
        :return:
        """
        return f"({self.data['preprint_date'].split('-')[0]})"
