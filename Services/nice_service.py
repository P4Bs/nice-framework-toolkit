import json
import logging
from urllib.request import urlopen, Request
from collections import defaultdict
from Models.relationship import Relationship


def load_nice_framework_relationships() -> list[Relationship]:
    try:

        with urlopen(
            Request(
                "https://csrc.nist.gov/csrc/media/Projects/cprt/documents/nice/cprt_SP_800_181_2_1_0_12-11-2025.json",
                headers={"User-Agent": "Mozilla/5.0 (NICE-Toolkit)"})) as r:
            return json.loads(r.read().decode("utf-8"))["response"]["elements"]["relationships"]
    except Exception as e:
        logging.error(e)
        raise



class NiceService:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.relationships = load_nice_framework_relationships()
        self.relationship_index = self._build_relationship_index()

    def _build_relationship_index(self):
        from collections import defaultdict
        index = defaultdict(list)

        for relationship in self.relationships:
            src = relationship["source_element_identifier"]
            dest = relationship["dest_element_identifier"]

            index[src].append(dest)

        return index

    def get_role_relationships(self, role_id: str):
        return self.relationship_index.get(role_id, [])
