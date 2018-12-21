import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torch.utils import data
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
from datetime import datetime, timedelta
import pickle
from drawer_utils import *
from sklearn import neighbors, svm
from sklearn.model_selection import cross_val_score, train_test_split

# Device configuration
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


# process data
# df_data = pd.read_csv('df_drawer.csv')
# for ind in df_data.index:
#     df_data.loc[ind, 'Time'] = datetime.strptime(df_data.loc[ind, 'Time'], "%Y-%m-%d %H:%M:%S.%f") + timedelta(hours=8)
# df_data.to_pickle('df_data.pkl')


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


# Hyper parameters
num_epochs = 8
num_classes = 6
batch_size = 32
learning_rate = 0.001


# Convolutional neural network (two convolutional layers)
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


try:
    # # load data
    # df_data = pd.read_pickle('df_data.pkl')
    # df_pivot_RSSIt = df_data.pivot_table(values='RSSI', index='EPC', columns=['pos', 'state'],
    #                                      aggfunc=np.nanmean)
    # df_pivot_PHASEt = df_data.pivot_table(values='Phase', index='EPC', columns=['pos', 'state'],
    #                                       aggfunc=np.nanmean)
    # df_data = df_data.dropna()
    # df_data['Time'] = [data.replace(microsecond=0) for data in df_data['Time']]
    # df_data = df_data.set_index(df_data['Time'])
    # dfs = pd.DataFrame()
    # for pos in df_data['pos'].unique():
    #     for state in df_data['state'].unique():
    #         df = df_data[(df_data['pos'] == pos) & (df_data['state'] == state)]
    #         for tag in df['EPC'].unique():
    #             print(pos, state, tag)
    #             df_tag = df[df['EPC'] == tag].loc[:, ['Phase', 'RSSI']]
    #             df_tag = df_tag[~df_tag.index.duplicated(keep='first')]
    #             df_tag = df_tag.reindex(pd.date_range(start=df.index.min(), end=df.index.max(), freq='0.5S'))
    #             df_tag = df_tag.interpolate(method='linear')
    #             df_tag['EPC'] = tag
    #             df_tag['pos'] = pos
    #             df_tag['state'] = state
    #             dfs = dfs.append(df_tag)
    # with open("dfs_interpolated_05s.pkl", "wb") as file:
    #     pickle.dump(dfs, file)
    # # feature extraction
    # with open("dfs_interpolated_05s.pkl", "rb") as file:
    #     df_data = pickle.load(file)
    # # # visulization
    # # df_pivot_RSSI = df_data.pivot_table(values='RSSI', index='EPC', columns=['pos', 'state'],
    # #                                     aggfunc=np.nanmean)
    # # df_pivot_PHASE = df_data.pivot_table(values='Phase', index='EPC', columns=['pos', 'state'],
    # #                                      aggfunc=np.nanmean)
    # xFrame, yFrame = feature_extraction_rssiphase(df_data, 2, 0.5)
    #
    # with open("full_set_win2_step05.pkl", "wb") as file:
    #     pickle.dump({'feature': xFrame, 'label': yFrame}, file)

    # train/test/dev split
    with open("full_set_win2_step05.pkl", "rb") as file:
        data_dict = pickle.load(file)
    xFrame = np.array(data_dict['feature'])
    xFrame = np.squeeze(np.array(xFrame))
    yFrame = np.array(data_dict['label'])

    X = list()
    y = list()
    for i, item in enumerate(xFrame):
        if ~np.isnan(np.sum(item)):
            X.append([np.array(item).reshape(4, 4)])
            y.append(yFrame[i])

    # SVM classifier
    # xFrame_flatten = np.array(xFrame).reshape(len(xFrame), -1)
    # xFrame_flatten[np.isnan(xFrame_flatten)] = 0
    # X_train, X_test, y_train, y_test = train_test_split(xFrame_flatten, yFrame, test_size=0.4, random_state=0)
    # clf = svm.SVC(kernel='rbf', gamma='scale', C=1).fit(X_train, y_train)
    # print(clf.score(X_test, y_test))

    # CNN
    full_set = Dataset(range(len(y)), torch.tensor(X), torch.tensor(y))
    train_size = int(0.8 * len(full_set))
    # dev_size = int((len(full_set) - train_size) / 2)
    test_size = len(full_set) - train_size
    train_set, dev_set = torch.utils.data.random_split(full_set, [train_size, test_size])

    # Data loader
    train_loader = torch.utils.data.DataLoader(dataset=train_set, batch_size=batch_size, shuffle=True)
    test_loader = torch.utils.data.DataLoader(dataset=dev_set, batch_size=batch_size, shuffle=False)

    model = ConvNet(num_classes).to(device)

    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Train the model
    total_step = len(train_loader)
    correct = 0
    total = 0
    for epoch in range(num_epochs):
        for i, (features, labels) in enumerate(train_loader):
            features = features.to(device, dtype=torch.float)
            labels = labels.to(device)
            # Forward pass
            outputs = model(features)
            loss = criterion(outputs, labels)
            _, predicted = torch.max(outputs.data, dim=1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (i + 1) % batch_size == 10:
                print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'
                      .format(epoch + 1, num_epochs, i + 1, total_step, loss.item()))
    print('Training Accuracy of the model on the {} test features: {} %'.format(total, 100 * correct / total))

    #
    # Test the model
    model.eval()  # eval mode (batchnorm uses moving mean/variance instead of mini-batch mean/variance)
    with torch.no_grad():
        correct = 0
        total = 0
        for features, labels in test_loader:
            features = features.to(device, dtype=torch.float)
            labels = labels.to(device)
            outputs = model(features)
            _, predicted = torch.max(outputs.data, dim=1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        print('Test Accuracy of the model on the {} test features: {} %'.format(total, 100 * correct / total))

    # # Save the model checkpoint
    # torch.save(model.state_dict(), 'model.ckpt')
except KeyboardInterrupt as e:
    print(e)
