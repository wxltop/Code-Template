    """本文件里存放的是对不同结构数据集的处理
    """
import os
import os.path as osp
import json
import shutil
import numpy as np
from tqdm import tqdm


#******************************* condition 1 *******************************
#*
#*
#*       datasets                                  datasets
#*         |                                         |
#*         |__class1                                 |__train
#*         |   |__image1.jpg                         |    |__images
#*         |   |__...                                |    |    |__000001.jpg
#*         |                                         |    |    |__000002.jpg
#*         |__class2                                 |    |    |__...
#*         |   |__image2.jpg                         |    |
#*         |   |__...                                |    |__annotations.txt
#*         |                      ======>            |    
#*         |__...                                    |__valid
#*                                                   |    |__images
#*                                                   |    |    |__000001.jpg
#*                                                   |    |    |__000002.jpg
#*                                                   |    |    |__...
#*                                                   |    |
#*                                                   |    |__annotations.txt
#*                                                   |
#*                                                   |__labels.json
#*
#*
#****************************************************************************
def dict2Json(dict_: dict, destination: str) -> None:
    """输入一个字典结构数据，将字典转换为json格式数据存放在destination路径

    Args:
        dict_ (dict): dict Data
        destination (str): the path of json file
    """
    json_str = json.dumps(dict_, indent=4, ensure_ascii=False)
    with open(destination, 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)


def data_split(data_path: str, output_path: str='merged_dataset', 
               train_rate: float=0.7, json_dst: str=None) -> None:
    """给定数据集，并且将相同类别的放在同一个文件夹下，需要将数据集划分为train/valid

    Args:
        data_path (str): the dataset path, contains different classes, each classes
        is a folder, each folder contains relative images
        train_rate (float, optional): [description]. Defaults to 0.7.
        json_dst (str, optional): Defaults to None.
    """
    # 这里是分为train/valid，如果想分为train/test可以将valid修改为test
    train_path = osp.join(output_path, 'train/images')
    valid_path = osp.join(output_path, 'valid/images')
    
    if osp.exists(output_path):
        shutil.rmtree(output_path)
    if not osp.exists(output_path):
        os.makedirs(output_path)
    if not osp.exists(train_path):
        os.makedirs(train_path)
    if not osp.exists(valid_path):
        os.makedirs(valid_path)
    
    dict_ = {}
    
    for id, clss in tqdm(enumerate(sorted(os.listdir(data_path)))):
        dict_[id] = clss
        img_list = os.listdir(osp.join(data_path, clss))
        order_lst = [i for i in range(len(img_list))]
        # *********随机抽取 train_rate 的数************
        train_rand = np.random.choice(order_lst, int(train_rate*len(img_list)), 
                                      replace=False)
        valid_rand = np.array(list(set(order_lst) - set(train_rand)))
        
        # **********将文件放入各自文件夹**********
        org_len_train = len(os.listdir(train_path))  # 原来路径下文件的数量
        org_len_valid = len(os.listdir(valid_path))  # 原来路径下文件的数量
        
        with open(osp.join(osp.dirname(train_path), 'annotations.txt'), 'a+', 
                  encoding='utf-8') as f:
            for i, idx in enumerate(train_rand):
                img_name = img_list[idx]
                endname = img_name.split('.')[-1]  # 文件后缀名
                newname = '%.6d.%s' % (org_len_train + i, endname)  # 新的文件名
                shutil.copyfile(osp.join(data_path, clss, img_name), 
                                osp.join(train_path, newname))
                f.write(newname + ' ' + str(id))
                f.write('\n')
                
        with open(osp.join(osp.dirname(valid_path), 'annotations.txt'), 'a+', 
                  encoding='utf-8') as f:
            for i, idx in enumerate(valid_rand):
                img_name = img_list[idx]
                endname = img_name.split('.')[-1]  # 文件后缀名
                newname = '%.6d.%s' % (org_len_valid + i, endname)  # 新的文件名
                shutil.copyfile(osp.join(data_path, clss, img_name), 
                                osp.join(valid_path, newname))
                f.write(newname + ' ' + str(id))
                f.write('\n')
    
    # 将int -> label的映射文件存放在data_path的上一级目录下
    if json_dst is None:
        dict2Json(dict_, osp.join(output_path, 'labels.json'))
    else:
        assert json_dst.endswith('.json')
        dict2Json(dict_, json_dst)
