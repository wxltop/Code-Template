"""本脚本存放的是常见类型文件的读写操作。
"""
import os
import json, csv
import os.path as osp
from typing import Iterable


#************************** Json file *****************************
def dict2json(dict_: dict, dst: str) -> None:
    """输入一个字典结构数据，将字典转换为json格式数据存放在dst路径
        #! 可以解决中文写入的问题
    Args:
        dict_ (dict): dict Data
        dst (str): the path of json file
    """
    if not osp.exists(osp.dirname(osp.abspath(dst))):
        os.makedirs(osp.dirname(osp.abspath(dst)))
        
    assert dst.endswith('.json'), print("输出路径必须将json文件名加上！")
    
    json_str = json.dumps(dict_, indent=4, ensure_ascii=False)
    with open(dst, 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)


def loadjson(jsonfile: str) -> dict:
    """输入json路径，读取数据并以字典的格式返回
        #! 可以解决包含中文的json文件读取的问题
    Args:
        jsonfile (str): dir to json file

    Returns:
        dict: json contents
    """
    assert osp.exists(jsonfile), print("Json file does not exists!")
    f = open(jsonfile, 'r', encoding='utf-8')
    result = json.loads(f.read())
    f.close()
    return result


#************************** txt file *******************************
def loadtxt(txtfile: str) -> list:
    """输入txt路径，读入数据并以列表格式返回，列表每一项表示一行，已经去除换行符
        #! 解决中文读入问题
    Args:
        txtfile (str): dir to txt file

    Returns:
        list: result list
    """
    
    assert osp.exists(txtfile), print('txt file does not exists!')
    with open(txtfile, 'r', encoding='utf-8') as f:
        res = f.readlines()
    
    # 去除换行符
    res = [line.split('\n')[0] for line in res]
    return res

def dumptxt(content: list, dst: str) -> None:
    """将列表数据存放在txt文件中，列表每一个元素表示一行
    #! 可以解决中文写入的问题，注意，列表中每一个元素后不能带换行符，否则会出现空行

    Args:
        content (list): content
        dst (str): destination
    """
    if not osp.exists(osp.dirname(osp.abspath(dst))):
        os.makedirs(osp.dirname(osp.abspath(dst)))
        
    assert dst.endswith('.txt'), print("输出路径必须将txt文件名加上！")
    
    with open(dst, 'w', encoding='utf-8') as f:
        for line in content:
            if isinstance(line, str):
                f.write(line)
            else:
                f.write(str(line))
            f.write('\n')
            
            
#************************** csv file *******************************
def dumpcsv(content: Iterable[Iterable], dst: str) -> None:
    """将content写入一个csv文件，content是一个可迭代对象，其中每一个元素也是可迭代对象
        #! 可以解决中文写入问题
    Args:
        content (Iterable[Iterable]): content
        dst (str): destination
    """
    if not osp.exists(osp.dirname(osp.abspath(dst))):
        os.makedirs(osp.dirname(osp.abspath(dst)))
        
    assert dst.endswith('.csv'), print("输出路径必须将csv文件名加上！")
    
    with open(dst, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        for line in content:
            writer.writerow(line)


def loadcsv(csvfile: str) -> list:
    """读入csv文件内容
    #! 可以解决中文读入问题

    Args:
        csvfile (str): csv path

    Returns:
        list: List[List]
    """
    assert osp.exists(csvfile), print('txt file does not exists!')
    
    res = []
    
    with open(csvfile, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            res.append(row)
    return res
