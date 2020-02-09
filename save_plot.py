import os
import re
import matplotlib.pyplot as plt


def __safe_filename(filename: str) -> str:
    return filename.replace("/", "").replace("\\", "")


def __mkdir(f):
    def wrapper(directory, *arg, **kwargs):
        if not os.path.isdir(directory):
            os.makedirs(directory)
        return f(directory, *arg, **kwargs)
    return wrapper


def __actionSavePNG(directory, filename):
    # パスが有効かどうかを検証し, ディレクトリがなければ作成する
    def save(postfix=""):
        path = directory+__safe_filename(filename+postfix+'.png')
        plt.savefig(path)
        print(f"save as png: {path}")
    return save


def __IFigureSaver(ext):
    if re.match(r"[pP](ng|NG)$", ext):
        return __actionSavePNG


@__mkdir
def save_plot(directory, fileName, ext="png"):
    saver = __IFigureSaver(ext)
    return saver(directory, fileName)
