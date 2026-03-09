import json
import logging
from urllib.request import urlopen, Request

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
