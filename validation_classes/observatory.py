# This is a validator for the "observatory" sheet of the EMO_BON_Metadata Google Sheets

import math
from datetime import date
from typing import Any, Optional, Union
from pydantic import BaseModel, model_validator

# The type Optional[x] is a shorthand for Union[x, None].
# Optional[x] can also be used to specify a required field that can take None as a value.
# The Union type allows a model attribute to accept different types
# If a field is missing from a sheet "=<value>" will add it and give it a default value

# TODO: add checks for ranges that the low value is lower that the upper value

# Types have been compared to https://github.com/emo-bon/observatory-profile/blob/main/logsheet_schema_extended.csv
# Most of the out types are the in-types for the triples, apart from the bools and datetime.date fields


class Model(BaseModel):
    project_name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    geo_loc_name: Optional[str]
    loc_broad_ocean: Optional[str]
    loc_broad_ocean_mrgid: Optional[int]
    loc_regional: Optional[str]
    loc_regional_mrgid: Optional[int]
    loc_loc: Optional[str]
    loc_loc_mrgid: Union[str, int]
    env_broad_biome: Optional[str]
    env_local: Optional[str]
    env_package: Optional[str]
    tot_depth_water_col: Optional[float]
    organization: Optional[str]
    organization_country: Optional[str]
    organization_edmoid: Union[str, int, None]
    obs_id: str
    wa_id: Optional[str] = None
    extra_site_info: Optional[str]
    contact_name: Optional[str]
    contact_email: Optional[str]
    contact_orcid: Optional[str]
    ENA_accession_number_umbrella: Optional[str] = None
    ENA_accession_number_project: Optional[str] = None

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
