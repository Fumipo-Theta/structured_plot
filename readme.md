# structured_plot

このパッケージは宣言的で再利用可能なパーツを組み合わせてデータプロットを行うためのものである.
また, このパッケージは `matplotlib` を使用したプロットのラッパーでもある.

## Import

```python
from structured_plot import Figure, Subplot, Layout, plot_action
```

## Subplot

`Subplot` (`ISubplot` の具象クラス) を用い, 何のデータとどのようなプロット方法を行うかを宣言する.

例えば, あるデータ `data` のうち, 変数 `x` と `y` を用いて散布図と折れ線図を行うサブプロットはそれぞれ次のように宣言する.

```python
plot_scatter_xy = Subplot().add(
    data,
    x="x",
    y="y",
    plot=[plot_action.scatter(c="black")]
)

plot_line_xy = Subplot().add(
    data,
    x="x",
    y="y",
    plot=[plot_action.line(linewidth=2)]
)
```

上記の散布図と折れ線図を重ね合わせる場合, 作成したそれぞれの `Subplot` インスタンスの和を取れば良い.

```python
plot_xy_point_and_line = plot_scatter_xy + plot_line_xy
```

または, この場合のように用いるデータと変数名が共通ならば, 引数 `plot` に与えるplot_actionの
リストの要素を増やしても良い.

```python
plot_xy_point_and_line = Subplot().add(
    data,
    x="x",
    y="y",
    plot=[
        plot_action.scatter(c="black"),
        plot_action.line(linewidth=2)
    ]
)
```

このようにして作成した `Subplot` インスタンスは, 次の `Figure` オブジェクトに登録することで
実際にプロットイメージ作成に使われる.

## Figure

`Figure`
