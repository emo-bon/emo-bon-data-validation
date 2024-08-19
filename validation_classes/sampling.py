import math
import datetime
from pydantic import BaseModel, field_validator, model_validator, ValidationError, Field, AliasChoices, field_serializer
from typing import Any

class Model(BaseModel):
    source_mat_id_orig: str | None
    samp_description: str | None
    tax_id: int | None
    scientific_name: str | None
    investigation_type: str | None
    env_material: str | None
    collection_date: datetime.date | str
    sampling_event: str | None
    sampl_person: str | None
    sampl_person_orcid: str | None
    tidal_stage: str | None
    depth: float | str | None
    replicate: float | None
    samp_size_vol: int | float | None = None
    time_fi: str | float | None = None
    size_frac: str | None = None
    size_frac_low: float | None
    size_frac_up: int | float | None
    membr_cut: bool | None = None
    samp_collect_device: str | None
    samp_mat_process: str | None
    samp_mat_process_dev: str | None
    samp_store_date: datetime.date | str | None
    samp_store_loc: str | None
    samp_store_temp: int | None
    store_person: str | None
    store_person_orcid: str | None = None
    other_person: str | None
    other_person_orcid: str | None
    long_store: bool | str | None
    ship_date: datetime.date | str | None
    arr_date_hq: datetime.date | str | None = None
    store_temp_hq: int | str | None
    ship_date_seq: datetime.date | None
    arr_date_seq: datetime.date | None 
    failure: bool | str | None
    failure_comment: str | None
    ENA_accession_number_sample: str | None = None
    source_mat_id: str = Field(..., validation_alias=AliasChoices("source_mat_id", "source_material_id"))

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
        #print(f"Final value { | Nonemodel}")
        return model

    #Get rid of "NA" "N/A"'s
    @model_validator(mode="before")
    @classmethod
    def replace_not_availables(cls, model: Any) -> Any:
        for key in model:
            if isinstance(model[key], str):
                elem = model[key].strip().lower
                if elem in ["na", "n a", "n/a", "n / a"]:
                    model[key] = None
            #print(f"Value in NaNs {model[key]}")
        #print(f"Final value {model}")
        return model
    

    @field_validator("membr_cut", "failure", "long_store")
    @classmethod
    def coerce_to_bool(cls, value: str | bool | None) -> bool | None:
        
        if value == "N\t2022-10-17\t2022-10-19\t-70\t2023-06-01\t2023-06-01\t\t\t": #In VB long_store
            return None 
        if not value:
            return None
        if isinstance(value, bool):
            return value
        else:
            vl = value.lower()
            #print(f"This is vl: {vl}")
            if vl not in ["y", "n", "t", "f", "\u03c4"]: # "\u03c4" is a Greek Tau in ROSKOGO
                raise ValueError(f"What the hell is this: {value}")
            else:
                if vl in ["y", "t"]:
                    return True
                else:
                    return False

    # Specifically dealing with crap

    @field_validator("store_temp_hq")
    @classmethod
    def coerce_store_temp_hq(cls, value: int | str) -> int:
        if isinstance(value, int):
            return value
        elif isinstance(value, str):
            try:
                int(value)
                return value
            except ValueError:
                #ROSKOGO has dates in this field
                try:
                    datetime.datetime.strptime(value, "%Y-%m-%d")
                    return None
                except ValueError:
                    raise ValueError(f"What the hell is this: {value}")

    @field_validator("collection_date", "samp_store_date", "ship_date", "arr_date_hq")
    @classmethod
    def coerce_the_date_strings(cls, value: str | None) -> datetime.date:
        if not value:
            return
        if isinstance(value, str):
            try:
                #ISO 8601 as it should be
                return datetime.datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                try:
                    #Day, month, year - 23/10/2023
                    return datetime.datetime.strptime(value, "%d/%m/%Y")
                except ValueError:
                    #NRMCB has "expected 06-2024"
                    if "expected" in value.lower():
                        return None
                    else:
                        raise ValueError(f"What the hell is this: {value}")
        else:
            raise ValueError(f"What the hell is this: {value}")

    @field_serializer("collection_date", "samp_store_date", "ship_date", "arr_date_hq")
    def serialize_dates(self, value: datetime.date | None) -> str | None:
        if isinstance(value, datetime.date):
            return value.strftime("%Y-%m-%d")
        else:
            return None