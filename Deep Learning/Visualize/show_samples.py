import torch
import matplotlib.pyplot as plt


def show_images(imgs, num_rows, num_cols, titles=None, scale=1.5):
    """可视化一些图像数据样本

    Args:
        imgs ([type]): List[numpy.ndarray, numpy.ndarray...]
        num_rows ([type]): [description]
        num_cols ([type]): [description]
        title ([type], optional): [description]. Defaults to None.
        scale (float, optional): [description]. Defaults to 1.5.
    
    Example: 
        ```python script
        import PIL.Image as Image
        import os
        imgs = os.listdir('image')
        res = []
        for img in imgs:
            img = Image.open(os.path.join('image', img))
            res.append(img)
        ax = show_images(res, 2, 4, titles=[0, 1, 2, 3, 4, 5, 6, 7])
        plt.show()
        ```
        
        ```jupyter notebook
        %matplotlib inline
        import PIL.Image as Image
        import os
        imgs = os.listdir('image')
        res = []
        for img in imgs:
            img = Image.open(os.path.join('image', img))
            res.append(img)
        ax = show_images(res, 2, 4, titles=[0, 1, 2, 3, 4, 5, 6, 7])
        ```
    """
    
    figsize = (num_cols * scale, num_rows * scale)
    _, axes = plt.subplots(num_rows, num_cols, figsize=figsize)
    axes = axes.flatten()
    for i, (ax, img) in enumerate(zip(axes, imgs)):
        if torch.is_tensor(img):
            # 图片张量
            ax.imshow(img.numpy())
        else:
            # PIL图片
            ax.imshow(img)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        if titles:
            ax.set_title(titles[i])
    return axes