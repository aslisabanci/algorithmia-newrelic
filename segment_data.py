import Algorithmia
import pandas as pd
import sys
import time

from pandas.core.frame import DataFrame

if __name__ == "__main__":
    client = Algorithmia.client(
        "simY73xk1582WI06j5CQCpddcJ/1", "https://api.devopsbay55.enthalpy.click"
    )
    algo = client.algo(f"asli_org/randomforest_creditcardapproval/0.1.0")

    # parquet_path = "/Users/aslisabanci/Downloads/clean-data.parquet"
    # clean_data_ds = pd.read_parquet(parquet_path)

    clean_data_ds = pd.read_csv(
        "/Users/aslisabanci/repos/algorithmia-newrelic/data/all.csv"
    )
    print(clean_data_ds.shape)

    records = clean_data_ds.to_dict("records")
    approveds = []
    rejecteds = []
    # for i in range(10):
    #     record = records[i]
    for record in records:
        # time.sleep(1)
        result = algo.pipe(record).result
        print(result)
        if result["approved"]:
            approveds.append(record)
        else:
            rejecteds.append(record)

    approved_ds = DataFrame.from_dict(approveds)
    rejected_ds = DataFrame.from_dict(rejecteds)
    approved_ds.to_csv("randomforest_creditcardapproval-approve.csv")
    rejected_ds.to_csv("randomforest_creditcardapproval-reject.csv")

    # input = {
    # "owns_home": 1,
    # "child_one": 0,
    # "child_two_plus": 0,
    # "has_work_phone": 0,
    # "age_high": 0,
    # "age_highest": 1,
    # "age_low": 0,
    # "age_lowest": 0,
    # "employment_duration_high": 0,
    # "employment_duration_highest": 0,
    # "employment_duration_low": 0,
    # "employment_duration_medium": 0,
    # "occupation_hightech": 0,
    # "occupation_office": 1,
    # "family_size_one": 1,
    # "family_size_three_plus": 0,
    # "housing_coop_apartment": 0,
    # "housing_municipal_apartment": 0,
    # "housing_office_apartment": 0,
    # "housing_rented_apartment": 0,
    # "housing_with_parents": 0,
    # "education_higher_education": 0,
    # "education_incomplete_higher": 0,
    # "education_lower_secondary": 0,
    # "marital_civil_marriage": 0,
    # "marital_separated": 0,
    # "marital_single_not_married": 1,
    # "marital_widow": 0
    # }
