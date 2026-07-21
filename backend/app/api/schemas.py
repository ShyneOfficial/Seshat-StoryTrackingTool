from typing import Annotated

from pydantic import StringConstraints


ChapterId = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=255)
]

NonEmptyName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=255)
]