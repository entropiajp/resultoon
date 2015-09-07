resultoon(リザルトゥーン)
=========================

Splatoon(スプラトゥーン)プレイ時に常駐してHDMIキャプチャボードの画像を監視し、ガチマッチのリザルトを自動収集するシステム。

## 何ができるのか
- ガチマッチのリザルトをCSV形式で保存
- ガチマッチのリザルトをGoogle Spreadsheet上に送信(上級者向け)
- 画面キャプチャ

## 取得可能なリザルト
- 試合前の自分のウデマエ(S+ 〜 C-)
- ウデマエポイント増減
- 試合後の自分のウデマエポイント
- 8人のプレイヤーのウデマエ、kill/death

## 準備
### インストール
resultoonの実行には以下の言語実行環境、ライブラリがすべて必要です。

- Python 2.7.10
    - requests 2.7.0
- OpenCV 3.0
- Tesseract 3.02.02

#### Pythonインストール
[Download Python | Python.org](https://www.python.org/downloads/)

Download Python 2.7.10のボタンからインストーラをダウンロードします。  
あとはインストーラの指示通りにインストールしてください。

`pip install requests` を実行してください。

#### OpenCVインストール
[DOWNLOADS | OpenCV](http://opencv.org/downloads.html)

Version 3.0のOpenCV For Windowsのリンクからインストーラをダウンロードします。  
あとはインストーラの指示通りにインストールしてください。

#### Tesseractインストール
[https://code.google.com/p/tesseract-ocr/downloads/detail?name=tesseract-ocr-setup-3.02.02.exe](https://code.google.com/p/tesseract-ocr/downloads/detail?name=tesseract-ocr-setup-3.02.02.exe)

### 初期設定
`resultoon.ini` ファイルにて以下の設定を行うことができます。

|          項目          |                     意味                    | 例 |
|------------------------|---------------------------------------------|----|
| SAVE_IMAGE_PATH        | キャプチャした画像の保存先フォルダ          |    |
| GOOGLE_APPS_SCRIPT_URL | Google Spreadsheetに送信する場合の送信先URL |    |
| CAPTURE_DEVICE_ID      | HDMIキャプチャボードのデバイスID            |    |


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

### Google Spreadsheetの設定(上級者向け)
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

#### Google Spreadsheetに送信されるデータ(json)の例
```
{
    udemae_point: 31,
    udemae_diff: -6,
    members: [
        {
            team: "win",
            rank:35,
            udemae: "S",
            kill: 12,
            death: 6
        },
        {
            team: "win",
            rank:35,
            udemae: "S",
            kill: 12,
            death: 6
        },
        {
            team: "win",
            rank:35,
            udemae: "S",
            kill: 12,
            death: 6
        },
        {
            team: "win",
            rank:35,
            udemae: "S",
            kill: 12,
            death: 6
        },
        {
            team: "lose",
            rank:42,
            udemae: "S",
            kill: 8,
            death: 9
        },
        {
            team: "lose",
            rank:35,
            udemae: "S",
            kill: 7,
            death: 9
        },
        {
            team: "lose",
            rank:33,
            udemae: "S",
            kill: 3,
            death: 2
        },
        {
            team: "lose",
            rank:45,
            udemae: "S+",
            kill: 1,
            death: 8,
            isPlayer: True
        },
    ]
}
```


## FAQ
### アナログキャプチャボードでは動作しますか？
動作しません。HDMIキャプチャボード経由で画像を取得することを前提にしたアルゴリズムを実装しているためです。

### Macで動作しますか？
未検証です。検証歓迎します。