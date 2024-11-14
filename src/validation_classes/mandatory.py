from typing import Any, Optional

from pydantic import BaseModel


class Model(BaseModel):
    # Mandatory fields
    arr_date_hq: Any
    arr_date_seq: Any
    chlorophyll: Any
    chlorophyll_method: Any
    collection_date: Any
    contact_email: Any
    contact_name: Any
    depth: Any
    ENA_accession_number_project: Any
    ENA_accession_number_sample: Any
    ENA_accession_number_umbrella: Any
    env_broad_biome: Any
    env_local: Any
    env_material: Any
    env_package: Any
    extra_site_info: Any
    failure: Any
    failure_comment: Any
    geo_loc_name: Any
    investigation_type: Any
    latitude: Any
    loc_broad_ocean: Any
    loc_broad_ocean_mrgid: Any
    loc_loc: Any
    loc_loc_mrgid: Any
    loc_regional: Any
    loc_regional_mrgid: Any
    long_store: Any
    longitude: Any
    membr_cut: Any
    obs_id: Any
    organization: Any
    organization_country: Any
    organization_edmoid: Any
    project_name: Any
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
    scientific_name: Any
    sea_subsurf_salinity: Any
    sea_subsurf_salinity_method: Any
    sea_subsurf_temp: Any
    sea_subsurf_temp_method: Any
    sea_surf_salinity: Any
    sea_surf_salinity_method: Any
    sea_surf_temp: Any
    sea_surf_temp_method: Any
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
    tot_depth_water_col: Any
    wa_id: Any

    # Optional fields
    alkalinity: Optional[Any] = None
    alkalinity_method: Optional[Any] = None
    ammonium: Optional[Any] = None
    ammonium_method: Optional[Any] = None
    bac_prod: Optional[Any] = None
    bac_prod_method: Optional[Any] = None
    biomass: Optional[Any] = None
    biomass_method: Optional[Any] = None
    chem_administration: Optional[Any] = None
    conduc: Optional[Any] = None
    conduc_method: Optional[Any] = None
    contact_orcid: Optional[Any] = None
    density: Optional[Any] = None
    density_method: Optional[Any] = None
    diss_carb_dioxide: Optional[Any] = None
    diss_carb_dioxide_method: Optional[Any] = None
    diss_inorg_carb: Optional[Any] = None
    diss_inorg_carb_method: Optional[Any] = None
    diss_org_carb: Optional[Any] = None
    diss_org_carb_method: Optional[Any] = None
    diss_org_nitro: Optional[Any] = None
    diss_org_nitro_method: Optional[Any] = None
    diss_oxygen: Optional[Any] = None
    diss_oxygen_method: Optional[Any] = None
    down_par: Optional[Any] = None
    down_par_method: Optional[Any] = None
    n_alkanes: Optional[Any] = None
    n_alkanes_method: Optional[Any] = None
    nitrate: Optional[Any] = None
    nitrate_method: Optional[Any] = None
    nitrite: Optional[Any] = None
    nitrite_method: Optional[Any] = None
    noteworthy_env_cond: Optional[Any] = None
    organism_count: Optional[Any] = None
    organism_count_method: Optional[Any] = None
    other_person: Optional[Any] = None
    other_person_orcid: Optional[Any] = None
    part_org_carb: Optional[Any] = None
    part_org_carb_method: Optional[Any] = None
    part_org_nitro: Optional[Any] = None
    part_org_nitro_method: Optional[Any] = None
    petroleum_hydrocarb: Optional[Any] = None
    petroleum_hydrocarb_method: Optional[Any] = None
    ph: Optional[Any] = None
    ph_method: Optional[Any] = None
    phaeopigments: Optional[Any] = None
    phaeopigments_method: Optional[Any] = None
    phosphate: Optional[Any] = None
    phosphate_method: Optional[Any] = None
    pigments: Optional[Any] = None
    pigments_method: Optional[Any] = None
    pressure: Optional[Any] = None
    pressure_method: Optional[Any] = None
    primary_prod: Optional[Any] = None
    primary_prod_method: Optional[Any] = None
    sampl_person_orcid: Optional[Any] = None
    silicate: Optional[Any] = None
    silicate_method: Optional[Any] = None
    store_person_orcid: Optional[Any] = None
    sulfate: Optional[Any] = None
    sulfate_method: Optional[Any] = None
    sulfide: Optional[Any] = None
    sulfide_method: Optional[Any] = None
    tidal_stage: Optional[Any] = None
    turbidity: Optional[Any] = None
    turbidity_method: Optional[Any] = None
    water_current: Optional[Any] = None
    water_current_method: Optional[Any] = None
