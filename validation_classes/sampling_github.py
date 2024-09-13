import math
import datetime
from pydantic import (
    BaseModel,
    field_validator,
    model_validator,
    ValidationError,
    Field,
    AliasChoices,
    field_serializer,
    HttpUrl,
)
from typing import Any


class ModelGithub(BaseModel):
    source_mat_id_orig: str | None
    samp_description: str | None
    tax_id: HttpUrl | None
    scientific_name: str | None
    investigation_type: str | None
    env_material: str | None
    collection_date: datetime.date | str
    sampling_event: str | None
    sampl_person: str | None
    sampl_person_orcid: str | None
    tidal_stage: str | None
    depth: float | str | None
    replicate: str | int | float
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
    samp_store_temp: int | str | None
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
    source_mat_id: str = Field(
        ..., validation_alias=AliasChoices("source_mat_id", "source_material_id")
    )

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

    # God I hate NaNs
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
    def coerce_to_bool(cls, value: str | bool | None) -> bool | None:
        if value == "N\t2022-10-17\t2022-10-19\t-70\t2023-06-01\t2023-06-01":
            # In VB long_store
            return None
        if not value:
            return None
        if value == "false":
            return False
        if value == "true":
            return True
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

    # The QC is actually introducing new errors not present in the original sheets
    @field_validator("samp_store_temp")
    @classmethod
    def coerce_samp_store_temp(cls, value: int | str) -> int:
        if isinstance(value, int):
            return value
        elif isinstance(value, str):
            try:
                int(value)
                return value
            except ValueError:
                # ROSKOGO has '-80°C' in this field
                if value[-1] == "C":
                    try:
                        return int(value[:-2])
                    except ValueError:
                        raise ValueError(f"Unrecognised value: {value}")

    @field_validator("store_temp_hq")
    @classmethod
    def coerce_store_temp_hq(cls, value: int | str) -> str:
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
    def coerce_replicate_to_string(cls, value: int | float | str) -> str:
        if isinstance(value, int):
            return str(value)
        elif isinstance(value, float):
            return str(int(value))
        elif isinstance(value, str):
            return value
        else:
            raise ValueError(f"Unrecognised value: {value}")

    @field_validator("collection_date", "samp_store_date", "ship_date", "arr_date_hq")
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

    @field_serializer("collection_date", "samp_store_date", "ship_date", "arr_date_hq")
    def serialize_dates(self, value: datetime.date | None) -> str | None:
        if isinstance(value, datetime.date):
            return value.strftime("%Y-%m-%d")
        else:
            return None


class StrictModelGithub(BaseModel):
    source_mat_id_orig: str
    samp_description: str
    tax_id: int
    scientific_name: str
    investigation_type: str
    env_material: str
    collection_date: datetime.date | str
    sampling_event: str
    sampl_person: str
    sampl_person_orcid: str | None
    tidal_stage: str | None
    depth: int
    replicate: str  # Rep int or "blank", hence str raw sheets are broken
    samp_size_vol: int
    time_fi: str | int
    size_frac: str
    size_frac_low: int
    size_frac_up: int
    membr_cut: bool | str
    samp_collect_device: str
    samp_mat_process: str
    samp_mat_process_dev: str
    samp_store_date: datetime.date | str
    samp_store_loc: str
    samp_store_temp: int
    store_person: str
    store_person_orcid: str | None
    other_person: str | None
    other_person_orcid: str | None
    long_store: bool | str
    ship_date: datetime.date | str
    arr_date_hq: datetime.date | str
    store_temp_hq: int
    ship_date_seq: datetime.date | str
    arr_date_seq: datetime.date | str
    failure: bool | str
    failure_comment: str
    ENA_accession_number_sample: str
    source_mat_id: str

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

    # God I hate NaNs
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

    @field_validator("membr_cut", "long_store", "failure")
    @classmethod
    def coerce_to_bool(cls, value: str | bool | None) -> bool | None:

        if (
            value == "N\t2022-10-17\t2022-10-19\t-70\t2023-06-01\t2023-06-01\t\t\t"
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

    @field_validator("collection_date", "samp_store_date", "ship_date", "arr_date_hq")
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


class SemiStrictModelGithub(BaseModel):
    source_mat_id_orig: str | None
    samp_description: str | None
    tax_id: int | None
    scientific_name: str | None
    investigation_type: str | None
    env_material: str | None
    collection_date: datetime.date | str | None
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
    membr_cut: bool | str | None
    samp_collect_device: str | None
    samp_mat_process: str | None
    samp_mat_process_dev: str | None
    samp_store_date: datetime.date | str | None
    samp_store_loc: str | None
    samp_store_temp: float | int | None
    store_person: str | None
    store_person_orcid: str | None
    other_person: str | None
    other_person_orcid: str | None
    long_store: bool | str | None
    ship_date: datetime.date | str | None
    arr_date_hq: datetime.date | str | None
    store_temp_hq: float | int | None
    ship_date_seq: datetime.date | str | None
    arr_date_seq: datetime.date | str | None
    failure: bool | str | None
    failure_comment: str | None
    ENA_accession_number_sample: str | None
    source_mat_id: str | None

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

    # God I hate NaNs
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

    @field_validator("membr_cut", "long_store", "failure")
    @classmethod
    def coerce_to_bool(cls, value: str | bool | None) -> bool | None:

        if (
            value == "N\t2022-10-17\t2022-10-19\t-70\t2023-06-01\t2023-06-01\t\t\t"
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

    @field_validator("collection_date", "samp_store_date", "ship_date", "arr_date_hq")
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

    @field_serializer("collection_date", "samp_store_date", "ship_date", "arr_date_hq")
    def serialize_dates(self, value: datetime.date | None) -> str | None:
        if isinstance(value, datetime.date):
            return value.strftime("%Y-%m-%d")
        else:
            return None
