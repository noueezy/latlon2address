# LatLon2Section

緯度経度から、（最も近い）都道府県名・市区町村名・大字町丁目名を取得

## Description
- Python実装
- Sqlite3によるDB構築
- [国土交通省位置参照情報ダウンロードサービス](http://nlftp.mlit.go.jp/cgi-bin/isj/dls/_choose_method.cgi)から、位置参照情報データを自動ダウンロード
    - Selenium+ChromeDriverによるブラウザGUI自動操作

## How to use

### 前準備

- Seleniumをインストール

        $ pip install selenium

- ChromeDriverをダウンロードして、任意のフォルダに配置

- CreateAddressLatLonDB.shの変数chromeDriverPathに、ChromeDriverのパスを記述（XXXXの部分を書き換え）
    

### DB構築

    $ bash CreateAddressLatLonDB.sh

- 位置参照情報データファイル自動ダウンロード
- zipファイル自動展開
- SQLiteデータベースファイル構築

### 都道府県名・市区町村名・大字町丁目名を取得

例：東京駅前

    $ python NearestSection.py 35.680178 139.769491
    address: 東京都 千代田区 丸の内一丁目
    distance(km): 0.25767395168844676
