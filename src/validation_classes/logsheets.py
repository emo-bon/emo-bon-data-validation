from __future__ import annotations

import math
from datetime import datetime
from typing import Any

from pydantic import (
    AliasChoices,
    BaseModel,
    Field,
    HttpUrl,
    model_validator,
)


class Model(BaseModel):
    country: str = Field(..., validation_alias=AliasChoices("EMBRC Node", "country"))
    institute: str = Field(
        ..., validation_alias=AliasChoices("EMBRC Site", "institute")
    )
    observatory_id: str = Field(
        ...,
        validation_alias=AliasChoices("EMOBON_observatory_id", "observatory_id"),
    )
    water_column: HttpUrl | None = Field(
        ..., validation_alias=AliasChoices("Water Column", "water_column")
    )
    soft_sediment: HttpUrl | None = Field(
        ..., validation_alias=AliasChoices("Soft sediment", "soft_sediemnt")
    )
    data_quality_control_threshold_date: datetime
    data_quality_control_assignee: str
    rocrate_profile_uri: HttpUrl
    autogenerate: bool

    # Let's get rid of empty strings first:
    @model_validator(mode="before")
    @classmethod
    def contains_a_blank_string(cls, model: Any) -> Any:
        for key in model:
            # print(f"Key {key} has value {model[key]} is type {type(model[key])}")
            # print(f"Value in blank_strings {value}")
            if isinstance(model[key], str) and model[key].strip() == "":
                model[key] = None
        return model

    # God I hate NaNs
    @model_validator(mode="before")
    @classmethod
    def replace_NaNs(cls, model: Any) -> Any:
        for key in model:
            if isinstance(model[key], float) and math.isnan(model[key]):
                model[key] = None
            # print(f"Value in NaNs {model[key]}")
        # print(f"Final value {model}")
        return model
