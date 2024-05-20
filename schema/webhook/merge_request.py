from pydantic import BaseModel


class Project(BaseModel):
    id: int


class ObjectAttributes(BaseModel):
    description: str
    url: str
    iid: int


class MergeRequestWebhook(BaseModel):
    object_attributes: ObjectAttributes
    project: Project
