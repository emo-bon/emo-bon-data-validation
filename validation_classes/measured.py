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
)
from typing import Any, Optional, Union


class Model(BaseModel):
    source_mat_id: str = Field(
        ..., validation_alias=AliasChoices("source_mat_id", "source_material_id")
    )
    chlorophyll: Union[float, str, None]
    chlorophyll_method: Optional[str]
    sea_surf_temp: Optional[float]
    sea_surf_temp_method: Optional[str]
    sea_subsurf_temp: Union[float, str, None] = None  # Not taken for soft sediments
    sea_subsurf_temp_method: Optional[str] = None  # Not taken for soft sediments
    sea_surf_salinity: Union[float, str, None] = None  # Not taken for soft sediments
    sea_surf_salinity_method: Optional[str] = None  # Not taken for soft sediments
    sea_subsurf_salinity: Union[float, str, None] = None  # Not taken for soft sediments
    sea_subsurf_salinity_method: Optional[str] = None  # Not taken for soft sediments
    alkalinity: Optional[str]
    alkalinity_method: Optional[str]
    ammonium: Optional[float]
    ammonium_method: Optional[str]
    bac_prod: Optional[str]
    bac_prod_method: Optional[str]
    biomass: Optional[str]
    biomass_method: Optional[str]
    chem_administration: Optional[str]
    conduc: Union[float, str, None] = None  # Not taken for soft sediments
    conduc_method: Optional[str] = None  # Not taken for soft sediments
    density: Union[float, str, None] = None  # Not taken for soft sediments
    density_method: Optional[str] = None  # Not taken for soft sediments
    diss_carb_dioxide: Optional[str]
    diss_carb_dioxide_method: Optional[str]
    diss_inorg_carb: Optional[str]
    diss_inorg_carb_method: Optional[str]
    diss_org_carb: Optional[str]
    diss_org_carb_method: Optional[str]
    diss_org_nitro: Optional[str]
    diss_org_nitro_method: Optional[str]
    down_par: Optional[float] = None  # Not taken for soft sediments
    down_par_method: Optional[str] = None  # Not taken for soft sediments
    diss_oxygen: Union[float, str, None]
    diss_oxygen_method: Optional[str]
    n_alkanes: Optional[str]
    n_alkanes_method: Optional[str]
    nitrate: Optional[float]
    nitrate_method: Optional[str]
    nitrite: Optional[float]
    nitrite_method: Optional[str]
    organism_count: Optional[str]
    organism_count_method: Optional[str]
    ph: Union[float, str, None]
    ph_method: Optional[str]
    part_org_carb: Optional[str]
    part_org_carb_method: Optional[str]
    part_org_nitro: Optional[str]
    part_org_nitro_method: Optional[str]
    petroleum_hydrocarb: Optional[str]
    petroleum_hydrocarb_method: Optional[str]
    phaeopigments: Optional[float]
    phaeopigments_method: Optional[str]
    phosphate: Union[float, str, None]
    phosphate_method: Optional[str]
    pigments: Union[float, str, None]
    pigments_method: Optional[str]
    pressure: Union[float, str, None]
    pressure_method: Optional[str]
    primary_prod: Optional[str] = None  # Not taken for soft sediments
    primary_prod_method: Optional[str] = None  # Not taken for soft sediments
    silicate: Optional[float]
    silicate_method: Optional[str]
    sulfate: Optional[str]
    sulfate_method: Optional[str]
    sulfide: Optional[str]
    sulfide_method: Optional[str]
    turbidity: Optional[float] = None  # Not taken for soft sediments
    turbidity_method: Optional[str] = None  # Not taken for soft sediments
    water_current: Optional[str]
    water_current_method: Optional[str]

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

    # Squash NaNs
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

    @field_validator(
        "chlorophyll",
        "sea_surf_salinity",
        "sea_subsurf_salinity",
        "phosphate",
        "pigments",
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
            try:
                return float(value)
            except ValueError:
                # BPNS has "Expected 12-2024"
                # ESC68N has 'could not retrieve CTD'
                return None
        else:
            raise ValueError(f"What the hell is this: {value}")

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
            raise ValueError(f"What the hell is this: {value}")

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
            raise ValueError(f"What the hell is this: {value}")
