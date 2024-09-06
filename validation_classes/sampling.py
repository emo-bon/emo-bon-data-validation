import math
import datetime
from pydantic import BaseModel, field_validator, model_validator, ValidationError, Field, AliasChoices, field_serializer, validator
from typing import Any, Optional, Union

# The type Optional[x] is a shorthand for Union[x, None].
# Optional[x] can also be used to specify a required field that can take None as a value.
# The Union type allows a model attribute to accept different types
# If a field is missing from a sheet "=<value>" will add it and give it a default value

# TODO: add checks for ranges that the low value is lower that the upper value

# Types have been compared to https://github.com/emo-bon/observatory-profile/blob/main/logsheet_schema_extended.csv
# Most of the out types are the in-types for the triples, apart from the bools and datetime.date fields

class Model(BaseModel):
    source_mat_id_orig:            Optional[str]
    samp_description:              Optional[str]
    tax_id:                        Union[int, float, None]               # Serialised to int, floats are due to NaNs being present
    scientific_name:               Optional[str] 
    investigation_type:            Optional[str] 
    env_material:                  Optional[str]
    collection_date:               Optional[str]                         # Serialised to datetime.date
    sampling_event:                Optional[str]
    sampl_person:                  Optional[str] 
    sampl_person_orcid:            Optional[str] 
    tidal_stage:                   Optional[str] 
    depth:                         Union[str, float, None]               # TODO serialise to str
    replicate:                     Union[str, int, float, None]          # Serialised to str
    samp_size_vol:                 Union[int, float, None] = None        # TODO serialise to float
    time_fi:                       Union[str, float, None] = None        # TODO serialise to str
    size_frac:                     Union[str, float, None] = None        # TODO serialise to str
    size_frac_low:                 Optional[float]
    size_frac_up:                  Optional[float]
    membr_cut:                     Union[bool, str, None] = None         # Serialised as bool         
    samp_collect_device:           Optional[str] 
    samp_mat_process:              Optional[str]
    samp_mat_process_dev:          Optional[str]
    samp_store_date:               Optional[str]                         # Serialised to datetime.date
    samp_store_loc:                Optional[str]
    samp_store_temp:               Optional[int]
    store_person:                  Optional[str]
    store_person_orcid:            Optional[str] = None
    other_person:                  Optional[str]
    other_person_orcid:            Optional[str]
    long_store:                    Union[bool, str, None]                 # Serialised to bool
    ship_date:                     Optional[str]                          # Serialised to datetime.date
    arr_date_hq:                   Optional[str] = None                   # Serialised to datetime.date
    store_temp_hq:                 Union[int, str, None]                  # Serialised to int
    ship_date_seq:                 Optional[str]                          # Serialised to date
    arr_date_seq:                  Optional[str]                          # Serialised to date
    failure:                       Union[bool, str, None]                 # Serialised to bool
    failure_comment:               Optional[str]
    ENA_accession_number_sample:   Optional[str] = None
    source_mat_id:                 str = Field(..., validation_alias=AliasChoices("source_mat_id", "source_material_id"))
    
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

    # Replace NaNs 
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

    # Get rid of "NA" "N/A"'s
    # These are in the original sheets and does not take account of pandas.NA types
    # there should be no pandas.NA anyway
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
    def coerce_to_bool(cls, value: Optional[str]) -> Optional[bool]:
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
                raise ValueError(f"Unrecognised value: {value}")
            else:
                if vl in ["y", "t"]:
                    return True
                else:
                    return False

    @field_validator("store_temp_hq")
    @classmethod
    def coerce_store_temp_hq(cls, value: Union[int, str]) -> int:
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
                    raise ValueError(f"Unrecognised value: {value}")

    # This is a horrible hack but Googlesheets interprets the work "blank" as NULL/NaN
    # when retrieving the sheet using this old "visualisation" method?!
    # The values in sheets are ints but are coerced to floats by pandas because of the NaNs
    # Here we assume all None's (replaced NaNs, see above) are supposed to be "blank"
    @field_validator("replicate")
    @classmethod
    def coerce_replicate_to_string(cls, value: Union[int, float, None]) -> str:
        #print(f"{value=} is type {type(value)}")
        if not value:
            return "blank"
        if isinstance(value, int):
            return str(value)
        elif isinstance(value, float):
            return str(int(value))
        else:
            raise ValueError(f"Unrecognised value: {value}")
    
    @field_validator("collection_date", "samp_store_date", "ship_date", "arr_date_hq", "ship_date_seq", "arr_date_seq")
    @classmethod
    def coerce_the_date_strings(cls, value: Optional[str]) -> datetime.date:
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
                        raise ValueError(f"Unrecognised value: {value}")
        else:
            raise ValueError(f"Unrecognised value: {value}")

    # Some sheets e.g. OSD74 have NaNs in this field and the values get read as floats by pandas
    # You cannot use standard serialisation because you end up with mixed "int" and "float" sheets
    @field_validator("tax_id")
    @classmethod
    def coerce_tax_id(cls, value: Union[int, float, None]) -> Optional[int]:
        #print(f"Type of {value} is {type(value)}")
        if not value:
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value) # this should be safe because the floats are coerced integers

    @field_serializer("collection_date", "samp_store_date", "ship_date", "arr_date_hq", "ship_date_seq", "arr_date_seq")
    def serialize_dates(self, value: Optional[datetime.date]) -> Optional[str]:
        if isinstance(value, datetime.date):
            return value.strftime("%Y-%m-%d")
        else:
            return None

    @field_serializer("depth", "time_fi", "size_frac")
    def serialize_str_float_to_str(self, value: Union[str, float, None]) -> Optional[str]:
        if isinstance(value, str):
            return value
        elif isinstance(value, float):
            return str(float)
        else:
            return None

    @field_serializer("samp_size_vol")
    def serialize_int_float_to_float(self, value: Union[int, float, None]) -> Optional[float]:
        if isinstance(value, float):
            return value
        elif isinstance(value, int):
            return float(value)
        else:
            return None        
    
    # Some sheets e.g. OSD74 have NaNs in this field and the values get read as floats by pandas
    # You cannot use standard serialisation because you end up with mixed "int" and "float" sheets
    #@field_serializer("tax_id")
    #def serialize_tax_id(self, value: Union[int, float, None]) -> Optional[int]:
    #    #print(f"Type of {value} is {type(value)}")
    #    if not value:
    #        return None
    #    if isinstance(value, int):
    #        return value
    #    if isinstance(value, float):
    #        return int(value) # this should be safe because the floats are coerced integers

################# STRICT ###################################################################

class StrictModel(Model):
    source_mat_id_orig:              str
    samp_description:                str
    tax_id:                          int 
    scientific_name:                 str
    investigation_type:              str
    env_material:                    str
    collection_date:                 Optional[str]
    sampling_event:                  str
    sampl_person:                    str 
    sampl_person_orcid:              Optional[str]
    tidal_stage:                     Optional[str]
    depth:                           int 
    replicate:                       str 
    samp_size_vol:                   int
    time_fi:                         Union[str, int]
    size_frac:                       str
    size_frac_low:                   float # Yes really a float!
    size_frac_up:                    float # Yes really a float! 
    membr_cut:                       Union[bool, str, None] = None
    samp_collect_device:             str
    samp_mat_process:                str
    samp_mat_process_dev:            str
    samp_store_date:                 Optional[str]
    samp_store_loc:                  str
    samp_store_temp:                 int
    store_person:                    str
    store_person_orcid:              Optional[str]
    other_person:                    Optional[str]
    other_person_orcid:              Optional[str]
    long_store:                      Union[bool, str, None] = None
    ship_date:                       Optional[str]
    arr_date_hq:                     Optional[str]
    store_temp_hq:                   int
    ship_date_seq:                   Optional[str]
    arr_date_seq:                    Optional[str] 
    failure:                         Union[bool, str, None] = None
    failure_comment:                 str
    ENA_accession_number_sample:     str
    source_mat_id:                   str

################# SEMI-STRICT ####################################################

class SemiStrictModel(Model):
    source_mat_id_orig:              Optional[str]
    samp_description:                Optional[str]
    tax_id:                          Optional[int]
    scientific_name:                 Optional[str]
    investigation_type:              Optional[str]
    env_material:                    Optional[str]
    collection_date:                 Optional[str]
    sampling_event:                  Optional[str]
    sampl_person:                    Optional[str]
    sampl_person_orcid:              Optional[str]
    tidal_stage:                     Optional[str]
    depth:                           Union[float, int, None]
    replicate:                       Union[str, int, float, None] # Rep int or "blank", hence str raw sheets are broken
    samp_size_vol:                   Union[float, int, None]
    time_fi:                         Union[str, int, None] # Either str "fi" or integer!
    size_frac:                       Optional[str]
    size_frac_low:                   Union[float, int, None]
    size_frac_up:                    Union[float, int, None]
    membr_cut:                       Union[bool, str, None] = None
    samp_collect_device:             Optional[str]
    samp_mat_process:                Optional[str]
    samp_mat_process_dev:            Optional[str]
    samp_store_date:                 Optional[str]
    samp_store_loc:                  Optional[str]
    samp_store_temp:                 Union[float, int, None]
    store_person:                    Optional[str]
    store_person_orcid:              Optional[str]
    other_person:                    Optional[str]
    other_person_orcid:              Optional[str]
    long_store:                      Union[bool, str, None] = None
    ship_date:                       Optional[str]
    arr_date_hq:                     Optional[str]
    store_temp_hq:                   Union[float, int, None]
    ship_date_seq:                   Optional[str]
    arr_date_seq:                    Optional[str]
    failure:                         Union[bool, str, None] = None
    failure_comment:                 Optional[str]
    ENA_accession_number_sample:     Optional[str]
    source_mat_id:                   Optional[str]
