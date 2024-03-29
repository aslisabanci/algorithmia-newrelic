import Algorithmia
import pandas as pd
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument(
    "-s",
    action="store",
    default="all",
    help="Data segment to use:all, approve or reject. Defaults to all",
)
argparser.add_argument(
    "-a",
    action="store",
    default="randomforest_creditcardapproval",
    help="Algorithm name to call",
)
argparser.add_argument(
    "-v",
    action="store",
    default="0.1.1",
    help="Algorithm version to call. Defaults to 0.1.1",
)
argparser.add_argument(
    "-home",
    action="store",
    default=None,
    help="Overrides owns_home input feature with 0 or 1. Defaults to None (doesn't change the original value)",
)
argparser.add_argument(
    "-phone",
    action="store",
    default=None,
    help="Overrides has_work_phone input feature with 0 or 1. Defaults to None (doesn't change the original value)",
)
argparser.add_argument(
    "-sleep",
    action="store",
    default=0,
    help="Num of seconds to increase the duration of the algorithm. Defaults to 0",
)

args = argparser.parse_args()
print(vars(args))

while True:
    segment = args.s
    algo_name = args.a
    version = args.v
    owns_home = args.home
    has_work_phone = args.phone
    sleep_seconds = args.sleep

    data_file = segment
    if segment != "all":
        data_file = f"{algo_name}-{segment}"
    input_ds = pd.read_csv(f"./data/{data_file}.csv")
    print(input_ds.shape)

    client = Algorithmia.client(
        "simqUvvKryCWCWgjihWcuGv7fro1", "https://api.therealreal.productionize.ai"
    )
    algo = client.algo(f"asli_algorithmia_trr/{algo_name}/{version}")

    records = input_ds.to_dict("records")
    for record in records:
        if owns_home is not None:
            record["owns_home"] = int(owns_home)
        if has_work_phone is not None:
            record["has_work_phone"] = int(has_work_phone)
        record["sleep"] = int(sleep_seconds)

        result = algo.pipe(record).result
        overridden_owns_home = record["owns_home"]
        overridden_has_work_phone = record["has_work_phone"]
        print(
            f"{result} from v{version} of {algo_name} sleeping for {sleep_seconds}s, overridden inputs: owns_home: {overridden_owns_home}, has_work_phone:{overridden_has_work_phone}"
        )
