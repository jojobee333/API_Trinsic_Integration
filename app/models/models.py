from typing import Optional, List
from pydantic import BaseModel


class TemplateField(BaseModel):
    name: str
    title: str
    description: str
    section: str
    optional: bool


class TemplateInfo(BaseModel):
    name: str
    title: str
    description: str
    fields: List[TemplateField]
    primary_field: str
    secondary_fields: Optional[List[str]]
    auxiliary_fields: Optional[List[str]]


class GovernanceFramework(BaseModel):
    name: str
    description: str
    uri: str

class JsonObject(BaseModel):
    json_object: dict
