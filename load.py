import Algorithmia
import pandas as pd
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument(
    "-s",
    action="store",
    default="all",
    help="Data segment to use:all, approve or reject",
)
argparser.add_argument(
    "-v", action="store", default="0.1.1", help="Algorithm version to call"
)
argparser.add_argument(
    "-home", action="store", default=None, help="Sets owns_home input feature to 1 or 0"
)
argparser.add_argument(
    "-phone",
    action="store",
    default=None,
    help="Sets has_work_phone input feature to 1 or 0",
)

args = argparser.parse_args()
print(vars(args))

while True:
    to_load = args.s
    version = args.v
    owns_home = args.home
    has_work_phone = args.phone

    input_ds = pd.read_csv(f"./data/{to_load}.csv")
    print(input_ds.shape)

    client = Algorithmia.client(
        "simqUvvKryCWCWgjihWcuGv7fro1", "https://api.therealreal.productionize.ai"
    )
    algo = client.algo(f"asli_algorithmia_trr/credit_card_approval/{version}")

    records = input_ds.to_dict("records")
    for record in records:
        if owns_home is not None:
            record["owns_home"] = owns_home
        if has_work_phone is not None:
            record["has_work_phone"] = has_work_phone

        result = algo.pipe(record).result
        record_owns_home = record["owns_home"]
        record_has_work_phone = record["has_work_phone"]
        print(f"{result} from v{version}, {record_owns_home}, {record_has_work_phone}")
