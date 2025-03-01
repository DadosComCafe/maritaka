import pandas as pd
from typing import Dict, List, Tuple


class ExpectedQuantitativeReport:
    def __init__(self, path: str, sep: str=",", list_fields: list=None):
        self.path = path
        self.sep = sep
        self.list_fields = list_fields
    
    def get_dataframe(self) -> pd.DataFrame:
        return pd.read_csv(self.path, sep=self.sep)
    
    def get_dataframe_only_numeric(self) -> pd.DataFrame:
        #TODO Preciso tanto corrigir a função get_dataframe_numeric_fields
        #quanto ajustá-la para fazê-la funcionar aqui!
        self.df = self.get_dataframe()
        if self.list_fields and len(self.list_fields) > 0:
            new_df = pd.DataFrame()
            for field in self.list_fields:
                new_df[field] = pd.to_numeric(self.df[field], errors="coerce")
            return new_df
