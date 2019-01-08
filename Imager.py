import imgkit
import HTMLer


def html2jpg(html, path):
    imgkit.from_string(html, path)


def data2jpg(rows=[{}], titles=[], path=''):
    html2jpg(HTMLer.table(rows, titles), path)

