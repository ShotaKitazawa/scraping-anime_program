**Do not maintain any more**

# About

https://akiba-souken.com/anime/[spring|summer|autumn|winter]/ からスクレイピングします。

# Environment

- macOS 10.12.3
- Python 3.5.2
	- beautifulsoup4 (4.5.3)
	- requests (2.13.0)
	- tweepy (3.5.0)
	- mysqlclient (1.3.10)
- MariaDB 10.1.21

# Stracture

- anime_db.sql: MariaDBセットアップ用のsql文です。
- broadcaster.py: 対象放送局を設定します。
- settings.py: Twitterアクセストークン、MariaDB接続情報 を格納します。
- insertdb.py: MariaDB に情報をinsertします。
- tweet.py: 引数の季節に放送する番組についてツイートを行います。

# Problem

- [しょぼいカレンダー](http://cal.syoboi.jp/) との差別化

# TODO

- 完: 放送時間を表示 > 放送局を指定できるようにする

- 放送時間のフォーマットの改善
	- AT-X2017年1月3日(火)23:30～
		- AT-X: 火曜 23:30～
	- TBS2017年1月6日(金)26:10～、1月13日(金)26:10～、1月20日(金)26:40～(※レギュラー放送時間25:55～)
		- TBS: 金曜 26:40～(※レギュラー放送時間25:55～)
		- 直す

- 完: title にファイル名使用不可文字が入ったときにエスケープする処理
	- Fate/Grand Order > Fate Grand Order

- 完: tweet フォーマットの改善
	- 現在: アイドル事変\nTOKYO MX2017年1月8日(日)23:30～
	- 未来: アイドル事変\nTOKYO MX: 日曜23:30~

- 完: ~/.images/ 以下に jpg ファイルを保存

- 完: 既に jpg がある場合は、ダウンロードしない

- 完: スタッフ・制作会社をスクレイピング

- 番組表を元に色々やる
	- しょぼいカレンダーからとってくる？
	- 放送1時間前にツイート
		- 第何話か・あらすじ等も
	- 対象アニメが最終回を迎えたら、監視対象から外す。
	- 対象放送局
		- [NHK Eテレ](http://www2.nhk.or.jp/hensei/program/wk.cgi?area=001&type=0&date=(日付)&tz=&ch=31&mode=2&f=week)
		- [日テレ](http://www.ntv.co.jp/program/)
		- [テレビ朝日](http://www.tv-asahi.co.jp/bangumi/)
		- [TBS](http://www.tbs.co.jp/tv/)
		- [テレビ東京](http://www.tv-tokyo.co.jp/index/timetable/)
		- [フジテレビ](http://www.fujitv.co.jp/timetable/weekly/)
		- [TOKYO MX](http://s.mxtv.jp/bangumi_pc/)
		- [AT-X](http://www.at-x.com/program)

- tweet.py における onairs_time_check 関数の最適化

- データベースで管理: MariaDB
	- 完: データベースに "ID, タイトル, 放送時間, 更新時間" を書き込む
		- 制作会社とか声優と書ければなおよい
	- 完: insertdb.py の実装
		- 実行することで、データベースにデータをインサートする。
	- インデックスを張る等の最適化処理

- HTML 出力: Django
	- 独自フォーマットで作り直す
	- カレンダー形式とかいいかも
		- [しょぼいカレンダー](http://cal.syoboi.jp/)

- アプリ化
	- 自Webサーバに情報を公開 (丸コピ?) して、そっから取ってくる仕組みとか？
	- google カレンダーと連携して、カレンダーに放送時間を書込

- ユーザ登録を実装
	- ID, PW のみの管理(が楽？) or Google アカウント
	- 見たい番組をハイライトする機能
	- 過去のハイライト状況からおすすめ番組の割り出し

# MEMO

- settings.py は別売り
	- 中身は以下

```python:settings.py
CONSUMER_KEY = hoge
CONSUMER_SECRET = hoge
ACCESS_TOKEN = hoge
ACCESS_TOKEN_SECRET = hoge

import MySQLdb
CONNECTION = MySQLdb.connect(
    user = hoge,
    passwd = hoge,
    host = hoge,
    db = hoge,
)
```

- broadcaster.py には、検索したい放送局名をリストに入れる。

- anime_db.sql の使い方

```bash
$ mysql -p -u (DBユーザ名) (DB名) < anime_db.sql
```
