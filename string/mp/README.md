# MP および文字列検索

## 何ができる？
長さ N の文字列の中に長さ M (<=N) の文字列があるかを判定し、あればその場所をすべて抜き出す
計算量は O(N) (のはず)

## 例
```
query  ... "ABABC"
target ... "ABABCABABABC"
result ... [100000010000]
```

## がんばった
テスト作成

## 参考文献
**MPによる前処理テーブルの作成**  
https://snuke.hatenablog.com/entry/2014/12/01/235807  
https://snuke.hatenablog.com/entry/2017/07/18/101026  

**テーブルを用いた文字列検索**  
http://sevendays-study.com/algorithm/ex-day2.html  
https://tech.retrieva.jp/entry/2020/05/21/134735  

など

## verify
外部のテストケースではまだ
