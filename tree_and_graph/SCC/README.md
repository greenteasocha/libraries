# Strongly Connected Component (強連結成分分解)

## 何ができる？
有向グラフを「互いに行き来できる頂点たちのグループ」に分割する  
出来上がった各グループを一つの頂点とみなしたとき、必ずグラフはDAGになる。(かつ、このライブラリで得られたグループの順番はトポソされた順になっている。)  
計算量 O(|E|+|V|)

## 頑張ったところ
非再帰にした 
帰りがけの処理がある場合もstackで扱えるようになった

## 参考にしたもの
https://hkawabata.github.io/technical-note/note/Algorithm/graph/scc.html  
https://manabitimes.jp/math/1250

## verify
ACL Practice - G  
https://atcoder.jp/contests/practice2/submissions/22179262

typical90 - 21  
https://atcoder.jp/contests/typical90/submissions/22179275
