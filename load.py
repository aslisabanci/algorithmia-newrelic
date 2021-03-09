import Algorithmia
import pandas as pd
import sys

if __name__ == "__main__":
    while True:
        to_load = "all"
        version = "0.1.1"
        args = sys.argv[1:]
        if len(args):
            to_load = args[0]
            version = args[1]

        input_ds = pd.read_csv(f"./data/{to_load}.csv")
        print(input_ds.shape)

        client = Algorithmia.client(
            "simqUvvKryCWCWgjihWcuGv7fro1", "https://api.therealreal.productionize.ai"
        )
        algo = client.algo(f"asli_algorithmia_trr/credit_card_approval/{version}")

        records = input_ds.to_dict("records")
        for record in records:
            result = algo.pipe(record).result
            print(f"{result} from v{version}")
