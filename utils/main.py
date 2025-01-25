import pandas as pd
from typing import Dict, List



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


def get_list_dict_metrics(df_only_numeric: pd.DataFrame) -> list[Dict]:
    """Cálcula o máximo, mínimo, a média e a soma para todos os campos do dataframe enviado.

    Args:
        df_only_numeric (pd.DataFrame): Dataframe contendo apenas campos numéricos, onde será possível realizar o cálculo.

    Returns:
        list[Dict]: Lista com todas as métricas para todos os campos contidos no dataframe, seguindo o exemplo (dado que o dataframe contenha
        os seguintes campos: "Campo1" e "Campo2"):[
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
        }]
    """
    list_fields = list(df_only_numeric.keys())
    list_metrics = []
    for field in list_fields:
        list_metrics.append(
            {field :
            {
                "max": float(df_only_numeric[field].max()),
                "min": float(df_only_numeric[field].min()),
                "avg": float(df_only_numeric[field].mean()),
                "sum": float(df_only_numeric[field].sum())
                }
            }
        )
    return list_metrics


def get_dataframe_from_list_dict(list_dicio: List[Dict]) -> pd.DataFrame:
    """Da lista de dicionários recebida, converte em um dataframe, onde cada dicionário
    se torna um dataframe, e todos são concatenados em um dataframe final.

    Args:
        list_dicio (List[Dict]): Lista de dicionários, oriundo da saída da função `get_list_dict_metrics` 

    Returns:
        pd.DataFrame: Dataframe com o conteúdo de cada dicionário na lista de dicionários usada como argumento.
    """
    lista_dataframes = []
    value = {}
    for n, dicio in enumerate(list_dicio):
        name = list(dicio.keys())[0]
        value["name"] = name
        value.update(list_dicio[n][name])
        lista_dataframes.append(pd.DataFrame([value]))
    
    df_all = pd.concat(lista_dataframes, ignore_index=True) 
    return df_all



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename")
    argumento = parser.parse_args()
    file = argumento.filename
    df = get_dataframe(file)
    list_fields = ["Sodium", "Carbs", "Fiber", "Sugars", "Protein", "WeightWatchersPnts"]
    df_only_numeric = get_dataframe_only_numeric(df, list_fields)
    list_metrics = get_list_dict_metrics(df_only_numeric)
    df_metrics = get_dataframe_from_list_dict(list_metrics)
    with pd.ExcelWriter('analise_quantitativa.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Conteúdo do Arquivo', index=False)
        df_metrics.to_excel(writer, sheet_name='Métricas', index=False)