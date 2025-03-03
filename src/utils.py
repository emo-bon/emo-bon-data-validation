import pandas as pd

from natsort import natsorted
import math
from pydantic import ValidationError, BaseModel


def validate_df(df: pd.DataFrame, validator: BaseModel, validation_index: str = None):
    errors = []
    validated_rows = []
    not_validated_rows = []
    for index, row in df.iterrows():
        try:
            sample_instance = validator(**row)
            validated_rows.append(sample_instance.model_dump())
        except ValidationError as e:
            error_messages = e.errors()
            errors.append({'index': index, 'errors': error_messages})
            not_validated_rows.append(row)

    validated = pd.DataFrame.from_records(validated_rows, index=validation_index)
    validated.reindex(index=natsorted(validated.index))
    return errors, validated, pd.DataFrame.from_records(not_validated_rows)


def filter_source_mat_df(df: pd.DataFrame):
    try:
        df_filtered = df.dropna(subset=['source_mat_id'])

        # Filter out rows where 'source_mat_id' is a float and not NaN
        df_filtered = df_filtered[~df_filtered['source_mat_id'].apply(lambda x: isinstance(x, float) and not math.isnan(x))]

        # Filter out rows where 'source_mat_id' is None or has less than 4 parts when split by '_'
        df_filtered = df_filtered[df_filtered['source_mat_id'].apply(lambda x: x is not None and len(x.split('_')) >= 4)]
    except (KeyError, ValueError):
        df_filtered = df

    try:
        # Filter out rows where 'source_mat_id_orig' contains "si les filets"
        df_filtered = df_filtered[~df_filtered['source_mat_id_orig'].str.contains("si les filets", na=False)]
    except KeyError:
        pass

    # Print the number of discarded records
    discarded_records = len(df) - len(df_filtered)
    print(f"Discarded {discarded_records} records leaving {len(df_filtered)}.")

    # Continue with the filtered DataFrame
    data_records_filtered = df_filtered.to_dict(orient="records")
    return data_records_filtered, df_filtered