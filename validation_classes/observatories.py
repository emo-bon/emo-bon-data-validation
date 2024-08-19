import math
from datetime import date
from typing import Optional, Any
from pydantic import (
    BaseModel,
    ValidationError,
    ValidationInfo,
    field_validator,
    Field,
    AliasChoices,
    model_validator,
    field_serializer,
)

class Model(BaseModel):
    country_code: str
    country: str
    observatory_name: str = Field(..., validation_alias=AliasChoices("EMOBON_observatory_name", "observatory_name"))
    observatory_id: str = Field(..., validation_alias=AliasChoices("EMOBON_observatory_id", "observatory_id"))
    start_date: str = Field(..., validation_alias=AliasChoices("startdate", "start_date"))
    end_date: str | None = Field(validation_alias=AliasChoices("enddate", "end_date"))
    water_column: str | bool = Field(..., validation_alias=AliasChoices("Water_Column", "water_column"))
    soft_substrates: str | bool = Field(..., validation_alias=AliasChoices("Soft_Substrates", "soft_substrates"))
    hard_substrates: str | bool = Field(..., validation_alias=AliasChoices("Hard_Substrates", "hard_substrates"))
    water_site_latitude: float | None
    water_site_longitude: float | None
    sediment_site_latitude: float | None
    sediment_site_longtitude: float | None
    hard_substrates_site1_longitude: float | None
    hard_substrates_site1_latitude: float | None
    hard_substrates_site2_longtitude: float | None
    hard_substrates_site2_latitude: float | None
    contact_person: str = Field(..., validation_alias=AliasChoices("contect person", "contact_person"))
    contact_person_email: str = Field(..., validation_alias=AliasChoices("contact person email", "contact_person_email"))
    ena_accession_number_umbrella: Optional[str] = Field(..., validation_alias=AliasChoices("ENA_accession_number_umbrella", "ena_accession_number_umbrella"))
    ena_accession_number_project: Optional[str] = Field(..., validation_alias=AliasChoices("ENA_accession_number_project", "ena_accession_number_project"))
    core: str | bool = Field(..., validation_alias=AliasChoices("EMOBON_core", "core"))

    #Let's get rid of empty strings first:
    @model_validator(mode="before")
    @classmethod
    def contains_a_blank_string(cls, model: Any) -> Any:
        for key in model:
            #print(f"Key {key} has value {model[key]} is type {type(model[key])}")
            #print(f"Value in blank_strings {value}")
            if isinstance(model[key], str):
                if model[key].strip() == "":
                    model[key] = None
        return model

    #God I hate NaNs
    @model_validator(mode="before")
    @classmethod
    def replace_NaNs(cls, model: Any) -> Any:
        for key in model:
            if isinstance(model[key], float):
                if math.isnan(model[key]):
                    model[key] = None
            #print(f"Value in NaNs {model[key]}")
        #print(f"Final value {model}")
        return model

    @field_validator("water_column", "soft_substrates", "hard_substrates", "core")
    @classmethod
    def coerce_to_bool(cls, value: str | bool) -> bool:
        if isinstance(value, bool):
            return value
        else:
            vl = value.lower()
            if vl not in ["y", "n"]:
                raise ValidationError(f"What the hell is this: {value}")
            else:
                if vl == "y":
                    return True
                else:
                    return False

    @field_validator("start_date")
    @classmethod
    def coerce_the_startdate(cls, value: str) -> date:
        if isinstance(value, str):
            bits = [int(bit) for bit in value.split("/")]
            value = date(bits[2], bits[1], bits[0])
            return value
        else:
            raise ValidationError(f"What the hell is this: {value}")

    @field_validator("end_date")
    @classmethod
    def coerce_the_enddate(cls, value: str | None) -> date | None:
        #print(f"Values is {value}")
        if value:
            if isinstance(value, str):
                bits = [int(bit) for bit in value.split("/")]
                value = date(bits[2], bits[1], bits[0])
                return value
            else:
                raise ValidationError(f"What the hell is this: {value}")
        else:
            return None

    @field_serializer("start_date")
    def serialize_start_date(self, start_date: date) -> str:
        return str(start_date)

    @field_serializer("end_date")
    def serialize_end_date(self, end_date: date | None) -> str | None:
        if isinstance(end_date, date):
            return str(end_date)
        else:
            return None

