from typing import Annotated
from pydantic import BeforeValidator

def cleanup_text(v: str | None) -> str | None:
    if v is None:
        return None
    return v.strip()

def cleanup_code(v: str | None) -> str | None:
    if v is None:
        return None
    return v.strip().upper()

CleanText = Annotated[str, BeforeValidator(cleanup_text)]
CleanCode = Annotated[str, BeforeValidator(cleanup_code)]
