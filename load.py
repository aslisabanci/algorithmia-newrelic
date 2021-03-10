import Algorithmia
import pandas as pd
import sys

if __name__ == "__main__":
    while True:
        to_load = "all"
        version = "0.1.1"
        owns_home = "-"
        has_work_phone = "-"
        args = sys.argv[1:]
        if len(args):
            to_load = args[0]
            version = args[1]
            owns_home = args[2]
            has_work_phone = args[3]

        input_ds = pd.read_csv(f"./data/{to_load}.csv")
        print(input_ds.shape)

        client = Algorithmia.client(
            "simqUvvKryCWCWgjihWcuGv7fro1", "https://api.therealreal.productionize.ai"
        )
        algo = client.algo(f"asli_algorithmia_trr/credit_card_approval/{version}")

        records = input_ds.to_dict("records")
        for record in records:
            if owns_home == "1":
                record["owns_home"] = 1
            elif owns_home == "0":
                record["owns_home"] = 0

            if has_work_phone == "1":
                record["has_work_phone"] = 1
            elif has_work_phone == "0":
                record["has_work_phone"] = 0

            result = algo.pipe(record).result
            owns_home_modified = record["owns_home"]
            has_work_phone_modified = record["has_work_phone"]
            print(
                f"{result} from v{version}, {owns_home_modified}, {has_work_phone_modified}"
            )
