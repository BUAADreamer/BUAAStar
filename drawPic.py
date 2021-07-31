import matplotlib
import matplotlib.pyplot as plt
import os

matplotlib.use('Agg')


def drawLine(y):
    if os.path.exists('./static/images/draw/line.png'):
        os.remove('./static/images/draw/line.png')
    x = list(range(len(y)))
    plt.figure()
    plt.plot(x, y, marker='o', color='r', label='price')
    plt.legend()
    plt.xlabel('num')
    plt.ylabel('price')
    plt.savefig('./static/images/draw/line.png')
    return


def drawHist(y):
    if os.path.exists('./static/images/draw/hist.png'):
        os.remove('./static/images/draw/hist.png')
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
    # 添加图形属性

    plt.xlabel('序号')
    plt.ylabel('价格')
    plt.title('商品价格直方图')

    first_bar = plt.bar(range(len(y)), y, color='blue')  # 初版柱形图，x轴0-9，y轴是列表y的数据，颜色是蓝色

    # 开始绘制x轴的数据
    index = list(range(len(y)))
    # name_list = ['a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9']  # x轴标签
    plt.xticks(index)  # 绘制x轴的标签

    # 柱形图顶端数值显示
    for data in first_bar:
        y = data.get_height()
        x = data.get_x()
        plt.text(x + 0.15, y, str(y), va='bottom')  # 0.15为偏移值，可以自己调整，正好在柱形图顶部正中

    # 图片的显示及存储
    plt.savefig("./static/images/draw/hist.png")
