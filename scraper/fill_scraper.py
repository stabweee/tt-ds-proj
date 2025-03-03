import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from bs4 import BeautifulSoup

from alive_progress import alive_bar


def getSrc(url):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless")

    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=options)

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    driver.get(url)
    src = driver.page_source
    driver.close()

    return src


def getFeatures(soup, list):
    features = []
    if list:
        for feature in soup.find_all("th", attrs={"class": "sortable"}):
            features.append(feature.text)
    else:
        for feature in soup.find_all("th")[1:]:
            features.append(feature.text)

    return features


def scrapePlayerInfo(databaseID):
    url = r"https://usatt.simplycompete.com/userAccount/trn/" + str(databaseID)
    src = getSrc(url)
    soup = BeautifulSoup(src, "html.parser")
    count = 0
    while not soup.find_all("tr") and count < 2:
        src = getSrc(url)
        soup = BeautifulSoup(src, "html.parser")
        count += 1
    if not soup.find_all("tr") and count == 2:
        return np.array([["", "", "", ""]])
    data = []

    for row in soup.find_all("tr")[1:]:
        record = []
        for feature in row.find_all("td", attrs={"class": "list-column"}):
            record.append(feature.text.replace("\n", "").strip())
        data.append(record)

    return np.array(data)


def scrapePlayerHistory(playerList):
    features = [
        "Rank",
        "First Name",
        "Last Name",
        "Database#",
        "USATT#",
        "Location",
        "Home Club",
        "Tournament Rating",
        "Last Played Tournament",
        "League Rating",
        "Last Played League",
        "Membership Expiration",
        "Tournament",
        "Date",
        "Initial Rating",
        "Final Rating",
    ]

    data = []
    with alive_bar(len(playerList), force_tty=True) as bar:
        playerList.apply(lambda x: addHistory(x, data, bar), axis=1)

    res = pd.DataFrame(data)
    res.columns = features
    res["Start Date"] = res["Date"].str.slice(stop=10)
    res["End Date"] = res["Date"].str.slice(start=12).str.strip()
    res = res.drop(columns=["Date"])

    res.to_csv("data/player-history-fill.csv", index=False)


def addHistory(row, data, bar):
    playerInfo = scrapePlayerInfo(row["Database#"])
    playerHistory = np.concatenate(
        (np.repeat([row], len(playerInfo), axis=0), playerInfo), axis=1
    )
    data.extend(playerHistory)
    bar()


import sys

sys.path.insert(0, "analysis\load_data")
from load import load_list, load_history

players = load_list()
history = load_history()
fill_players = players[
    (
        ~players["Database#"].isin(history["Database#"])
        & (players["Tournament Rating"] > 0)
    )
]

scrapePlayerHistory(fill_players)
