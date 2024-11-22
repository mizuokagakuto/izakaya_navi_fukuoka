import pandas as pd


def calculate_weightedsum(weights, max_money=None, place=None, count=None):

    # 固定されたスコア列
    score_columns = [
        "star_score_re",
        "posi_nega_score_re",
        "satisfy_score_re",
        "insta_score_re",
        "calm_score_re",
        "service_score_re",
    ]

    # CSVファイルを読み込む
    df = pd.read_csv("./static/data/review_data.csv")

    # スコア列がデータフレームに存在しているか確認
    missing_columns = [col for col in score_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"以下の列がCSVファイルに存在しません: {missing_columns}")

    # 重みを文字列から浮動小数点数に変換
    try:
        float_weights = {col: float(weights[col]) for col in score_columns}
    except ValueError as e:
        raise ValueError(f"重みをfloatに変換できません: {e}")

    # 各列に重みを掛ける
    weighted_scores = df[score_columns].mul(
        [float_weights[col] for col in score_columns], axis=1
    )

    # 行ごとの和を計算
    df["weighted_sum"] = weighted_scores.sum(axis=1, skipna=True)

    # moneyでフィルター
    if max_money and max_money != "all":
        df = df[(df["max_money"] <= float(max_money)) & (df["max_money"] > float(max_money)-1000)]

    # placeでフィルター
    if place and place != "all":
        df = df[df["place"] == place]

    # データがフィルターで空になった場合の処理
    if df.empty:
        return False

    # 結果を降順に並び替え
    sorted_df = df.sort_values(by="weighted_sum", ascending=False)

    # 上位のstore_name, picture_url, link_urlを取得
    store_name = []
    picture_url = []
    link_url = []
    range_money = []
    place_list = []
    if sorted_df["weighted_sum"].count() - count < 10:
        for i in range(0+count,sorted_df["weighted_sum"].count()):
            pickup_row = sorted_df.iloc[i]
            store_name.append(pickup_row["store_name"])
            picture_url.append(pickup_row["picture_url"])
            link_url.append(pickup_row["link_url"])
            range_money.append(pickup_row["range_money"])
            place_list.append(pickup_row["place"])
    else:      
        for i in range(0+count,10+count):
            pickup_row = sorted_df.iloc[i]
            store_name.append(pickup_row["store_name"])
            picture_url.append(pickup_row["picture_url"])
            link_url.append(pickup_row["link_url"])
            range_money.append(pickup_row["range_money"])
            place_list.append(pickup_row["place"])

    result = {
        "store_name": store_name,
        "picture_url": picture_url,
        "link_url": link_url,
        "pickup_count": count,
        "len" : sorted_df["weighted_sum"].count(),
        "range_money": range_money,
        "place_list":place_list
    }

    return result


# --------------------------------------#
