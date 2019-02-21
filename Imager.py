import imgkit
import HTMLer
from pandas import DataFrame
from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.table import Table


# 保存表格
def data_frame_to_jpg(title: str, data_frame: DataFrame, path: str):
    fig: Figure = pyplot.figure(figsize=(data_frame.shape[1] * 2, data_frame.shape[0] * 0.3))  # 创建绘图对象

    ax: Axes = fig.add_subplot(1, 1, 1)
    # ax.set_title(title)  # 图标题
    ax.axis('off')

    table: Table = ax.table(cellText=data_frame.values,  # cellColours=None,
                            cellLoc='center', # colWidths=[2] * data_frame.values.shape[1],
                            # rowLabels=data_frame.index,
                            colLabels=data_frame.columns, colLoc='center',
                            loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.2)
    # pyplot.show()
    fig.savefig(path, dpi=200)


def html2jpg(html: str, path: str):
    imgkit.from_string(html, path)


def data2jpg(rows=[{}], titles=[], path=''):
    html2jpg(HTMLer.table(rows, titles), path)

