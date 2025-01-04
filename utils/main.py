import pandas as pd
from typing import Dict

file = "FastFoodNutritionMenu2.csv"
df = pd.read_csv(file, sep=",")

def get_dataframe(path: str, sep: str=",") -> pd.DataFrame:
    """Manipula o arquivo retornando um dataframe

    Args:
        path (str): Caminho do arquivo csv
        sep (str, optional): O separador que é usado no arquivo. Defaults to ",".

    Returns:
        pd.DataFrame: Dataframe do conteúdo do arquivo csv
    """
    return pd.read_csv(path, sep=sep)


def get_dataframe_only_numeric(df: pd.DataFrame, list_fields: list) -> pd.DataFrame:
    """Manipula o dataframe garantindo que os campos passados estejam presentes no dataframe retornado como campos float  

    Args:
        df (pd.DataFrame): O dataframe que deve conter campos float
        list_fields (list): Lista com nomes dos campos floats

    Returns:
        pd.DataFrame: Um dataframe com somente os campos informados, estes campos serão todos do tipo float.
    """
    new_df = pd.DataFrame()
    for field in list_fields:
        new_df[field] = pd.to_numeric(df[field], errors="coerce")
    return new_df


def get_dataframe_metrics(df_only_numeric: pd.DataFrame) -> list[Dict]:
    """Cálcula o máximo, mínimo, a média e a soma para todos os campos do dataframe enviado.

    Args:
        df_only_numeric (pd.DataFrame): Dataframe contendo apenas campos numéricos, onde será possível realizar o cálculo.

    Returns:
        list[Dict]: Lista com todas as métricas para todos os campos contidos no dataframe, seguindo o exemplo (dado que o dataframe contenha
        os seguintes campos: "Campo1" e "Campo2"):
        {"Campo1":
            {
            "max": 100,
            "min": 10,
            "avg": 5,
            "sum": 1000
            },
        "Campo2":
            {
            "max": 200,
            "min": 20,
            "avg": 10,
            "sum": 2000
            }
        }
    """
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