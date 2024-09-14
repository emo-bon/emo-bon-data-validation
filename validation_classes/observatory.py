# This is a validator for the "observatory" sheet of the EMO_BON_Metadata Google Sheets
from __future__ import annotations

import math
from typing import Any
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import model_validator

# The type Optional[x] is a shorthand for Union[x, None].
# Optional[x] can also be used to specify a required field that can take None as a value.
# The Union type allows a model attribute to accept different types
# If a field is missing from a sheet "=<value>" will add it and give it a default value

# TODO: add checks for ranges that the low value is lower that the upper value

# Types have been compared to https://github.com/emo-bon/observatory-profile/blob/main/logsheet_schema_extended.csv
# Most of the out types are the in-types for the triples, apart from the bools and datetime.date fields


class Model(BaseModel):
    project_name: str | None
    latitude: float | None
    longitude: float | None
    geo_loc_name: str | None
    loc_broad_ocean: str | None
    loc_broad_ocean_mrgid: int | None
    loc_regional: str | None
    loc_regional_mrgid: int | None
    loc_loc: str | None
    loc_loc_mrgid: str | int
    env_broad_biome: str | None
    env_local: str | None
    env_package: str | None
    tot_depth_water_col: float | None
    organization: str | None
    organization_country: str | None
    organization_edmoid: str | int | None
    obs_id: str
    wa_id: str | None = None
    extra_site_info: str | None
    contact_name: str | None
    contact_email: str | None
    contact_orcid: str | None
    ENA_accession_number_umbrella: str | None = None
    ENA_accession_number_project: str | None = None

    # Let's get rid of empty strings first:
    @model_validator(mode="before")
    @classmethod
    def contains_a_blank_string(cls, model: Any) -> Any:
        for key in model:
            # print(f"Key {key} has value {model[key]} is type {type(model[key])}")
            # print(f"Value in blank_strings {value}")
            if isinstance(model[key], str):
                if model[key].strip() == "":
                    model[key] = None
        return model

    # Replace NaNs
    @model_validator(mode="before")
    @classmethod
    def replace_NaNs(cls, model: Any) -> Any:
        for key in model:
            if isinstance(model[key], float):
                if math.isnan(model[key]):
                    model[key] = None
            # print(f"Value in NaNs {model[key]}")
        # print(f"Final value { | Nonemodel}")
        return model
