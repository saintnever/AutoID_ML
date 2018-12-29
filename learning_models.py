import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torch.utils import data


class Dataset(data.Dataset):
    # 'Characterizes a dataset for PyTorch'
    def __init__(self, list_IDs, feature, labels):
        # 'Initialization'
        self.labels = labels
        self.list_IDs = list_IDs
        self.features = feature

    def __len__(self):
        # 'Denotes the total number of samples'
        return len(self.list_IDs)

    def __getitem__(self, index):
        # 'Generates one sample of data'
        # Select sample
        ID = self.list_IDs[index]

        # Load data and get label
        X = self.features[ID]
        y = self.labels[ID]

        return X, y


# 2D CNN model for drawer_learning.py, with interpolation
class ConvNet(nn.Module):
    def __init__(self, num_classes=3):
        super(ConvNet, self).__init__()
        self.layer1 = nn.Sequential(
            # nn.BatchNorm2d(2),
            nn.Conv2d(1, 16, kernel_size=2, stride=1, padding=1),
            # nn.BatchNorm2d(16, affine=False),
            nn.ReLU())
        # nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=2, stride=1, padding=1),
            # nn.BatchNorm2d(32, affine=False),
            nn.ReLU())
        # self.layer3 = nn.Sequential(
        #     nn.Conv2d(32, 64, kernel_size=2, stride=1, padding=1),
        #     # nn.BatchNorm2d(32, affine=False),
        #     nn.ReLU())
        # nn.MaxPool2d(kernel_size=2, stride=2))
        # self.fc1 = nn.Linear(1 * 256 * 32, num_classes)
        # self.fc1 = nn.Linear(7*7*64, 7*7*64)
        self.fc2 = nn.Linear(6*6*32, num_classes)

    def forward(self, x):
        out = self.layer1(x)
        # print(out.shape)
        out = self.layer2(out)
        # print(out.shape)
        # out = self.layer3(out)
        out = out.reshape(out.size(0), -1)
        # print(out.shape)
        # out = self.fc1(out)
        out = self.fc2(out)
        return out


# 2D CNN model for drawer_learning_sliding.py, without interpolation
class ConvNet_nointerp(nn.Module):
    def __init__(self, num_classes=6):
        super(ConvNet_nointerp, self).__init__()
        self.layer1 = nn.Sequential(
            # nn.BatchNorm2d(2),
            nn.Conv2d(2, 16, kernel_size=2, stride=1, padding=1),
            # nn.BatchNorm2d(16, affine=False),
            nn.ReLU())
        # nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=2, stride=1, padding=1),
            # nn.BatchNorm2d(32, affine=False),
            nn.ReLU())
        self.layer3 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=2, stride=1, padding=1),
            # nn.BatchNorm2d(32, affine=False),
            nn.ReLU())
        # nn.MaxPool2d(kernel_size=2, stride=2))
        # self.fc1 = nn.Linear(1 * 256 * 32, num_classes)
        # self.fc1 = nn.Linear(7*7*64, 7*7*64)
        self.fc2 = nn.Linear(357*64, num_classes)

    def forward(self, x):
        out = self.layer1(x)
        # print(out.shape)
        out = self.layer2(out)
        # print(out.shape)
        out = self.layer3(out)
        # print(out.shape)
        out = out.reshape(out.size(0), -1)
        # print(out.shape)
        # out = self.fc1(out)
        out = self.fc2(out)
        return out