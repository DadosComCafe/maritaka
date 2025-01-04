import pandas as pd

file = "FastFoodNutritionMenu2.csv"
df = pd.read_csv(file, sep=",")

def get_dataframe(path: str, sep: str=",") -> pd.DataFrame:
    return pd.read_csv(path, sep=sep)


def get_dataframe_only_numeric(df: pd.DataFrame, list_fields: list) -> pd.DataFrame:
    new_df = pd.DataFrame()
    for field in list_fields:
        new_df[field] = pd.to_numeric(df[field], errors="coerce")
    return new_df


def get_dataframe_metrics(df_only_numeric: pd.DataFrame):
    list_fields = list(df_only_numeric.keys())
    list_metrics = []
    for field in list_fields:
        list_metrics.append(
            {
                "max": float(df_only_numeric[field].max()),
                "min": float(df_only_numeric[field].min()),
                "avg": float(df_only_numeric[field].mean()),
                "sum": float(df_only_numeric.sum())
                }
        )
    return list_metrics