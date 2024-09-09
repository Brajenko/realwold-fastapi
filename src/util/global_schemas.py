from typing import Annotated

import zoneinfo
from pydantic import AfterValidator, PastDatetime, PlainSerializer

zone = zoneinfo.ZoneInfo("Europe/Moscow")

MicrosecondsDateTime = Annotated[
    PastDatetime,
    AfterValidator(lambda x: x.replace(tzinfo=zone)),
    PlainSerializer(lambda x: x.isoformat(timespec="milliseconds"), return_type=str),
]
