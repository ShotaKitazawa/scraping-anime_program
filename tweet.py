import sys
import os
import re
import datetime
from bs4 import BeautifulSoup
import requests
import tweepy
import settings
import broadcaster

YEARS = datetime.date.today().year

auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


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
    scrape_and_tweet(url, argvs[1])


def scrape_and_tweet(url, season):
    response = requests.get(url)
    if response.status_code == 404:
        sys.stderr.write('NotFound.')
        sys.exit(1)
    mkdir(season)
    html = response.text.encode(response.encoding, "ignore")
    soup = BeautifulSoup(html, "lxml")
    contents = soup.find_all("div", {"class": "itemBox"})
    for i in range(len(contents)):
        try:
            title = contents[i].find("div", {"class": "mTitle"}).find("a").text
        except AttributeError:
            title = contents[i].find("div", {"class": "mTitle"}).find("h2").text
        title_escaped = escaping(title)
        image_url = contents[i].find("div", {"class": "itemImg"}).find("img")['src']
        onairs = contents[i].find("div", {"class": "schedule"}).find("table").find_all("td")
        onairs_time = onairs_time_check(onairs)

        if image_exist(title_escaped, season):
            sys.stdout.write("{0} image have already existed.\n".format(title))
        else:
            download_image(image_url, title_escaped, season)

        tweet = str(YEARS) + "年" + japanese(season) + "\n\n" + title + "\n\n"
        if len(onairs_time) == 0:
            tweet += "Not OnAir"
        else:
            for i in onairs_time:
                tweet += i
                tweet += "\n"
        api.update_with_media(filename="{0}/.images/{1}-{2}/{3}.jpg".format(os.path.expanduser('~'), YEARS, season, title_escaped), status=tweet)
        sys.stdout.write("{0} tweet.\n".format(title))


def mkdir(season):
    if not (os.path.exists("{0}/.images".format(os.path.expanduser('~')))):
        os.mkdir("{0}/.images".format(os.path.expanduser('~')))
    if not (os.path.exists("{0}/.images/{1}-{2}".format(os.path.expanduser('~'), YEARS, season))):
        os.mkdir("{0}/.images/{1}-{2}".format(os.path.expanduser('~'), YEARS, season))


def escaping(title):
    escape_list = ['\\', '/', ':', '*', '?', '"', '>', '<', '|']
    for i in escape_list:
        title = title.replace(i, " ")
    return title


def onairs_time_check(onairs):
    onairs_time = []
    for i in range(len(onairs)):
        station_html = onairs[i].find("span", {"class": "station"})
        if station_html is not None:
            for j in broadcaster.broadcaster_list:
                if station_html.text == j:
                    onair_time_first = onairs[i].find_all("span")[1].text
                    onair_time_weekly = re.sub(r"^.*\(([月|火|水|木|金|土|日])\)(.*)$", r"\1曜 \2", onair_time_first)
                    onairs_time.append(station_html.text + ": " + onair_time_weekly)
                    break
    return onairs_time


def image_exist(title, season):
    if (os.path.exists("{0}/.images/{1}-{2}/{3}.jpg".format(os.path.expanduser('~'), YEARS, season, title))):
        return True
    else:
        return False


def download_image(url, title, season):
    response = requests.get(url)
    with open("{0}/.images/{1}-{2}/{3}.jpg".format(os.path.expanduser('~'), YEARS, season, title), 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)


def japanese(season):
    if season == "spring":
        return "春"
    elif season == "summer":
        return "夏"
    elif season == "autumn":
        return "秋"
    elif season == "winter":
        return "冬"
    return "N/A"


if __name__ == "__main__":
    main()
