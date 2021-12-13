 
import numpy as np
from IPython import display
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
from functools import partial
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
 

#****************************** jupyter notebook show animation *********************************
def use_svg_display():
    """使用svg格式在jupyter中显示绘图
    """
    display.set_matplotlib_formats('svg')


def set_axes(axes, xlabel, ylabel, xlim, ylim, xscale, yscale, legend):
    """用于设置由matplotlib生成图表的轴的属性

    Args:
        axes ([type]): [description]
        xlabel ([type]): [description]
        ylabel ([type]): [description]
        xlim ([type]): [description]
        ylim ([type]): [description]
        xscale ([type]): [description]
        yscale ([type]): [description]
        legend ([type]): [description]
    """
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel)
    axes.set_xscale(xscale)
    axes.set_yscale(yscale)
    axes.set_xlim(xlim)
    axes.set_ylim(ylim)
    if legend:
        axes.legend(legend)
    axes.grid()
    
    
class Animator:  
    """在动画中绘制数据。用于jupyter notebook
    
    Example1:
        在一个训练函数train(net, train_iter, test_iter, loss, num_epochs, updater)中，
        首先定义一个Animator对象:
        ```python
        animator = Animator(xlable='epoch', xlim=[1, num_epochs], ylim=[0.3, 0.9],
                            legend=['train loss', 'train acc', 'test acc'])
        ```
        然后在每一个epoch之后，添加如下:
        ```python
        animator.add(epoch+1, train_metrics + (test_acc, ))
        ```
    
    Example2:
        ```pyton
        import time
        import numpy as np
        animator = Animator(xlabel='epochs', ylabel='value', xlim=[0, 3], ylim=[0, 20],
                            legend=['train loss', 'train acc', 'test acc', 'test loss'], figsize=(7, 4))
        x = 0
        for _ in range(30):
            x += 0.1
            _y = (np.sin(x)*10, np.cos(x)*10, x ** 2, 10 * x)
            animator.add(x, _y)
            time.sleep(1)
        ```
    """
    def __init__(self, xlabel=None, ylabel=None, legend=None, xlim=None,
                 ylim=None, xscale='linear', yscale='linear',
                 fmts=('-', 'm--', 'g-.', 'r:', 'bo', 'go--', 'r+'), nrows=1, ncols=1,
                 figsize=(3.5, 2.5)):
        # 增量地绘制多条线
        if legend is None:
            legend = []
        use_svg_display()
        self.fig, self.axes = plt.subplots(nrows, ncols, figsize=figsize)
        if nrows * ncols == 1:
            self.axes = [self.axes, ]
        # 使用lambda函数捕获参数
        self.config_axes = lambda: set_axes(
            self.axes[0], xlabel, ylabel, xlim, ylim, xscale, yscale, legend)
        self.X, self.Y, self.fmts = None, None, fmts

    def add(self, x, y):
        # 向图表中添加多个数据点
        if not hasattr(y, "__len__"):
            y = [y]
        n = len(y)
        if not hasattr(x, "__len__"):
            x = [x] * n
        if not self.X:
            self.X = [[] for _ in range(n)]
        if not self.Y:
            self.Y = [[] for _ in range(n)]
        for i, (a, b) in enumerate(zip(x, y)):
            if a is not None and b is not None:
                self.X[i].append(a)
                self.Y[i].append(b)
        self.axes[0].cla()
        for x, y, fmt in zip(self.X, self.Y, self.fmts):
            self.axes[0].plot(x, y, fmt)
        self.config_axes()
        display.display(self.fig)
        display.clear_output(wait=True)

#****************************************************************************

#******************************** python shell show animation *******************************
# class Animator2():
#     def __init__(self, xlabel=None, ylabel=None, legend=None, xlim=None,
#                  ylim=None, xscale='linear', yscale='linear',
#                  fmts=('-', 'm--', 'g-.', 'r:', 'bo', 'go--', 'r+'), nrows=1, ncols=1,
#                  figsize=(3.5, 2.5)) -> None:
#         # 增量地绘制多条线
#         if legend is None:
#             legend = []
            
#         plt.style.use('fivethirtyeight')
#         self.fig, self.axes = plt.subplots(nrows, ncols, figsize=figsize)
#         if nrows * ncols == 1:
#             self.axes = [self.axes, ]
#         # 使用lambda函数捕获参数
#         self.config_axes = lambda: set_axes(
#             self.axes[0], xlabel, ylabel, xlim, ylim, xscale, yscale, legend)
#         self.X, self.Y, self.fmts = None, None, fmts

#     def animate(self, i):
#         # i表示的是经历过的"时间", 即每调用一次animate函数, i的值会自动加一

#         # plt对象的cla方法: clear axes: 清除当前轴线(前面说过axes对象表示的是plt整个figure对象下面的一个绘图对象, 一个figure可以有多个axes, 其实就是当前正在绘图的实例).
#         # 我们可以不清除当前的axes而沿用前面的axes, 但这样会产生每次绘出来的图形都有很大的变化(原因是重新绘制的时候,颜色,坐标等都重新绘制,可能不在同一个地方了,所以看上去会时刻变化).
#         # 因此必须要清除当前axes对象,来重新绘制.
#         plt.cla()
#         for x, fmt in zip(self.X, self.fmts):
#             for y in self.Y:
#                 plt.plot(x, y, label='Channel 1')
#         self.config_axes()
#         # plt.legend(loc='upper left')
#         plt.tight_layout()
    
#     def add(self, x, y):
#         # 向图表中添加多个数据点
#         if not hasattr(y, "__len__"):
#             y = [y]
#         n = len(y)
#         if not hasattr(x, "__len__"):
#             x = [x] * n
#         if not self.X:
#             self.X = [[] for _ in range(n)]
#         if not self.Y:
#             self.Y = [[] for _ in range(n)]
        
#         for i, (a, b) in enumerate(zip(x, y)):
#             if a is not None and b is not None:
#                 self.X[i].append(a)
#                 self.Y[i].append(b)
#         self.axes[0].cla()
#         for x, y, fmt in zip(self.X, self.Y, self.fmts):
#             self.axes[0].plot(x, y, fmt)
#         self.config_axes()
#         display.display(self.fig)
#         display.clear_output(wait=True)
                
#     def animation_show(self):
#         # 利用itertools里的count创建一个迭代器对象,默认从0开始计数, 是一个"无限大"的等差数列
#         index = count()
#         x = 0
#         # FuncAnimation可以根据给定的interval(时间间隔, ms为单位)一直重复调用某个函数来进行绘制, 从而模拟出实时数据的效果.
#         x += 1
#         y1 = np.random.rand(1)
#         y2 = np.random.rand(1)

#         ani = FuncAnimation(plt.gcf(), self.animate, fargs=(x, y1, y2, y3, y4), interval=1000)

#         plt.show()


#************************************************************************

#*************************** plot lines in a fig (max for 4) *************************
def set_figsize(figsize=(4, 3)):
    """设置matplotlib图表大小

    Args:
        figsize (tuple, optional): 图表的形状. Defaults to (3.5, 2.5).
    """
    use_svg_display()
    plt.rcParams['figure.figsize'] = figsize
    
    
def plot(X, Y=None, xlabel=None, ylabel=None, legend=None, 
         xlim=None, ylim=None, xscale='linear', yscale='linear',
         fmts=('-', 'm--', 'g-.', 'r:'), figsize=(7, 4), axes=None):
    """绘制数据点

    Args:
        X ([type]): [description]
        Y ([type], optional): [description]. Defaults to None.
        xlabel ([type], optional): [description]. Defaults to None.
        ylabel ([type], optional): [description]. Defaults to None.
        legend ([type], optional): [description]. Defaults to None.
        xlim ([type], optional): [description]. Defaults to None.
        ylim ([type], optional): [description]. Defaults to None.
        xscale (str, optional): [description]. Defaults to 'linear'.
        yscale (str, optional): [description]. Defaults to 'linear'.
        fmts (tuple, optional): [description]. Defaults to ('-', 'm--', 'g-.', 'r:').
        figsize (tuple, optional): [description]. Defaults to (3.5, 2.5).
        axes ([type], optional): [description]. Defaults to None.
    
    Example:
        ```python
            x = np.linspace(-2, 5, 400)
            y1 = np.sin(x)*10
            y2 = np.cos(x)*10
            y3 = x ** 2 
            y4 = 10 * x
            plot([x]*4, [y1, y2, y3, y4], xlabel='x', ylabel='value', 
                legend=['10sin(x)', '10cos(x)', 'x**2/100', '10x'])
            plt.show()
        ```
    """
    if legend is None:
        legend = []

    set_figsize(figsize)
    axes = axes if axes else plt.gca()
    
    # 如果 `X` 有⼀个轴，输出True
    def has_one_axis(X):
        return (hasattr(X, "ndim") and X.ndim == 1 or isinstance(X, list)
                and not hasattr(X[0], "__len__"))
    if has_one_axis(X):
        X = [X]
    if Y is None:
        X, Y = [[]] * len(X), X
    elif has_one_axis(Y):
        Y = [Y]
    if len(X) != len(Y):
        X = X * len(Y)
    axes.cla()
    for x, y, fmt in zip(X, Y, fmts):
        if len(x):
            axes.plot(x, y, fmt)
        else:
            axes.plot(y, fmt)
    set_axes(axes, xlabel, ylabel, xlim, ylim, xscale, yscale, legend)

#************************************************************************