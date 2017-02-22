import sys
import os
import re
import datetime
from bs4 import BeautifulSoup
import requests
import settings
import broadcaster

YEARS = datetime.date.today().year
con = settings.CONNECTION
c = con.cursor()


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
        anime_id = int(years_num + season_num + str(i).zfill(3))
        try:
            title = contents[i].find("div", {"class": "mTitle"}).find("a").text
        except AttributeError:
            title = contents[i].find("div", {"class": "mTitle"}).find("h2").text
        try:
            about = contents[i].find("p", {"class": "leadText"}).text
        except:
            about = "_"
        try:
            actors = contents[i].find("dd").find_all("a")
            for j in actors:
                actor = j.text
                c.execute('select actor_id from actor where name = "{0}";'.format(actor))
                if len(c.fetchall()) == 0:
                    c.execute('insert into actor(name) values ("{0}");'.format(actor))
                c.execute('select actor_id from actor where name = "{0}";'.format(actor))
                actor_id = c.fetchall()[0][0]
                c.execute('insert into anime_actor values({0},{1});'.format(anime_id, actor_id))
        except:
            actor = "_"
        try:
            staff = contents[i].find("dd", {"class": "staff"}).text.replace('\n', '')
            # MEMO: 制作会社 は要素の最後にある前提
            brand = re.sub(r"^.*制作会社：(.*)$", r"\1", staff)
            if staff.count("原作："):
                # MEMO: 原作 は要素 0 番目にある前提
                writer = staff.split("、")[0].replace("原作：", "")
                if writer.count("("):
                    writer = re.sub(r"^(.*)\(.*$", r"\1", writer)
            else:
                writer = "_"
            if re.match("^監督", staff):
                director = re.sub(r"^監督(|・.*?)：(.*?)、.*$", r"\2", staff)
            elif staff.count("、監督"):
                director = re.sub(r"^.*、監督(|・.*?)：(.*?)、.*$", r"\2", staff)
            else:
                director = "_"
        except:
            staff = "_"
            brand = "_"
            writer = "_"
            director = "_"
        try:
            music = contents[i].find("dl", {"class": "music"}).find("dd").text.replace("\n", "").replace("\r", "")
            if music.count("【OP】") and music.count("【ED】"):
                op = re.sub(r"^【OP】(.*)【ED】(.*)$", r"\1", music)
                ed = re.sub(r"^【OP】(.*)【ED】(.*)$", r"\2", music)
                op_title = re.sub(r"^(.*)「(.*)」$", r"\2", op)
                op_singer = re.sub(r"^(.*)「(.*)」$", r"\1", op)
                ed_title = re.sub(r"^(.*)「(.*)」$", r"\2", ed)
                ed_singer = re.sub(r"^(.*)「(.*)」$", r"\1", ed)
            elif music.count("【OP】"):
                op = re.sub(r"^【OP】(.*)$", r"\1", music)
                ed = "_"
                op_title = re.sub(r"^(.*)「(.*)」$", r"\2", op)
                op_singer = re.sub(r"^(.*)「(.*)」$", r"\1", op)
            elif music.count("【ED】"):
                op = "_"
                ed = re.sub(r"^【ED】(.*)$", r"\1", music)
                ed_title = re.sub(r"^(.*)「(.*)」$", r"\2", ed)
                ed_singer = re.sub(r"^(.*)「(.*)」$", r"\1", ed)
            else:
                op = music
                ed = "_"
                op_title = re.sub(r"^(.*)「(.*)」$", r"\2", op)
                op_singer = re.sub(r"^(.*)「(.*)」$", r"\1", op)
            if not op == "_":
                c.execute('select singer_id from singer where name = "{0}";'.format(op_singer))
                if len(c.fetchall()) == 0:
                    c.execute('insert into singer(name) values ("{0}");'.format(op_singer))
                c.execute('select singer_id from singer where name = "{0}";'.format(op_singer))
                singer_id = c.fetchall()[0][0]
                c.execute('select singer_id from openingsong where op = "{0}";'.format(op_title))
                if len(c.fetchall()) == 0:
                    c.execute('insert into openingsong values ("{0}", {1});'.format(op_title, singer_id))
            if not ed == "_":
                c.execute('select singer_id from singer where name = "{0}";'.format(ed_singer))
                if len(c.fetchall()) == 0:
                    c.execute('insert into singer(name) values ("{0}");'.format(ed_singer))
                c.execute('select singer_id from singer where name = "{0}";'.format(ed_singer))
                singer_id = c.fetchall()[0][0]
                c.execute('select singer_id from endingsong where ed = "{0}";'.format(ed_title))
                if len(c.fetchall()) == 0:
                    c.execute('insert into endingsong values ("{0}", {1});'.format(ed_title, singer_id))
        except:
            music = "_"
        onairs = contents[i].find("div", {"class": "schedule"}).find("table").find_all("td")
        onairs_times = onairs_time_check(onairs)
        for j in onairs_times:
            onair_time = j
            onair_time_list = onair_time.split(",")
            print(j)
            c.execute('select anime_id from broadcast_time where anime_id = {0};'.format(anime_id))
            if len(c.fetchall()) == 0:
                c.execute('select broadcaster_id from broadcaster where name = "{0}";'.format(onair_time_list[0]))
                broadcaster_id = c.fetchall()[0][0]
                c.execute('insert into broadcast_time values ({0}, {1}, "{2}", "{3}");'.format(anime_id, broadcaster_id, onair_time_list[1], onair_time_list[2]))
        try:
            official_site = contents[i].find("a", {"class": "officialSite"})['href']
        except:
            official_site = "_"
        try:
            official_twitter = contents[i].find("a", {"class": "officialTwitter"})['href']
        except:
            official_twitter = "_"
        c.execute('select * from anime where anime_id = {0};'.format(anime_id))
        if len(c.fetchall()) == 0:
            c.execute('insert into anime values ({0},"{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}");'.format(anime_id, escaping(title), escaping(about), escaping(brand), escaping(writer), escaping(director), escaping(op_title), escaping(ed_title), escaping(official_site), escaping(official_twitter)))

    con.commit()
    c.close()
    con.close()
    sys.exit(0)


def onairs_time_check(onairs):
    onairs_times = []
    for i in range(len(onairs)):
        station_html = onairs[i].find("span", {"class": "station"})
        if station_html is not None:
            for j in broadcaster.broadcaster_list:
                if station_html.text == j:
                    onair_time_first = onairs[i].find_all("span")[1].text
                    onair_time_weekly = re.sub(r"^.*\(([月|火|水|木|金|土|日])\)(.*)$", r"\1,\2", onair_time_first)
                    if onair_time_weekly.count("レギュラー放送"):
                        onair_time_weekly = re.sub(r"^([月|火|水|木|金|土|日]).*レギュラー放送時間(.*)\)$", r"\1,\2", onair_time_weekly)
                    if onair_time_weekly.count("※"):
                        onair_time_weekly = re.sub(r"^(.*)　.*$", r"\1", onair_time_weekly)
                    onairs_times.append(station_html.text + "," + onair_time_weekly)
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


def escaping(name):
    escape_list = ['"', '\'']
    for i in escape_list:
        name = name.replace(i, " ")
    return name


if __name__ == "__main__":
    main()
