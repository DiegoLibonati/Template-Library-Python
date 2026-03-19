from pydantic import BaseModel, constr


class TemplateModel(BaseModel):
    name: constr(min_length=1, strip_whitespace=True)
