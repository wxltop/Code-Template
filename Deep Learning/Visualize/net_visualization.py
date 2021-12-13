import hiddenlayer as hl
from torch import nn
import torch
from torchviz import make_dot


#*********************** hidden layer *************************
class ConvNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.AvgPool2d(kernel_size=2, stride=2)
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.AvgPool2d(kernel_size=2, stride=2)
        )
        self.fc = nn.Sequential(
            nn.Linear(in_features=32*7*7, out_features=128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU()
        )
        self.out = nn.Linear(64, 10)
    
    def forward(self, X):
        H1 = self.conv1(X)
        H2 = self.conv2(H1)
        H2 = H2.view(H2.size(0), -1)
        H3 = self.fc(H2)
        output = self.out(H3)
        return output

net = ConvNet()
# print(net)
x = torch.randn(1, 1, 28, 28).requires_grad_(True)
y = net(x)
viz = make_dot(y, params=dict(list(net.named_parameters()) + [('x', x)]))
# 将viz保存为图片
viz.format = 'png'  # 保存的格式
viz.directory = 'img/myvis'  # 保存的路径
viz.view()  # 自动在当前文件夹生成相应目录和文件
#*******************************************************