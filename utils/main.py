import pandas as pd
from typing import Dict, List, Tuple



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


def get_list_dict_metrics(df_only_numeric: pd.DataFrame) -> List[Dict]:
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

def compare_numeric_dataframes(df1: pd.DataFrame, df2: pd.DataFrame) -> List[Dict]:
    list1, list2 = list(df1["name"]), list(df2["name"])
    list_comparation = []
    if list1 == list2:
        #TODO: pensar em como fazer caso o contrário
        for name in list1:
            #caso em que os dois arquivos possuem os mesmos campos numéricos
            df_n1, df_n2 = df1.loc[df1["name"] == name], df2.loc[df2["name"] == name]
            list_comparation.append(
                {name:
                 {
                     "diff_max": float(df_n1["max"] - df_n2["max"]),
                     "diff_min": float(df_n1["min"] - df_n2["min"]),
                     "diff_avg": float(df_n1["avg"] - df_n2["avg"]),
                     "diff_sum": float(df_n1["sum"] - df_n2["sum"])
                 }}
            )
            print("OK")
    return list_comparation


def get_couple_dataframes(path1: str, path2: str, list_fields: list, sep=",") -> Tuple[pd.DataFrame]:
    df1 = get_dataframe(path1, sep)
    df2 = get_dataframe(path2, sep)
    df1n = get_dataframe_only_numeric(df1, list_fields)
    df2n = get_dataframe_only_numeric(df2, list_fields)
    list_metrics1 = get_list_dict_metrics(df1n)
    list_metrics2 = get_list_dict_metrics(df2n)
    df1_metrics = get_dataframe_from_list_dict(list_metrics1)
    df2_metrics = get_dataframe_from_list_dict(list_metrics2)
    list_dict_comparation = compare_numeric_dataframes(df1=df1_metrics, df2=df2_metrics)
    df_comparation = get_dataframe_from_list_dict(list_dict_comparation)
    try:
        with pd.ExcelWriter('analise_quantitativa.xlsx', engine="openpyxl") as writer:
            name1 = f"{path1.split(".")[0]}"
            name2 = f"{path2.split(".")[0]}"
            df1.to_excel(writer, sheet_name=name1, index=False)
            df1_metrics.to_excel(writer, sheet_name=f"Métricas {name1}")
            df2.to_excel(writer, sheet_name=name2, index=False)
            df2_metrics.to_excel(writer, sheet_name=f"Métricas {name2}")
            df_comparation.to_excel(writer, sheet_name="Comparação")
        return True
    except Exception as e:
        print(f"Deu merda: {e}")
    #return final_df1, final_df2


def get_dataframe_numeric_fields(df: pd.DataFrame) -> dict | False:
    dicio_types = {key: str(df.dtypes[key]) for key in df.keys()}
    if "int64" in dicio_types.values() or "float64" in dicio_types.values():
        return dicio_types
    return False
    


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f1", "--filename1")
    parser.add_argument("-f2", "--filename2")
    #parser.add_argument("-l", "--list_fields")
    argumento = parser.parse_args()
    file1 = argumento.filename1
    file2 = argumento.filename2
    #fields_list = argumento.list_fields
    print(file1, file2)
    get_couple_dataframes(path1=file1, path2=file2, list_fields=["Sodium", "Carbs", "Fiber", "Sugars", "Protein", "WeightWatchersPnts"])