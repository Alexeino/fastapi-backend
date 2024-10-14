from pydantic import BaseModel, Field, conlist
import enum
from typing import Annotated
from annotated_types import Len
from typing import Optional


class JobStatus(enum.Enum):
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    FILLED = "FILLED"


class JobCreationRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=10)
    location: Annotated[list[str], Len(min_length=1)]
    status: str = Field(default=JobStatus.OPEN)
    salary_range: str = Field(min_length=3)
    tags: Annotated[list[str], Len(min_length=1)]


class JobFilter(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    status: Optional[Annotated[str, JobStatus]] = Field(
        title="Not Yet Implemented", default=None
    )
    location: Optional[str] = None  # Can be comma separated values
    min_salary: Optional[str] = None
    max_salary: Optional[str] = None
    tags: Optional[str] = None  # Can be comma seperated values
