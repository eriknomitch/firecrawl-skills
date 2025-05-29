from pydantic import BaseModel, Field


class CompanyDetailsSchema(BaseModel):
    company_mission: str
    supports_sso: bool
    is_open_source: bool
    is_in_yc: bool
