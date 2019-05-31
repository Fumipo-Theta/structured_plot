---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.0'
      jupytext_version: 0.8.2
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
  language_info:
    codemirror_mode:
      name: ipython
      version: 3
    file_extension: .py
    mimetype: text/x-python
    name: python
    nbconvert_exporter: python
    pygments_lexer: ipython3
    version: 3.7.0
---

```python
import matplotlib.pyplot as plt

from figure import Figure
from subplot import Subplot
import plot_action as plot
```

```python
moc = {"x":[0,1,2],"y": [0,1,4]}

f1 = Figure()

f1.add_subplot(Subplot().add(
    moc,
    x="x",
    y="y",
    plot=[plot.scatter()]
))

f2 = Figure().add_subplot(
    Subplot(axes_spec={"projection":"polar"}).add(
        moc,
        x="x",
        y="y",
        ylim=[0,10],
        plot=[plot.line()]
    ),
    names=["b"]
)


f3 = Figure().add_subplot(
    Subplot().add(
        moc,
        x="x",
        y="y",
        plot=[plot.line()]
    )
)

f = f1+f2+f3

f.show(size=(4,4),column=3)
```

```python

```
