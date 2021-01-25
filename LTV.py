import pandas as pd
import numpy as np

DEV_PROCEEDS = 9.99 * 0.7

df = pd.read_csv("data_analytics.csv")


def get_max_purchase(df):
    df = df[df["Subscription Offer Type"] != "Free Trial"]
    df = df.groupby("Subscriber ID")["Event Date"].count()
    MAX = df.max()
    return MAX


def get_subscribers_transaction(s_id, df):
    info = df[df["Subscriber ID"] == s_id]

    purchase = info[info["Subscription Offer Type"].isna()]
    purchase_num = purchase.shape[0]

    num = get_max_purchase(df)
    transaction = np.zeros(num)
    for i in range(purchase_num):
        transaction[i] = 1
    return transaction


def ltv(df, print_info=True):
    subscribers = df[["Subscriber ID"]].drop_duplicates().values.flatten()

    all_transaction = []
    for subscriber in subscribers:
        transaction = get_subscribers_transaction(subscriber, df)
        all_transaction.append(transaction)

    all_transaction = sum(all_transaction)
    LTV = sum(all_transaction) * DEV_PROCEEDS / subscribers.shape[0]

    if print_info:
        num = get_max_purchase(df)
        for i in range(num):
            if i == 0:
                print("Conversation from trial: ", all_transaction[i])
            else:
                print(f"{i}th purchase to {i+1}th: ", all_transaction[i])

        print()

        print("LTV =", LTV)
    return LTV


ltv(df)
