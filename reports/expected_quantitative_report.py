import pandas as pd
from typing import Dict, List


class ExpectedQuantitativeReport:
    def __init__(self, path: str, sep: str=",", list_fields: list=None):
        self.path = path
        self.sep = sep
        self.list_fields = list_fields
    
    def get_dataframe(self) -> pd.DataFrame:
        return pd.read_csv(self.path, sep=self.sep)
    

    def get_dataframe_numeric_fields(self) -> dict:
        self.df = self.get_dataframe()
        dicio_types = {key: str(self.df.dtypes[key]) for key in self.df.keys()}
        new_dicio = {}
        for key, value in dicio_types.items():
            if value in ("int64", "float64"):
                new_dicio[key] = value
        return new_dicio


    def get_dataframe_only_numeric(self) -> pd.DataFrame:
        self.df = self.get_dataframe()
        if self.list_fields and len(self.list_fields) > 0:
            new_df = pd.DataFrame()
            for field in self.list_fields:
                new_df[field] = pd.to_numeric(self.df[field], errors="coerce")
            return new_df
        
        dicio_types = self.get_dataframe_numeric_fields()
        print(dicio_types)
        if not dicio_types:
            print("Campos devem ser informados, pois o documento analisado possui todos os campos como string!")
            return exit()
        numeric_keys = [key for key, value in dicio_types.items() if value in ["int64", "float64"]]
        new_df = self.df[numeric_keys]
        return new_df


    def get_list_dict_metrics(self) -> List[Dict]:
        self.df_only_numeric = self.get_dataframe_only_numeric()  
        list_fields = list(self.df_only_numeric.keys())
        list_metrics = []
        for field in list_fields:
            list_metrics.append(
                {field :
                {
                    "max": float(self.df_only_numeric[field].max()),
                    "min": float(self.df_only_numeric[field].min()),
                    "avg": float(self.df_only_numeric[field].mean()),
                    "sum": float(self.df_only_numeric[field].sum())
                    }
                }
            )
        return list_metrics
    

    def get_dataframe_from_list_dict(self) -> pd.DataFrame:
        self.list_dicio = self.get_list_dict_metrics()
        lista_dataframes = []
        value = {}
        for n, dicio in enumerate(self.list_dicio):
            name = list(dicio.keys())[0]
            value["name"] = name
            value.update(self.list_dicio[n][name])
            lista_dataframes.append(pd.DataFrame([value]))
        
        df_all = pd.concat(lista_dataframes, ignore_index=True) 
        return df_all
    

    def export_numeric_report_to_excel(self):
        try:
            df1 = self.get_dataframe()
            df1_metrics = self.get_dataframe_from_list_dict()
            name = f"{self.path.split(".")[0]}"
            with pd.ExcelWriter(f"analise_quantitativa_{name}_.xlsx", engine="openpyxl") as writer:
                df1.to_excel(writer, sheet_name=name, index=False)
                df1_metrics.to_excel(writer, sheet_name=f"Métricas {name}")
            return True
        except Exception as e:
            print(f"Deu merda: {e}")



if __name__ == "__main__":
    #import ipdb
    #ipdb.set_trace()
    file = "FastFoodNutritionMenu1.csv"

    report_obj = ExpectedQuantitativeReport(path=file)
    print(report_obj.get_list_dict_metrics())
    report_obj.export_numeric_report_to_excel()
