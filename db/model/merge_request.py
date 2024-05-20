from sqlmodel import Field, SQLModel
from typing import Union


class ReleaseNote(SQLModel, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    current_description: str = Field(index=True)
    url: str = Field()


class History(SQLModel, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    description: str = Field()
    mr_id: Union[int, None] = Field(default=None, foreign_key="releasenote.id")
