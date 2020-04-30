# nlpapi_entityresolver



## sudachi_entry_aliases.jsonl

- [Sudachi 同義語辞書](https://github.com/WorksApplications/SudachiDict/blob/develop/docs/synonyms.md) にある synonyms.txt をダウンロード
- python3 convert_sudachi.py を実行してスクリプトが読み込み可能な形式にする

## wikipedia_entry_aliases.jsonl

- [Wikidata](https://www.wikidata.org/wiki/Wikidata:Database_download/)内に含まれる aliases エントリに基づく同義語辞書
```
 $ wget https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.gz
```
- TODO: convert_wikidata.py は再現性不十分なので直す
- [元データ](https://dumps.wikimedia.org/wikidatawiki/entities/)
- [元データ仕様](https://www.mediawiki.org/wiki/Wikibase/DataModel/JSON)
- リダイレクト情報から構築することも可能: https://qiita.com/yukinoi/items/78d64aeb3afbaadf52b1


## Build and Run

```
docker build -t nlpapi-synonyms .
docker run --rm --name nlpapi-synonyms -p 9000:80 nlpapi-synonyms
```