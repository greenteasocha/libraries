# 遅延伝播セグメントツリー

## 何ができる?

数列に対して、以下の操作がO(logN)でできる。(Nは数列の長さ)

- ある区間の値に対して一定の演算をする。(例えば、掛け算)
```
10| 2 | 8 | 6 | 4 | 2 | 0 | 9
      |-       x3        -| 
                ↓
10| 2 | 24| 18| 12| 6 | 0 | 9
```
- ある区間に対しての値を取得する(例えば、区間の和)

```
10| 2 | 24| 18| 12| 6 | 0 | 9
              |-  range sum  -|
> 27
```

演算およびクエリ以外には、上記に挙げた物以外にも一定の性質を満たす物があれば組み込むことができる。

詳しい話は理解が及んでおらずまだ説明できないので、勉強する
- 参考
https://opt-cp.com/cp/lazysegtree-practice/ 他、色々

## 実装に当たって参考にした物
- https://maspypy.com/segment-tree-%E3%81%AE%E3%81%8A%E5%8B%89%E5%BC%B72
- https://smijake3.hatenablog.com/entry/2018/11/03/100133
- https://tsutaj.hatenablog.com/entry/2017/03/30/224339

<<<<<<< HEAD
他、yosupo judgeの提出一覧などq
=======
他、yosupo judge(Range Affine Range Sum)の AC一覧など 色々
>>>>>>> fa164848ad1f46fa63acdc757e35e7eb5c7f2b29

## がんばった
非再帰、抽象化をした

## verify 
https://judge.yosupo.jp/submission/27653
