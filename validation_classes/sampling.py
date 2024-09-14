from __future__ import annotations

import datetime
import math
from typing import Any

from pydantic import AliasChoices
from pydantic import BaseModel
from pydantic import Field
from pydantic import field_serializer
from pydantic import field_validator
from pydantic import model_validator


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
    replicate: str | int | float | None  # Serialised to str
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
    source_mat_id: str = Field(
        ...,
        validation_alias=AliasChoices("source_mat_id", "source_material_id"),
    )

    # Let's get rid of empty strings first:
    @model_validator(mode="before")
    @classmethod
    def contains_a_blank_string(cls, model: Any) -> Any:
        for key in model:
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
        if (
            value
            == "N\t2022-10-17\t2022-10-19\t-70\t2023-06-01\t2023-06-01\t\t\t"
        ):  # In VB long_store
            return None
        if not value:
            return None
        if isinstance(value, bool):
            return value
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
                if vl in ["y", "t"]:
                    return True
                else:
                    return False

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
                except ValueError:
                    raise ValueError(f"Unrecognised value: {value}")

    @field_validator("replicate")
    @classmethod
    def coerce_replicate_to_string(cls, value: int | float | None) -> str:
        # pylint: disable=unsubscriptable-object
        """
        Coerces replicate to a string, or "blank" if None

        Google sheets interprets the word "blank" as NULL/NaN
        when retrieving the sheet using the old "visualisation" method?!
        The values in sheets are ints but are coerced to floats by pandas
        because of the NaNs. Here we assume all None's (replaced NaNs,
        see above) are supposed to be "blank"
        """
        # print(f"{value=} is type {type(value)}")
        if not value:
            return "blank"
        if isinstance(value, int):
            return str(value)
        elif isinstance(value, float):
            return str(int(value))
        else:
            raise ValueError(f"Unrecognised value: {value}")

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
                except ValueError:
                    # NRMCB has "expected 06-2024"
                    if "expected" in value.lower():
                        return None
                    else:
                        raise ValueError(f"Unrecognised value: {value}")
        else:
            raise ValueError(f"Unrecognised value: {value}")

    # Some sheets e.g. OSD74 have NaNs in this field and the
    # values get read as floats by pandasYou cannot use standard
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
    def serialize_str_float_to_str(
        self, value: str | float | None
    ) -> str | None:
        if isinstance(value, str):
            return value
        elif isinstance(value, float):
            return str(value)
        else:
            return None

    @field_serializer("samp_size_vol")
    def serialize_int_float_to_float(
        self, value: int | float | None
    ) -> float | None:
        if isinstance(value, float):
            return value
        elif isinstance(value, int):
            return float(value)
        else:
            return None

    # Some sheets e.g. OSD74 have NaNs in this field and the values get read as floats by pandas
    # You cannot use standard serialisation because you end up with mixed "int" and "float" sheets
    # @field_serializer("tax_id")
    # def serialize_tax_id(self, value: Union[int, float, None]) -> Optional[int]:
    #    #print(f"Type of {value} is {type(value)}")
    #    if not value:
    #        return None
    #    if isinstance(value, int):
    #        return value
    #    if isinstance(value, float):
    #        return int(value) # this should be safe because the floats are coerced integers


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
