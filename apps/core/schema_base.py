from datetime import date, datetime
from typing import Annotated, List, Literal, Optional

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    id: Optional[Annotated[int, Field(ge=1)]]
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None


class BaseFilterSchema(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    @property
    def is_empty(self) -> bool:
        return not self.model_dump(exclude_unset=True, exclude_none=True)


class BaseSearchFilter(BaseModel):
    search_field: Optional[str] = None


class GeoJsonSchema(BaseModel):
    type: Literal['Point', 'Polygon']
    coordinates: List[float] | List[List[List[float]]]
