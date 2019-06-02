# structured_plot

このパッケージは宣言的で再利用可能なパーツを組み合わせてデータプロットを行うためのものである.
また, このパッケージは `matplotlib` を使用したプロットのラッパーでもある.

## Import

```python
from structured_plot import Figure, Subplot, SubplotTime, Layout, plot_action
```

## Subplot

`Subplot` (`ISubplot` の具象クラス) を用い, 何のデータとどのようなプロット方法を行うかを宣言する.

例えば, あるデータ `data` のうち, 変数 `x` と `y` を用いて散布図と折れ線図を行うサブプロットはそれぞれ次のように宣言する.

```python
plot_scatter_xy = Subplot().add(
    data,
    x="x",
    y="y",
    xlabel="x",
    ylabel="y",
    plot=plot_action.scatter(c="black")
)

plot_line_xy = Subplot().add(
    data,
    x="x",
    y="y",
    xlabel="x",
    ylabel="y",
    plot=plot_action.line(linewidth=2)
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
    xlabel="x",
    ylabel="y",
    plot=[
        plot_action.scatter(c="black"),
        plot_action.line(linewidth=2)
    ]
)
```

サブプロットの軸ラベルや目盛りラベルのフォントファミリーやフォントサイズ, フォンカラーといった見た目の情報は `Subplot` インスタンス初期化時に引数で指定することができる.

```python
axes_style = dict(
    xlabel = {"fontsize" : 16},
    ylabel = {"family" : "serif", "fontstyle" : "italic"},
    tick = {"labelsize" : 12},
    xtick = {"labelbottom" : False},
    grid = {"axis" : "both"},
    xlim=[0,1],
    ylim=[0,1]
)

styled_subplot = Subplot(axes_style)
```

なお, `Subplot` インスタンス同士の和をとったときには, 最初の `Subplot` のスタイルが引き継がれる.

このようにして作成した `Subplot` インスタンスは `Figure` オブジェクトに登録されプロットイメージの作成に使われる.

### SubplotTime

`SubplotTime` は時系列データの表示に特化したクラスである.
インスタンス初期化時に `xFmt` オプションを渡すことで時間軸の表示フォーマットを指定できる.
また, 時間軸の変数の指定には `add` メソッド呼び出し時に `index` オプションを用いる.

```python
time_subplot = SubplotTime(xFmt="%Y/%m/%d %H:%M:%S")\
    .add(
        time_series_data,
        index="datetime",
        y="y",
        plot=plot.line()
    )
```

複数の変数を結合して時間軸の変数を作成するときは, `index` オプションに変数名のリストを渡す.

```python
time_subplot = SubplotTime(xFmt="%Y/%m/%d %H:%M:%S")\
    .add(
        time_series_data,
        index=["date", "time"],
        y="y",
        plot=plot.line()
    )
```

## Figure

`Figure` インスタンスにはいくつかの `Subplot` インスタンスを登録できる. 次のコマンドは, 変数 x, y の散布図を作成することを表す.

```python
figure = Figure()
figure.add_subplot(plot_xy_point)
```
上記のコマンドはメソッドチェーンにより次のようにもかける.

```python
figure = Figure().add_subplot(plot_xy_point)
```

また, 次のコマンドはいずれも変数 x, y に関する散布図と折れ線図の2つのサブプロットを作成することを示す.

```python
# add_subplot を複数回呼び出す
figure = Figure()\
    .add_subplot(plot_xy_point)\
    .add_subplot(plot_xy_line)

# add_subplot に複数の Subplot インスタンスを渡す
figure = Figure()\
    .add_subplot(
        plot_xy_point,
        plot_xy_line
    )

# 複数の Figure インスタンスの和を取る
figure_xy_point = Figure().add_subplot(plot_xy_point)
figure_xy_line = Figure().add_subplot(plot_xy_line)
figure = figure_xy_point + figure_xy_line
```

`Figure` インスタンスも各 `Subplot` インスタンスのいずれもサブプロットのレイアウトの情報を持たないので, 実際にプロットイメージを作成するには `show` メソッドにレイアウト情報を渡す.

次のコマンドは, 変数 x, y の散布図を 6 inches * 6 inches の大きさで作成することを示す.
デフォルト dpi は72であるので, 432 px * 432 px の図が出来上がる.

```python
figure = Figure().add_subplot(plot_xy_plot)

fig, axes = figure.show(size=(6,6))
```

戻り値の `fig` は `matplotlib.figure.Figure` インスタンスで, `axes` は サブプロット名をキーとし, `matplotlib.axes._axes.Axes` インスタンスをバリューとする辞書である. サブプロット名は `add_subplot` 時に `names` オプションで指定できる. デフォルトは 0 から始まる整数の連番になる. 上記の例では, `axes[0]` が散布図の情報を持つ `Axes` インスタンスである. `Axes` インスタンスを用いることで, プロット作成後に細かい調整を行うこともできる.


```python
fig, axes = Figure().add_subplot(plot_xy_point, names="a")\
    .show(size=(6,6))
# axes has key of "a"
# Set limit of x axis manually
axis.get("a").set_xlim([0,1])

fig, axes = Figure().add_subplot(
    plot_xy_point,
    plot_xy_line,
    names=["a","b"]
).show(size=(6,6))
# Set names of multiple subplots
# axes has keys of "a" and "b"
```

`show` メソッドの引数の指定方法にはいくつかのパターンがある.
最も単純なのは, 上記の例のように `size` として数値からなるタプルを一つだけ渡す場合である.
`size` オプションはグリッドレイアウトを作成し, タプルが渡されると等しいサイズのサブグリッドに区切られる.

さらに, `column` オプションでグリッドの列数を指定でき, `margin` オプションでサブプロット間の横と縦の間隔を指定できる.

また, `order` オプションで各 `Subplot` インスタンスを何番目のサブグリッドに対応付けるか指定できる.
サブグリッドの番号は, 行方向に0から数える.

```python
figure = Figure().add_subplot(
    plot_xy_point,
    plot_xy_point,
    plot_xy_point,
    plot_xy_line,
    plot_xy_line,
    plot_xy_line,
    names=["a","b","c","d","e","f"]
)

figure.show(size=(4,4))
# Layout of 1 x 6 grid
# a b c d e f

figure.show(size=(4,4), column=3)
# Layout of 2 x 3 grid
# a b c
# d e f

figure.show(size=(4,4), column=3, margin=(0,0), order=[0,3,1,4,2,5])
# Layout of 2 x 3 grid with no margin
# Order of subgrid
# 0 1 2
# 3 4 5
# Align of subplots
# a c e
# b d f
```

`size` オプションに数値からなるタプルのリストを指定すると, グリッド上に各タプルで指定されたサイズのサブグリッドが生成される.

```python
figure.show([(4,4),(8,4)]*3, column=2)
# Layout of 3 x 2 grid
# Order of subgrid
# 0 1
# 2 3
# 4 5
# Align and sizes of subgrids
# a bb
# c dd
# e ff
```

サブグリッドの数がサブプロットより少ない場合, 余ったサブプロットは表示されない.
サブグリッドの数がサブプロットより大きい場合, サブグリッドのスペースは確保されるが何も表示されない.

より自由なレイアウトを行いたい場合, `show` メソッドに次の `Layout` インスタンスを指定する.

## Layout

`Layout` はサブグリッドのサイズと配置を実際の長さを用いて指定する方法を提供する.

最初のサブグリッドのサイズを決めるために, `add_origin` メソッドを用いる.
他のメソッドは, すでに作成したサブグリッドに対する相対的な位置を元に新しいサブグリッドを作成するために用いる.

`from_left_top`, `from_left_bottom`, `from_right_top`, `from_right_bottom` メソッドはそれぞれ, 主に既存のサブグリッドの内部に新しいサブグリッドを作る際に用いる.

`add_right`, `add_bottom`, `add_left`, `add_top` メソッドはそれぞれ, 主に既存のサブグリッドの外側に新しいサブグリッドを作る際に用いる.

```python
layout = Layout()
layout.add_origin("a", size=(8,8))
layout.from_left_top("a", "b", size=(4,2), offset=(0,0))
layout.from_right_top("a", "c", size=(2,4), offset=(0,0))
layout.from_right_bottom("a", "d", size=(4,2), offset=(0,0))
layout.from_left_bottom("a", "e", size=(2,4), offset=(0,0))

# Layout "b" and "c" inset of "a"
# b b a c
# a a a c
# e a a a
# e a d d


layout = Layout()
layout.add_origin("a", size=(8,8))
layout.add_right("a", "b", size=(4,4), margin=1)
layout.add_bottom("a", "c" size=(4,4), margin=1)
layout.add_left("a", "d" size=(4,4), margin=1)
layout.add_top("a", "c" size=(4,4), margin=1)
#   e
# d a a b
#   a a
#   c

layout = Layout()
layout.add_origin("a" size=(8,8))
layout.add_right("a", "b", size=(4,4), margin=0, offset=(0,2))
# a a a a
# a a a a b b
# a a a a b b
# a a a a
```

作成した `Layout` インスタンスに従ってサブプロットを配置するには, `Figure` インスタンスの `show` メソッドに `order` オプションと共に渡す.

```python
figure.show(layout, order=["a","b","c","d","e"])
```

## plot_action

`plot_action` モジュールに含まれる関数は, スタイルに関するオプションを引数にとる.
基本的には `matplotlib` の同名のメソッドのキーワード引数と同じ引数をとる.
ただし, 引数として `pandas.DataFrame` をとる関数を指定しておくと, プロット実行時にデータフレーム計算された値が渡される.

```python
red_line_width2 = plot_action.line(color="red", linewidth=2)

bubble_plot = plot_Action.scatter(
    s=lambda df: df["z"].apply(np.sqrt)
)
```
