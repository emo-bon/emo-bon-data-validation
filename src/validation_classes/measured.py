from __future__ import annotations

import math
from typing import Any

from pydantic import BaseModel, field_validator, model_validator


class Model(BaseModel):
    source_mat_id: str
    chlorophyll: float | str | None  # str is an annotation error
    chlorophyll_method: str | None
    sea_surf_temp: float | None
    sea_surf_temp_method: str | None
    sea_subsurf_temp: float | str | None = None  # Not taken for soft sediments
    sea_subsurf_temp_method: None | (str) = None  # Not taken for sediments
    sea_surf_salinity: float | str | None = None  # Not taken for soft sediments
    sea_surf_salinity_method: None | (str) = None  # Not taken for soft sediments
    sea_subsurf_salinity: float | str | None = None  # Not taken for soft sediments
    sea_subsurf_salinity_method: None | (str) = None  # Not taken for soft sediments
    alkalinity: str | None
    alkalinity_method: str | None
    ammonium: float | None
    ammonium_method: str | None
    bac_prod: str | None
    bac_prod_method: str | None
    biomass: str | None
    biomass_method: str | None
    chem_administration: str | None
    conduc: float | str | None = None  # Not taken for soft sediments
    conduc_method: str | None = None  # Not taken for soft sediments
    density: float | str | None = None  # Not taken for soft sediments
    density_method: str | None = None  # Not taken for soft sediments
    diss_carb_dioxide: str | None
    diss_carb_dioxide_method: str | None
    diss_inorg_carb: str | None
    diss_inorg_carb_method: str | None
    diss_org_carb: str | None
    diss_org_carb_method: str | None
    diss_org_nitro: str | None
    diss_org_nitro_method: str | None
    down_par: float | None = None  # Not taken for soft sediments
    down_par_method: str | None = None  # Not taken for soft sediments
    diss_oxygen: float | str | None
    diss_oxygen_method: str | None
    n_alkanes: str | None
    n_alkanes_method: str | None
    nitrate: float | None
    nitrate_method: str | None
    nitrite: float | None
    nitrite_method: str | None
    organism_count: str | None
    organism_count_method: str | None
    ph: float | str | None
    ph_method: str | None
    part_org_carb: str | None
    part_org_carb_method: str | None
    part_org_nitro: str | None
    part_org_nitro_method: str | None
    petroleum_hydrocarb: str | None
    petroleum_hydrocarb_method: str | None
    phaeopigments: str | None
    phaeopigments_method: str | None
    phosphate: float | str | None
    phosphate_method: str | None
    pigments: str | None
    pigments_method: str | None
    pressure: float | str | None
    pressure_method: str | None
    primary_prod: str | None = None  # Not taken for soft sediments
    primary_prod_method: str | None = None  # Not taken for soft sediments
    silicate: float | None
    silicate_method: str | None
    sulfate: str | None
    sulfate_method: str | None
    sulfide: str | None
    sulfide_method: str | None
    turbidity: float | None = None  # Not taken for soft sediments
    turbidity_method: str | None = None  # Not taken for soft sediments
    water_current: str | None
    water_current_method: str | None

    # Let's get rid of empty strings first:
    @model_validator(mode="before")
    @classmethod
    def contains_a_blank_string(cls, model: Any) -> Any:
        for key in model:
            # print(f"Value in blank_strings {value}")
            if isinstance(model[key], str) and model[key].strip() == "":
                model[key] = None
        return model

    # Squash NaNs
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

    # Any strings in these fields are annotations and can be ignored
    @field_validator(
        "chlorophyll",
        "sea_surf_salinity",
        "sea_subsurf_salinity",
        "phosphate",
        "diss_oxygen",
        "pressure",
        "density",
    )
    @classmethod
    def coerce_str_to_float(cls, value: float | str | None) -> float | None:
        if not value:
            return None
        if isinstance(value, float):
            return value
        if isinstance(value, str):
            # BPNS has "Expected 12-2024"
            # ESC68N has 'could not retrieve CTD'
            # If it cannot be automatically coerced to a float, return None
            return None
        else:
            raise ValueError(f"Error: unrecognised value {value}")

    @field_validator("sea_subsurf_temp", "ph")
    @classmethod
    def coerce_str_float_with_comma_to_float(
        cls, value: float | str | None
    ) -> float | None:
        if not value:
            return None
        if isinstance(value, float):
            return value
        if isinstance(value, str):
            try:
                return float(value.replace(",", "."))
            except ValueError:
                # NRMCB has '16,7041'
                return None
        else:
            raise ValueError(f"Error: unrecognised value {value}")

    @field_validator("conduc")
    @classmethod
    def coerce_string_float_with_comma_to_float(
        cls, value: float | str | None
    ) -> float | None:
        # e.g. input_value='36,356.62'
        if not value:
            return None
        if isinstance(value, float):
            return value
        if isinstance(value, str):
            if "." in value:
                try:
                    return float(value.replace(",", ""))
                except ValueError:
                    # NRMCB has '16,7041'
                    return None
            else:
                return None
        else:
            raise ValueError(f"Error: unrecognised value {value}")
