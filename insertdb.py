import sys
import os
import re
import datetime
from bs4 import BeautifulSoup
import requests
import settings
import broadcaster

YEARS = datetime.date.today().year


def main():
    argvs = sys.argv
    if len(argvs) != 2:
        sys.stderr.write('Error: Usage: python {0} [spring|summer|autumn|winter]\n'.format(argvs[0]))
        sys.exit(1)
    if argvs[1] == "spring":
        url = "https://akiba-souken.com/anime/spring/"
    elif argvs[1] == "summer":
        url = "https://akiba-souken.com/anime/summer/"
    elif argvs[1] == "autumn":
        url = "https://akiba-souken.com/anime/autumn/"
    elif argvs[1] == "winter":
        url = "https://akiba-souken.com/anime/winter/"
    else:
        sys.stderr.write('Error: Usage: python {0} [spring|summer|autumn|winter]\n'.format(argvs[0]))
        sys.exit(1)
    scrape_and_insert_db(url, argvs[1])


def scrape_and_insert_db(url, season):
    years_num = str("{0:02d}".format(YEARS % 100))
    season_num = season_to_i(season)
    response = requests.get(url)
    if response.status_code == 404:
        sys.stderr.write('NotFound.')
        sys.exit(1)
    html = response.text.encode(response.encoding, "ignore")
    soup = BeautifulSoup(html, "lxml")
    contents = soup.find_all("div", {"class": "itemBox"})
    for i in range(len(contents)):
        # アニメid、 タイトル、あらすじ、会社id、会社名、声優id、声優名、原作者id、原作者名、監督id、監督名、オープニングid、エンディングid、歌手id、歌手名、公式サイトurl、公式ツイッターurl を取ってくる。
        # TODO: id をどう定義するか
        anime_id = int(years_num + season_num + str(i).zfill(3))
        try:
            title = contents[i].find("div", {"class": "mTitle"}).find("a").text
        except AttributeError:
            title = contents[i].find("div", {"class": "mTitle"}).find("h2").text
        about = contents[i].find("p", {"class": "leadText"}).text
        onairs = contents[i].find("div", {"class": "schedule"}).find("table").find_all("td")
        onairs_times = onairs_time_check(onairs)
        try:
            official_site = contents[i].find("a", {"class": "officialSite"})['href']
        except AttributeError:
            official_site = "_"
        try:
            official_twitter= contents[i].find("a", {"class": "officialTwitter"})['href']
        except AttributeError:
            official_twitter= "_"



def onairs_time_check(onairs):
    onairs_times = []
    for i in range(len(onairs)):
        station_html = onairs[i].find("span", {"class": "station"})
        if station_html is not None:
            for j in broadcaster.broadcaster_list:
                if station_html.text == j:
                    onair_time_first = onairs[i].find_all("span")[1].text
                    onair_time_weekly = re.sub(r"^.*\(([月|火|水|木|金|土|日])\)(.*)$", r"\1曜 \2", onair_time_first)
                    onairs_times.append(station_html.text + ": " + onair_time_weekly)
                    break
    return onairs_times


def season_to_i(season):
    if season == "spring":
        return "1"
    elif season == "summer":
        return "2"
    elif season == "autumn":
        return "3"
    elif season == "winter":
        return "4"
    return "0"


if __name__ == "__main__":
    main()
