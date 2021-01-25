import pandas as pd
import numpy as np


class LTV(object):
    """
    LTV = [1] + [2] + [3] + [4] + [5]

    [1] = DEV_PROCEEDS * Conversation from trial
    [2] = [1] * 1th purchase to 2nd = DEV_PROCEEDS * Conversation from trial * 1th purchase to 2nd
    ...
    [5] = [4] * 4th to 5th = DEV_PROCEEDS * Conversation from trial * ... * 4th to 5th

    k1 := Conversation from trial
    k2 := 1th purchase to 2nd
    ...
    k5 := 4th purchase to 3rd

    LTV = DEV_PROCEEDS * (k1 + k1*k2 + ... + k1*k2*k3*k4*k5)
    kn - measured as a percentage
    """

    def __init__(
        self,
        df: pd.DataFrame,
        subscription_price: float = 9.99,
        commission_percentage: float = 0.3,
        subscriber_id_column: str = "Subscriber ID",
        event_dt_column: str = "Event Date",
        subscription_offer_type_column: str = "Subscription Offer Type",
        inplace: bool = False,
    ):
        assert subscriber_id_column in df.columns
        assert event_dt_column in df.columns
        assert subscription_offer_type_column in df.columns

        self.DEV_PROCEEDS = subscription_price * (1 - commission_percentage)

        assert self.DEV_PROCEEDS > 0

        self.subscriber_id_column = subscriber_id_column
        self.event_dt_column = event_dt_column
        self.subscription_offer_type_column = subscription_offer_type_column

        self.df = df if inplace else df.copy()
        self.ltv = None

    def get_max_purchase(self) -> np.int64:
        """
        :return: max purchase number was made by 1 subscriber
        """
        t = self.df[
            self.df[self.subscription_offer_type_column] != "Free Trial"
        ]
        t = t.groupby(self.subscriber_id_column)
        return t[self.event_dt_column].count().max()

    def get_subscribers_transaction(self, s_id: np.int64) -> np.ndarray:
        """
        :param s_id: subscriber id
        this function find array of transaction of each
        subscriber like: [1, 1, 1, 0, 0, 0]
        it means that subscriber was on free trial,
        and made 2 purchase
        :param df: DataFrame with our dataset
        :param max_purchase_num: max purchase number was made by 1 subscriber
        :return: np.array
        """

        info = self.df[self.df[self.subscriber_id_column] == s_id]

        purchase = info[info[self.subscription_offer_type_column].isna()]

        # number of purchase made by this subscriber
        purchase_num = purchase.shape[0]
        max_purchase_num = self.get_max_purchase()

        transaction = np.zeros(max_purchase_num + 1)

        # as every had free trial, put 1 on the first place
        transaction[0] = 1
        for i in range(1, purchase_num + 1):
            transaction[i] = 1
        return transaction

    def get_ltv(self) -> np.float64:
        """
        :return: ltv
        """
        subscribers = self.df[[self.subscriber_id_column]].drop_duplicates()
        subscribers["transaction"] = subscribers[
            self.subscriber_id_column
        ].apply(lambda x: self.get_subscribers_transaction(x))

        max_purchase_num = self.get_max_purchase()

        all_transaction = subscribers["transaction"].sum()
        percent_of_conversation = (
            all_transaction[1:] / all_transaction[:max_purchase_num]
        )

        # list of k1, k2, ..., k5
        K = []
        for i in range(max_purchase_num):
            k = percent_of_conversation[: i + 1].prod()
            K.append(k)

        self.ltv = sum(K) * self.DEV_PROCEEDS

        return self.ltv
