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

from typing import Any, Optional

from pydantic import BaseModel


class WaterColumnDataModel(BaseModel):
    # 32 Mandatory fields
    arr_date_hq: Any
    arr_date_seq: Any
    collection_date: Any
    depth: Any
    env_material: Any
    failure: Any
    failure_comment: Any
    investigation_type: Any
    long_store: Any
    membr_cut: Any
    replicate: Any
    samp_collect_device: Any
    samp_description: Any
    samp_mat_process: Any
    samp_mat_process_dev: Any
    samp_size_vol: Any
    samp_store_date: Any
    samp_store_loc: Any
    samp_store_temp: Any
    sampl_person: Any
    sampling_event: Any
    ship_date: Any
    ship_date_seq: Any
    size_frac: Any
    size_frac_low: Any
    size_frac_up: Any
    source_mat_id_orig: Any
    source_mat_id: Any
    store_person: Any
    store_temp_hq: Any
    tax_id: Any
    time_fi: Any

    # 6 Optional fields
    noteworthy_env_cond: Optional[Any] = None
    other_person: Optional[Any] = None
    other_person_orcid: Optional[Any] = None
    sampl_person_orcid: Optional[Any] = None
    store_person_orcid: Optional[Any] = None
    tidal_stage: Optional[Any] = None


class SoftSedimentDataModel(BaseModel):
    # 28 Mandatory fields
    arr_date_hq: Any
    arr_date_seq: Any
    collection_date: Any
    comm_samp: Any
    depth: Any
    env_material: Any
    failure: Any
    failure_comment: Any
    investigation_type: Any
    long_store: Any
    replicate: Any
    samp_collect_device: Any
    samp_store_date: Any
    samp_mat_process: Any
    samp_mat_process_dev: Any
    samp_size_mass: Any
    samp_store_loc: Any
    samp_store_temp: Any
    sampl_person: Any
    sampling_event: Any
    ship_date: Any
    ship_date_seq: Any
    size_frac_low: Any
    size_frac_up: Any
    source_mat_id_orig: Any
    source_mat_id: Any
    store_person: Any
    store_temp_hq: Any

    # 6 Optional fields
    noteworthy_env_cond: Optional[Any] = None
    other_person: Optional[Any] = None
    other_person_orcid: Optional[Any] = None
    sampl_person_orcid: Optional[Any] = None
    store_person_orcid: Optional[Any] = None
    tidal_stage: Optional[Any] = None
