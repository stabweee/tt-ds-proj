import pandas as pd
from datetime import date

players = pd.read_csv("./data/player-list.csv")
td = pd.read_csv("./data/td-ratings.csv")
history = pd.read_csv("./data/player-history.csv")

td.rename({"Member ID": "USATT#"}, axis=1, inplace=True)
td = td[["USATT#", "State", "Zip", "Gender", "Date of Birth", "Expiration Date"]]
players = players.merge(td)


def max_rating(player):
    r_hist = history[history["USATT#"] == player["USATT#"]]
    return r_hist["Final Rating"].max()


history["Final Rating"] = pd.to_numeric(history["Final Rating"], errors="coerce")
players["Max Rating"] = players.apply(max_rating, axis=1)

players["Date of Birth"] = pd.to_datetime(players["Date of Birth"], errors="coerce")
tdy = date.today()
players["Age"] = pd.to_timedelta(pd.to_datetime(tdy) - players["Date of Birth"])  # type: ignore

players.to_csv("./data/player-stats.csv", index=False)
