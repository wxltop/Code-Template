import torch
from IPython import display
from matplotlib import pyplot as plt


def use_svg_display():
    """使用svg格式在jupyter中显示绘图
    """
    display.set_matplotlib_formats('svg')

def show_heatmaps(matrices, xlabel, ylabel, titles=None, figsize=(2.5, 2.5), cmap='Reds'):
    """热力图显示，输入一个矩阵matrices，将其以热力图的方式在jupyter notebook中显示

    Args:
        matrices (numpy or torch.FloatTensor): 形状一定要是(n, m, height, width), n和m分别表示纵轴和横轴subplot的个数
        xlabel (str): [description]
        ylabel (str): [description]
        titles (str, optional): [description]. Defaults to None.
        figsize (tuple, optional): [description]. Defaults to (2.5, 2.5).
        cmap (str, optional): Reds or Blues or Greens. Defaults to 'Reds'.
    
    Examples
    --------
    ::
    
        # use numpy: 
        res = np.random.randn(6, 8).reshape((1, 1, 6, 8))
        show_heatmaps(res, xlabel, ylabel, title, figsize, cmap)
        
        # use torch:
        res = torch.randn(6, 8).reshape((1, 1, 6, 8))
        show_heatmaps(res, xlabel, ylabel, title, figsize, cmap)
        
    """
    # use_svg_display()
    num_rows, num_cols = matrices.shape[0], matrices.shape[1]
    fig, axes = plt.subplots(num_rows, num_cols, figsize=figsize,
                             sharex=True, sharey=True, squeeze=False)
    
    for i, (row_axes, row_matrices) in enumerate(zip(axes, matrices)):
        for j, (ax, matrix) in enumerate(zip(row_axes, row_matrices)):
            if type(matrix) == torch.FloatTensor or type(matrix) == torch.DoubleTensor or type(matrix) == torch.IntTensor:
                pcm = ax.imshow(matrix.detach().numpy(), cmap=cmap)
            else:
                pcm = ax.imshow(matrix, cmap=cmap)
            if i == num_rows - 1:
                ax.set_xlabel(xlabel)
            if j == 0:
                ax.set_ylabel(ylabel)
            if titles:
                ax.set_title(titles[j])
    fig.colorbar(pcm, ax=axes, shrink=0.6)