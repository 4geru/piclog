# 日記自動生成アプリ

## 概要

画像からpdfを自動生成する.

## 利用方法

python3 \_application\_name\_  \_IMAGE\_URL\_

##  仕様技術

### 言語
||利用技術|その他|
|:---|:---|:---|
|言語|python|3.6.0|
|利用API|A3RT Proofreading API|文章添削|
||A3RT Text suggest API|文章作成|
||Azure Vision API|画像から単語を作成|
|ライブラリ|requests|APIリクエスト|
||mecab-python3|自然言語処理|
||pillow|画像処理|
||reportlab|pdf作成|
||coverage|coverage測定|
||python-dotenv|環境変数|

## その他
### test/coverageの使い方

```
 $ python -m unittest discover tests
 $ coverage run -m unittest discover tests
```

## 参考

### pdf生成
- [PythonでPDFを生成したい そしてサイコロを作りたい - \[\[ともっくす alloc\] init\]](http://o-tomox.hatenablog.com/entry/2013/07/22/221158)
- [pythonでReportLabを使ったPDFファイルの作り方〜その２〜 - Live the Life you Lov](http://www.llul.info/entry/2016/11/07/python%E3%81%A7ReportLab%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%9FPDF%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AE%E4%BD%9C%E3%82%8A%E6%96%B9%E3%80%9C%E3%81%9D%E3%81%AE%EF%BC%92%E3%80%9C)
- [Python + Pillow(PIL)で画像の回転を行う(rotate, transpose) - Symfoware](http://symfoware.blog68.fc2.com/blog-entry-1533.html)

## test
- [Python 3 標準の unittest でテストを書く際のディレクトリ構成 - Qiita](https://qiita.com/hoto17296/items/fa0166728177e676cd36)
- [初心者のためのPythonにおけるソフトウェアテスト - MyEnigma](http://myenigma.hatenablog.com/entry/2015/05/23/173423#テストカバレージ)

## Azure
- [Computer Vision Python Quick Starts](https://docs.microsoft.com/ja-jp/azure/cognitive-services/computer-vision/quickstarts/python)
