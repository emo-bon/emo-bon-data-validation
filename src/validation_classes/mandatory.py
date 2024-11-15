"""
Processing BPNS... water column
Sample sheet data: https://docs.google.com/spreadsheets/d/1mEi4Bd2YR63WD0j54FQ6QkzcUw_As9Wilue9kaXO2DE/gviz/tq?tqx=out:csv&sheet=Updated%20definitions
Sheet type link: https://docs.google.com/spreadsheets/d/1mEi4Bd2YR63WD0j54FQ6QkzcUw_As9Wilue9kaXO2DE/edit?usp=sharing
Length wc_mandatory fields 32
Length wc_optional fields 6
Fields: ['arr_date_hq', 'arr_date_seq', 'collection_date', 'depth', 'env_material', 'failure', 'failure_comment',
         'investigation_type', 'long_store', 'membr_cut', 'replicate', 'samp_collect_device', 'samp_description',
         'samp_mat_process', 'samp_mat_process_dev', 'samp_size_vol', 'samp_store_date', 'samp_store_loc',
         'samp_store_temp', 'sampl_person', 'sampling_event', 'ship_date', 'ship_date_seq', 'size_frac',
         'size_frac_low', 'size_frac_up', 'source_mat_id_orig', 'source_mat_id', 'store_person', 'store_temp_hq',
         'tax_id', 'time_fi']
Fields: ['noteworthy_env_cond', 'other_person', 'other_person_orcid', 'sampl_person_orcid', 'store_person_orcid',
         'tidal_stage']


Processing BPNS... soft sediment
Sample sheet data: https://docs.google.com/spreadsheets/d/1zc0bZdpl-Eoi35lI_5BGkElbscplyQRyNPLkSgeEyEQ/gviz/tq?tqx=out:csv&sheet=Updated%20definitions
Sheet type link: https://docs.google.com/spreadsheets/d/1zc0bZdpl-Eoi35lI_5BGkElbscplyQRyNPLkSgeEyEQ/edit?usp=sharing
Length ss_mandatory fields 29 (NOTE: samp_store_date appears 2 times)
Length ss_optional fields 6
Fields: ['arr_date_hq', 'arr_date_seq', 'collection_date', 'comm_samp', 'depth', 'env_material', 'failure', 'failure_comment', 'investigation_type', 'long_store', 'replicate', 'samp_collect_device', 'samp_store_date', 'samp_mat_process', 'samp_mat_process_dev', 'samp_size_mass', 'samp_store_date', 'samp_store_loc', 'samp_store_temp', 'sampl_person', 'sampling_event', 'ship_date', 'ship_date_seq', 'size_frac_low', 'size_frac_up', 'source_mat_id_orig', 'source_mat_id', 'store_person', 'store_temp_hq']
Fields: ['noteworthy_env_cond', 'other_person', 'other_person_orcid', 'sampl_person_orcid', 'store_person_orcid', 'tidal_stage']

Length of wc_fields: 38
Length of ss_fields: 35
Checking for duplicates in water_column...
Checking for duplicates in soft_sediment...
Field samp_store_date appears 2 times
Water column mandatory fields: 32
Water column optional fields: 6
Soft sediment mandatory fields: 29
Soft sediment optional fields: 6
All MANDATORY fields: 34
Common MANDATORY fields in both WC and SS: 26
MANDATORY fields only in WC: 6
MANDATORY fields only in SS: 2
Common OPTIONAL fields in both WC and SS: 6
All OPTIONAL fields: 6
OPTIONAL fields only in WC: 0
OPTIONAL fields only in SS: 0

"""

import math
from typing import Optional

from pydantic import BaseModel, model_validator


class WaterColumnDataModel(BaseModel):
    # 32 Mandatory fields
    arr_date_hq: str
    arr_date_seq: str
    collection_date: str
    depth: int | float
    env_material: str
    failure: str
    failure_comment: str
    investigation_type: str
    long_store: str
    membr_cut: str
    replicate: str
    samp_collect_device: str
    samp_description: str
    samp_mat_process: str
    samp_mat_process_dev: str
    samp_size_vol: int
    samp_store_date: str
    samp_store_loc: str
    samp_store_temp: float
    sampl_person: str
    sampling_event: str
    ship_date: str
    ship_date_seq: str
    size_frac: str | float | int
    size_frac_low: float | int
    size_frac_up: float | int
    source_mat_id_orig: str
    source_mat_id: str
    store_person: str
    store_temp_hq: float | int
    tax_id: int
    time_fi: str | int | float

    # 6 Optional fields
    noteworthy_env_cond: Optional[str] = None
    other_person: Optional[str] = None
    other_person_orcid: Optional[str] = None
    sampl_person_orcid: Optional[str] = None
    store_person_orcid: Optional[str] = None
    tidal_stage: Optional[str] = None

    # Replace NaNs
    @model_validator(mode="before")
    @classmethod
    def replace_NaNs(cls, model):
        for key in model:
            # NaNs
            if isinstance(model[key], float) and math.isnan(model[key]):
                model[key] = None
            # Strings
            if isinstance(model[key], str):
                # Empty strings
                if model[key].strip() == "":
                    model[key] = None
                else:
                    # "NA" "N/A"s
                    elem = model[key].strip().lower
                    if elem in ["na", "n a", "n/a", "n / a", "none"]:
                        model[key] = None
        return model


class SoftSedimentDataModel(BaseModel):
    # 28 Mandatory fields
    arr_date_hq: str
    arr_date_seq: str
    collection_date: str
    comm_samp: str
    depth: int | float
    env_material: str
    failure: str
    failure_comment: str
    investigation_type: str
    long_store: str
    replicate: str | int
    samp_collect_device: str
    samp_store_date: str
    samp_mat_process: str
    samp_mat_process_dev: str
    samp_size_mass: int | float
    samp_store_loc: str
    samp_store_temp: int | float
    sampl_person: str
    sampling_event: str
    ship_date: str
    ship_date_seq: str
    size_frac_low: int | float
    size_frac_up: int | float
    source_mat_id_orig: str
    source_mat_id: str
    store_person: str
    store_temp_hq: int | float

    # 6 Optional fields
    noteworthy_env_cond: Optional[str] = None
    other_person: Optional[str] = None
    other_person_orcid: Optional[str] = None
    sampl_person_orcid: Optional[str] = None
    store_person_orcid: Optional[str] = None
    tidal_stage: Optional[str] = None

    # Replace NaNs
    @model_validator(mode="before")
    @classmethod
    def replace_NaNs(cls, model):
        for key in model:
            # NaNs
            if isinstance(model[key], float) and math.isnan(model[key]):
                model[key] = None
            # Strings
            if isinstance(model[key], str):
                # Empty strings
                if model[key].strip() == "":
                    model[key] = None
                else:
                    # "NA" "N/A"s
                    elem = model[key].strip().lower
                    if elem in ["na", "n a", "n/a", "n / a", "none"]:
                        model[key] = None
        return model
