import cv2
import os
import time
from src import config  # 写一个config.py，将本脚本中涉及到的config超参数设置一下
import shutil
from  configparser import ConfigParser
from tqdm.notebook import tqdm

class ConfigParserUper(ConfigParser):
    def optionxform(self,optionstr):
        return optionstr

class VIV():
    """输入视频路径，将视频转换为逐帧图像，处理完图像之后，可以将图像拼接成视频
    """
    def __init__(self, seq_name, input_video_path, time_interval=1, sz=None):
        """输入参数

        Args:
            seq_name (str): 视频输出视频、输出图像的保存地址都会将seq_name作为目录
            input_video_path (str): 输入视频路径
            time_interval (int, optional): 采样时间间隔. Defaults to 1.
            sz (tuple, optional): 如果input_video_path==None, 表示只需要将图像拼接成视频(img2video), 
            拼接好的视频输出路径为config.output_video_dir, 此时sz参数必须!=None, 表示需要拼接的图像size;
            如果input_video_path!=None, 表示输入视频, 而且要将视频分成图像帧(video2img), 图像帧的存放路径为config.frame_save_path,
            处理完图像帧之后使用img2video将config.frame_save_path里的图像拼接成视频, 存放在config.output_video_dir.
            Defaults to None.
        """
        self.seq_name = seq_name
        self.input_video_path = input_video_path
        self.frame_save_path = config.frame_save_path
        self.time_interval = time_interval

        if self.input_video_path is not None:
            assert os.path.exists(self.input_video_path), print("输入的视频路径不对，视频不存在！")
            self.videoCapture = cv2.VideoCapture(self.input_video_path)
            self.frame_num = self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
            self.extract_frame_num = 0
            self.fps = self.videoCapture.get(cv2.CAP_PROP_FPS)  # 视频的流畅度
            self.size = (int(self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        else:
            # 如果没有传入视频，则需要将sz参数传入
            self.size = sz
            assert sz is not None, print("sz 参数值为None!")

        if not os.path.exists(config.output_video_dir):
            os.makedirs(config.output_video_dir)
        print(f"----> 视频的大小为：W = {self.size[0]}; H = {self.size[1]}")
        self.videoWriter = cv2.VideoWriter(os.path.join(config.output_video_dir, f'{self.seq_name}.avi'), 
                                            cv2.VideoWriter_fourcc(*'MJPG'), 
                                            20, self.size)
        
    def video2img(self):
        assert self.videoCapture.isOpened(), print("video Caputure is not opened!")
        
        if os.path.exists(os.path.join(self.frame_save_path, self.seq_name)):
            shutil.rmtree(os.path.join(self.frame_save_path, self.seq_name))
        os.makedirs(os.path.join(self.frame_save_path, self.seq_name, 'img1'))
        
        success, frame = self.videoCapture.read()
        for count in tqdm(range(1, int(self.frame_num + 1))):
            success, frame = self.videoCapture.read()
            if success:
                if count % self.time_interval == 0:
                    cv2.imwrite(os.path.join(self.frame_save_path, self.seq_name, 'img1',
                                             f'{int(count / self.time_interval):06d}.jpg'), frame)
                    self.extract_frame_num = int(count / self.time_interval)
                    
        if self.time_interval == 1:
            self.frame_num = self.extract_frame_num
            
        print(f'--从视频中抽取：\t{self.extract_frame_num}帧\n')
        print(f'--视频的帧率为：\t{self.fps} fps\n')
        print(f'--逐帧图像大小：\tW: {self.size[0]}, H: {self.size[1]} \n')
        
        self.create_ini_file()

    def create_ini_file(self):
        """生成seqinfo.ini文件，将视频信息存放在这个文件中.
        """
        cf = ConfigParserUper()
        cf.add_section('Sequence')
        cf.set("Sequence", "name", self.seq_name)
        cf.set("Sequence", "imDir", config.imDir)
        cf.set("Sequence", "frameRate", str(self.fps))
        cf.set("Sequence", "seqLength", str(self.extract_frame_num))
        cf.set("Sequence", "imWidth", str(self.size[0]))
        cf.set("Sequence", "imHeight", str(self.size[1]))
        cf.set("Sequence", "imExt", config.imExt)
        
        if not os.path.exists(os.path.join(self.frame_save_path, self.seq_name)):
            os.makedirs(os.path.join(self.frame_save_path, self.seq_name))

        with open(os.path.join(self.frame_save_path, self.seq_name, "seqinfo.ini"), "w+") as f:
            cf.write(f)
    
    def img2video(self, image_path: str=None):
        """
            如果使用VIV类仅仅为了拼接图像为视频，可以传入image_path参数，
            正常情况下该参数值为None
        """
        assert image_path is not None or self.input_video_path is not None, print("没有输入视频，也没有输入切割图像的路径！")

        if image_path is None:
            image_path = os.path.join(self.frame_save_path, self.seq_name)

        imgs = sorted(os.listdir(image_path), key=lambda x: int(x.split('.')[0]))
        for img in tqdm(imgs):
            im = cv2.imread(os.path.join(image_path, img))
            self.videoWriter.write(im)
        self.videoWriter.release()
    