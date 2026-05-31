from pydantic import BaseModel
from typing import Dict

class QueryTemplateClassFromGenAI(BaseModel):
    thinking_process: str
    query_template_class: str
    is_possible_via_templates: bool
    attributes: Dict
    missing_attributes: bool

class GenAIResponseToUser(BaseModel):
    thinking_process: str
    response_to_user: str
    is_generic: bool