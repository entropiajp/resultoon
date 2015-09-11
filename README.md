resultoon(リザルトゥーン)
=========================

Splatoon(スプラトゥーン)プレイ時に常駐してHDMIキャプチャボードの画像を監視し、ガチマッチのリザルトを自動収集するシステム。

## 何ができるのか
- ガチマッチのリザルトをGoogle Spreadsheet上に送信
- 画面キャプチャ

## 取得可能なリザルト
- ガチマッチのルール
- ステージ名
- 試合前の自分のウデマエ(S+ 〜 C-)
- ウデマエポイント増減
- 試合後の自分のウデマエポイント
- 8人のプレイヤーのウデマエ、kill/death

## demo


## 準備
### インストール
resultoonの実行には以下の言語実行環境、ライブラリがすべて必要です。

- Python 2.7.10
    - requests 2.7.0
- OpenCV 3.0
- Tesseract 3.02.02
    - python-tesseract 0.9-0.4

#### Pythonインストール
[Download Python | Python.org](https://www.python.org/downloads/)

Download Python 2.7.10のボタンからインストーラをダウンロードします。  
あとはインストーラの指示通りにインストールしてください。

##### requestsインストール
コマンドプロンプトで `pip install requests` を実行するとインストールできます。

#### OpenCVインストール
[DOWNLOADS | OpenCV](http://opencv.org/downloads.html)

Version 3.0のOpenCV For Windowsのリンクからインストーラをダウンロードします。  
あとはインストーラの指示通りにインストールしてください。

#### Tesseractインストール
[https://code.google.com/p/tesseract-ocr/downloads/detail?name=tesseract-ocr-setup-3.02.02.exe](https://code.google.com/p/tesseract-ocr/downloads/detail?name=tesseract-ocr-setup-3.02.02.exe)

##### python-tesseractインストール
[3togo / python-tesseract / ダウンロード — Bitbucket](https://bitbucket.org/3togo/python-tesseract/downloads)

`python-tesseract-0.9-0.4.win32-py2.7.exe` をダウンロードします。
あとはインストーラの指示通りにインストールしてください。

### 初期設定
`resultoon.ini` ファイルにて以下の設定を行うことができます。

|          項目          |                     意味                    | 初期値 |
|------------------------|---------------------------------------------|----|
| SAVE_IMAGE_PATH        | キャプチャした画像の保存先フォルダ          | `./`   |
| GOOGLE_APPS_SCRIPT_URL | Google Spreadsheetに送信する場合の送信先URL |  ` `  |
| CAPTURE_DEVICE_ID      | HDMIキャプチャボードのデバイスID            |  `0`  |


## 利用方法
### 起動
`resultoon.py` をダブルクリックしてください。
(コマンドプロンプトで `python resultoon.py` でも起動できます)  

しばらくするとゲーム画面が表示されたウィンドウが立ち上がります。  
あとは普通にガチバトルをプレイするだけで、リザルトを勝手に収集します。  
また、任意のタイミングで `スペースキー` を押すことで画面キャプチャを取得することができます。


### 終了
`Esc` キーを押してください。　※ウィンドウを閉じても終了しません。

### 注意
- PC上のウィンドウにもゲーム画面が表示されますが、**fpsは一定ではありません**。PCの処理内容によってはプレイに支障をきたすレベルでfpsが低下するおそれがあります。そのため、分配器を使った別モニタへの表示を強く推奨します。
- AmarecTV等で同じキャプチャボードの画像を同時に取得することはできません(本アプリがデバイスを占有するため)

### Google Spreadsheetの設定
Google Spreadsheet上にリザルトを記録するためには、以下の設定作業が必要です。

#### Google SpreadSheet上での作業
- [https://docs.google.com/spreadsheets](https://docs.google.com/spreadsheets) を開きます
- スプレッドシートを新規作成します
     - このスプレッドシートのURL `https://docs.google.com/spreadsheets/d/xxxxxxxxxxxx/edit` をメモしておきます
- `master` という名前のシートを新規作成します
- `ツール > スクリプトエディタ` をクリックします
- `空のプロジェクト` をクリックします
- エディタの内容を `main.gs` の内容で上書きします
     - main.gsの1行目 `SPREADSHEET_ID` の文字列を先ほどメモしたspreadsheetのURLのうち `xxxxxxxxxxxx` に該当する文字列に置き換えます
- `公開 > ウェブアプリケーションとして導入` をクリックします
    - 「現在のウェブアプリケーションのURL」をメモしておきます
- プロジェクト名には `resultoon` と入力します
- `次のユーザーとしてアプリケーションを実行: 自分`、`アプリケーションにアクセスできるユーザー: 全員(匿名ユーザーを含む)` を選択して `更新` をクリックします

#### PC上での作業
- 先ほどメモしておいた「現在のウェブアプリケーションのURL」をコピーして、 `resultoon.ini`の`GOOGLE_APPS_SCRIPT_URL`の=の右側にペーストします

設定完了後、resultoonを起動すると `master` シートにリザルトが自動的に記録されていきます。

#### Google Spreadsheetに送信されるデータの例
データ形式はjsonです。

```
{
    udemae_point: 19,
    udemae_diff: "+3",
    members: [
        {
            team: "win",
            udemae: "A+",
            kill: 6,
            death: 3
        },
        {
            team: "win",
            udemae: "S",
            kill: 3,
            death: 1
        },
        {
            team: "win",
            udemae: "S+",
            kill: 2,
            death: 1,
            isPlayer: true
        },
        {
            team: "win",
            udemae: "A",
            kill: 1,
            death: 0
        },
        {
            team: "lose",
            udemae: "A+",
            kill: 2,
            death: 3
        },
        {
            team: "lose",
            udemae: "A",
            kill: 1,
            death: 3
        },
        {
            team: "lose",
            udemae: "A",
            kill: 0,
            death: 2
        },
        {
            team: "lose",
            udemae: "S",
            kill: 0,
            death: 4
        }
    ],
    rule: "ガチヤグラ",
    stage: "シオノメ油田"
}
```

## TODO
- リザルトをCSV形式で保存する機能の追加
- エラー例外処理

## License
MIT

## Author
Copyright(c) 2015- Kenichi Koyama
