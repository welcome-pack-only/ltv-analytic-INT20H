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
import pandas as pd
import numpy as np


DEV_PROCEEDS = 9.99 * 0.7

df = pd.read_csv("data_analytics.csv")


def get_max_purchase():
    """
    :return: max purchase number was made by 1 subscriber
    """
    s = df.groupby("Subscriber ID")
    s = s["Event Date"].count()
    num = s.max() - 1
    return num


def get_subscribers_transaction(s_id):
    """
    :param s_id: subscriber id
    this function find array of transaction of each
    subscriber like: [1, 1, 1, 0, 0, 0]
    it means that subscriber was on free trial,
    and maid 2 purchase
    :return: np.array
    """
    info = df[df["Subscriber ID"] == s_id]

    purchase = info[info["Subscription Offer Type"].isna()]
    purchase_num = purchase.shape[
        0
    ]  # number of purchase made by this subscriber

    num = get_max_purchase()
    transaction = np.zeros(num + 1)
    transaction[0] = 1  # as every had free trial, put 1 on the first place
    for i in range(1, purchase_num + 1):
        transaction[i] = 1
    return transaction


subscribers = df[["Subscriber ID"]].drop_duplicates()
subscribers["transaction"] = subscribers["Subscriber ID"].apply(
    get_subscribers_transaction
)

all_transaction = subscribers["transaction"].sum()
percent_of_conversation = (
    all_transaction[1:] / all_transaction[: get_max_purchase()]
)

K = []  # list of k1, k2, ..., k5
for i in range(get_max_purchase()):
    k = percent_of_conversation[: i + 1].prod()
    K.append(k)

LTV = sum(K) * DEV_PROCEEDS
print("LTV: ", LTV)
