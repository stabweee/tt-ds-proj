import pandas as pd


def load_list():
    players = pd.read_csv(
        r"C:\Users\hsu_s\Projects\Personal\tt-ds-proj\data\player-list.csv"
    )
    players[["Rank", "USATT#", "Database#", "Tournament Rating", "League Rating"]] = (
        players[
            ["Rank", "USATT#", "Database#", "Tournament Rating", "League Rating"]
        ].apply(pd.to_numeric)
    )
    players[["Last Played Tournament", "Last Played League"]] = players[
        ["Last Played Tournament", "Last Played League"]
    ].apply(pd.to_datetime)

    return players


def load_history():
    history = pd.read_csv(
        r"C:\Users\hsu_s\Projects\Personal\tt-ds-proj\data\player-history.csv"
    )
    history[
        [
            "Rank",
            "USATT#",
            "Database#",
            "Tournament Rating",
            "League Rating",
            "Initial Rating",
            "Final Rating",
        ]
    ] = history[
        [
            "Rank",
            "USATT#",
            "Database#",
            "Tournament Rating",
            "League Rating",
            "Initial Rating",
            "Final Rating",
        ]
    ].apply(
        pd.to_numeric, errors="coerce"
    )
    history[["Last Played Tournament", "Last Played League"]] = history[
        ["Last Played Tournament", "Last Played League"]
    ].apply(pd.to_datetime)
    history["Start Date"] = (
        pd.to_datetime(history["Start Date"], format="%Y-%m-%d", errors="coerce")
        .fillna(
            pd.to_datetime(history["Start Date"], format="%m-%d-%Y", errors="coerce")
        )
        .fillna(
            pd.to_datetime(history["Start Date"], format="%m/%d/%Y", errors="coerce")
        )
    )
    history["End Date"] = (
        pd.to_datetime(history["End Date"], format="%Y-%m-%d", errors="coerce")
        .fillna(pd.to_datetime(history["End Date"], format="%m-%d-%Y", errors="coerce"))
        .fillna(pd.to_datetime(history["End Date"], format="%m/%d/%Y", errors="coerce"))
    )

    return history


def load_stats():
    stats = pd.read_csv(
        r"C:\Users\hsu_s\Projects\Personal\tt-ds-proj\data\player-stats.csv"
    )
    stats[
        [
            "Rank",
            "USATT#",
            "Database#",
            "Tournament Rating",
            "League Rating",
            "Max Rating",
            "Tournaments Played",
        ]
    ] = stats[
        [
            "Rank",
            "USATT#",
            "Database#",
            "Tournament Rating",
            "League Rating",
            "Max Rating",
            "Tournaments Played",
        ]
    ].apply(
        pd.to_numeric, errors="coerce"
    )
    stats[["Last Played Tournament", "Last Played League", "Date of Birth"]] = stats[
        ["Last Played Tournament", "Last Played League", "Date of Birth"]
    ].apply(pd.to_datetime)
    stats[["Age"]] = stats[["Age"]].apply(pd.to_timedelta)

    return stats


def load_td():
    td = pd.read_csv(r"C:\Users\hsu_s\Projects\Personal\tt-ds-proj\data\td-ratings.csv")
    td[["Member ID", "Rating"]] = td[["Member ID", "Rating"]].apply(pd.to_numeric)

    return td
