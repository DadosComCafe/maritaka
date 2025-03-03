from expected_quantitative_report import ExpectedQuantitativeReport
from real_quantitative_report import RealQuantitativeReport


if __name__ == "__main__":
    depara = "FastFoodNutritionMenu1.csv"
    real = "FastFoodNutritionMenu2.csv"

    depara_report_obj = ExpectedQuantitativeReport(path=depara)
    print(depara_report_obj.get_list_dict_metrics())
    depara_report_obj.export_numeric_report_to_excel()

    real_report_obj = RealQuantitativeReport(path=real)
    print(real_report_obj.get_list_dict_metrics())
    real_report_obj.export_numeric_report_to_excel()
