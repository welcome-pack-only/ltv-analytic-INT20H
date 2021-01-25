import pandas as pd
import os

from src.utils import get_config
from src.ltv import LTV


if __name__ == "__main__":
    CONFIG = get_config("config.yaml")

    df = pd.read_csv(
        os.path.join(CONFIG["path_to_data_folder"], CONFIG["data_filename"])
    )

    ltv = LTV(
        df=df,
        subscription_price=CONFIG["subscription_price"],
        commission_percentage=CONFIG["commission_percentage"],
        subscriber_id_column=CONFIG["subscriber_id_column"],
        event_dt_column=CONFIG["event_dt_column"],
        subscription_offer_type_column=CONFIG[
            "subscription_offer_type_column"
        ],
    )
    print("LTV:", ltv.get_ltv())
