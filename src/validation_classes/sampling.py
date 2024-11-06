from __future__ import annotations

import datetime
import math
from typing import Any

from pydantic import (
    BaseModel,
    ValidationInfo,
    field_serializer,
    field_validator,
    model_validator,
)

class Model(BaseModel):
    source_mat_id_orig: str | None
    samp_description: str | None
    tax_id: (
        int | float | None
    )  # Serialised to int, floats are due to NaNs being present
    scientific_name: str | None
    investigation_type: str | None
    env_material: str | None
    collection_date: str | None  # Serialised to datetime.date
    sampling_event: str | None
    sampl_person: str | None
    sampl_person_orcid: str | None
    tidal_stage: str | None
    depth: str | float | None  # TODO serialise to str
    noteworthy_env_cond: str | None
    replicate: str | int #https://github.com/emo-bon/observatory-profile/issues/33
    samp_size_vol: int | float | None = None  # TODO serialise to float
    time_fi: str | float | None = None  # TODO serialise to str
    size_frac: str | float | None = None  # TODO serialise to str
    size_frac_low: float | None
    size_frac_up: float | None
    membr_cut: bool | str | None = None  # Serialised as bool
    samp_collect_device: str | None
    samp_mat_process: str | None
    samp_mat_process_dev: str | None
    samp_store_date: str | None  # Serialised to datetime.date
    samp_store_loc: str | None
    samp_store_temp: int | None
    store_person: str | None
    store_person_orcid: str | None = None
    other_person: str | None
    other_person_orcid: str | None
    long_store: bool | str | None  # Serialised to bool
    ship_date: str | None  # Serialised to datetime.date
    arr_date_hq: str | None = None  # Serialised to datetime.date
    store_temp_hq: int | str | None  # Serialised to int
    ship_date_seq: str | None  # Serialised to date
    arr_date_seq: str | None  # Serialised to date
    failure: bool | str | None  # Serialised to bool
    failure_comment: str | None
    ENA_accession_number_sample: str | None = None
    source_mat_id: str

    # Let's get rid of empty strings first:
    @model_validator(mode="before")
    @classmethod
    def contains_a_blank_string(cls, model: Any) -> Any:
        for key in model:
            # print(f"Value in blank_strings {value}")
            if isinstance(model[key], str) and model[key].strip() == "":
                model[key] = None
        return model

    # Replace NaNs
    @model_validator(mode="before")
    @classmethod
    def replace_NaNs(cls, model: Any) -> Any:
        for key in model:
            if isinstance(model[key], float) and math.isnan(model[key]):
                model[key] = None
            # print(f"Value in NaNs {model[key]}")
        # print(f"Final value { | Nonemodel}")
        return model

    # Get rid of "NA" "N/A"'s
    # These are in the original sheets and does not
    # take account of pandas.NA types
    # there should be no pandas.NA anyway
    @model_validator(mode="before")
    @classmethod
    def replace_not_availables(cls, model: Any) -> Any:
        for key in model:
            if isinstance(model[key], str):
                elem = model[key].strip().lower
                if elem in ["na", "n a", "n/a", "n / a"]:
                    model[key] = None
            # print(f"Value in NaNs {model[key]}")
        # print(f"Final value {model}")
        return model

    @field_validator("membr_cut", "failure", "long_store")
    @classmethod
    def coerce_to_bool(cls, value: str | None) -> bool | None:
        if isinstance(value, bool):
            return value
        if not value or (
            value == "N\t2022-10-17\t2022-10-19\t-70\t2023-06-01\t2023-06-01\t\t\t"
        ):  # In VB long_store
            return None
        # https://github.com/emo-bon/observatory-profile/issues/32
        try:
            float(value)
            return None
        except ValueError as e:
            if not "could not convert string to float" in str(e):
                raise e
        # Should be string
        else:
            vl = value.lower()
            # print(f"This is vl: {vl}")
            if vl not in [
                "y",
                "n",
                "t",
                "f",
                "\u03c4",
            ]:  # "\u03c4" is a Greek Tau in ROSKOGO
                raise ValueError(f"Unrecognised value: {value}")
            else:
                return vl in ["y", "t", "\u03c4"]

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
                # ROSKOGO has dates in this field
                try:
                    datetime.datetime.strptime(value, "%Y-%m-%d")
                    return None
                except ValueError as err:
                    raise ValueError(f"Unrecognised value: {value}") from err

    @field_validator(
        "collection_date",
        "samp_store_date",
        "ship_date",
        "arr_date_hq",
        "ship_date_seq",
        "arr_date_seq",
    )
    @classmethod
    def coerce_the_date_strings(cls, value: str | None) -> datetime.date:
        if not value:
            return
        if isinstance(value, str):
            try:
                # ISO 8601 as it should be
                return datetime.datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                try:
                    # Day, month, year - 23/10/2023
                    return datetime.datetime.strptime(value, "%d/%m/%Y")
                except ValueError as err:
                    # NRMCB has "expected 06-2024"
                    if "expected" in value.lower():
                        return None
                    # UMF has "to_arrive_Sep_2023"
                    elif "arrive" in value.lower():
                        return None
                    else:
                        raise ValueError(f"Unrecognised value: {value}") from err
        else:
            raise ValueError(f"Unrecognised value: {value}")

    # Some sheets e.g. OSD74 have NaNs in this field and the
    # values get read as floats by pandas You cannot use standard
    # serialisation because you end up with mixed "int" and "float" sheets
    @field_validator("tax_id")
    @classmethod
    def coerce_tax_id(cls, value: int | float | None) -> int | None:
        # print(f"Type of {value} is {type(value)}")
        if not value:
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(
                value
            )  # this should be safe because the floats are coerced integers

    # Check to see if size_frac_up is greater than size_frac_low
    @field_validator("size_frac_up")
    @classmethod
    def check_size_frac(cls, value: float | None, info: ValidationInfo) -> float | None:
        if not value:
            return None
        if value < 0:
            raise ValueError(f"Value is less than 0: {value}")

        size_frac_low = info.data.get("size_frac_low")
        if size_frac_low is not None and value < size_frac_low:
            raise ValueError(
                f"size_frac_up ({value}) cannot be less than size_frac_low ({size_frac_low})"
            )

        return value

    #https://github.com/emo-bon/observatory-profile/issues/33
    @field_validator("replicate")
    @classmethod
    def check_if_replicate_is_still_an_int(cls, value: str | int) -> str:
        # It appears not all sheets have had replicate changed to a string type
        if isinstance(value, int):
            return str(value)
        else:
            return value
    
    @field_serializer(
        "collection_date",
        "samp_store_date",
        "ship_date",
        "arr_date_hq",
        "ship_date_seq",
        "arr_date_seq",
    )
    def serialize_dates(self, value: datetime.date | None) -> str | None:
        if isinstance(value, datetime.date):
            return value.strftime("%Y-%m-%d")
        else:
            return None

    @field_serializer("depth", "time_fi", "size_frac")
    def serialize_str_float_to_str(self, value: str | float | None) -> str | None:
        if isinstance(value, str):
            return value
        elif isinstance(value, float):
            return str(value)
        else:
            return None

    @field_serializer("samp_size_vol")
    def serialize_int_float_to_float(self, value: int | float | None) -> float | None:
        if isinstance(value, float):
            return value
        elif isinstance(value, int):
            return float(value)
        else:
            return None

# STRICT #########################################################


class StrictModel(Model):
    source_mat_id_orig: str
    samp_description: str
    tax_id: int
    scientific_name: str
    investigation_type: str
    env_material: str
    collection_date: str | None
    sampling_event: str
    sampl_person: str
    sampl_person_orcid: str | None
    tidal_stage: str | None
    depth: int
    replicate: str
    samp_size_vol: int
    time_fi: str | int
    size_frac: str
    size_frac_low: float  # Yes really a float!
    size_frac_up: float  # Yes really a float!
    membr_cut: bool | str | None = None
    samp_collect_device: str
    samp_mat_process: str
    samp_mat_process_dev: str
    samp_store_date: str | None
    samp_store_loc: str
    samp_store_temp: int
    store_person: str
    store_person_orcid: str | None
    other_person: str | None
    other_person_orcid: str | None
    long_store: bool | str | None = None
    ship_date: str | None
    arr_date_hq: str | None
    store_temp_hq: int
    ship_date_seq: str | None
    arr_date_seq: str | None
    failure: bool | str | None = None
    failure_comment: str
    ENA_accession_number_sample: str
    source_mat_id: str


# SEMI-STRICT ####################################################


class SemiStrictModel(Model):
    source_mat_id_orig: str | None
    samp_description: str | None
    tax_id: int | None
    scientific_name: str | None
    investigation_type: str | None
    env_material: str | None
    collection_date: str | None
    sampling_event: str | None
    sampl_person: str | None
    sampl_person_orcid: str | None
    tidal_stage: str | None
    depth: float | int | None
    replicate: (
        str | int | float | None
    )  # Rep int or "blank", hence str raw sheets are broken
    samp_size_vol: float | int | None
    time_fi: str | int | None  # Either str "fi" or integer!
    size_frac: str | None
    size_frac_low: float | int | None
    size_frac_up: float | int | None
    membr_cut: bool | str | None = None
    samp_collect_device: str | None
    samp_mat_process: str | None
    samp_mat_process_dev: str | None
    samp_store_date: str | None
    samp_store_loc: str | None
    samp_store_temp: float | int | None
    store_person: str | None
    store_person_orcid: str | None
    other_person: str | None
    other_person_orcid: str | None
    long_store: bool | str | None = None
    ship_date: str | None
    arr_date_hq: str | None
    store_temp_hq: float | int | None
    ship_date_seq: str | None
    arr_date_seq: str | None
    failure: bool | str | None = None
    failure_comment: str | None
    ENA_accession_number_sample: str | None
    source_mat_id: str | None
