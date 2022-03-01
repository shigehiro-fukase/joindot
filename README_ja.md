# joindot
Graphviz の .dot ファイルを結合するpython スクリプト

- 入力: 複数の .dot ファイル
  - 中には `digraph` が一つ入っているものとします
- 出力: 単一の .dot ファイル
  - 単一の `digraph` を出力します
    - 中には各ファイルの `digraph` を `subgraph` にして保持します

