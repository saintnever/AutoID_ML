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
from calibration import *
from learning_models import *

# Device configuration
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

try:
    # epc_mapping = pd.read_csv('bitid_mapping.csv')
    # rfids = epc_mapping[epc_mapping['type'] == 'rfid']
    # rfid_list = list(rfids['EPC'])
    # rfid_size = len(rfid_list)
    # bitids = epc_mapping[epc_mapping['type'] == 'bitid']
    # bitid_list = list(bitids['EPC'])
    # bitid_size = len(bitid_list)
    # bitid_drawer = bitids[bitids['location'] == 'drawer']['EPC'].values[0]
    #
    # df = pd.read_pickle('data_6trails_3people_cal.pkl')
    # for index in df.index:
    #     if type(df.loc[index, 'Time']) is str:
    #         df = df.drop(index=index)
    #         print(index, 'dropped')
    # df = df.set_index(df['Time']).sort_index()
    # ant_num = len(df['Ant'].unique())
    # time = df.index[100]
    # win = 2
    # step = 0.5
    # X = list()
    # y = list()
    # # get data for one frame
    # while time <= df.index[-1]:
    #     # init frame values rfid_size X ant_num
    #     frame_rssi = np.ones([rfid_size, ant_num]) * -100
    #     frame_phase = np.ones([rfid_size, ant_num]) * 0
    #     frame_y = list()
    #     df_frame = df.loc[time-timedelta(seconds=win):time, :]
    #     df_framey = df.loc[time-timedelta(seconds=5):time, :]
    #     time = time + timedelta(seconds=step)
    #     if len(df_framey.index) == 0:
    #         continue
    #     for tag in bitid_list:
    #         frame_y.append(tag in df_framey['EPC'].unique())
    #     print(time, frame_y)
    #     df_rfid = df_frame[df_frame['EPC'].isin(rfid_list)]
    #     df_rfid['RSSI'] = df_rfid['RSSI'].astype(float)
    #     df_rfid['Phase'] = df_rfid['Phase'].astype(float)
    #     df_rfid['Ant'] = df_rfid['Ant'].astype(int)
    #     rssi_pivot = df_rfid.pivot_table(values='RSSI', index='EPC', columns='Ant', aggfunc=np.mean)
    #     rssi_pivot = rssi_pivot.replace(np.nan, -100)
    #     phase_pivot = df_rfid.pivot_table(values='Phase', index='EPC', columns='Ant', aggfunc=np.mean)
    #     phase_pivot = phase_pivot.replace(np.nan, 0)
    #     # deal with missing antennas
    #     for i in range(1, ant_num+1):
    #         if i not in rssi_pivot.columns:
    #             rssi_pivot[i] = -100
    #             phase_pivot[i] = 0
    #     for tag in rssi_pivot.index:
    #         i = rfid_list.index(tag)
    #         frame_rssi[i] = rssi_pivot.loc[tag, :]
    #         frame_phase[i] = phase_pivot.loc[tag, :]
    #     X.append(np.array([frame_rssi, frame_phase]))
    #     y.append(frame_y)
    # with open("6trials_win2_step05_nointerpolation_multilabel.pkl", "wb") as file:
    #     pickle.dump({'feature': X, 'label': y}, file)

    # phase_calibrate('data_6trails_3people.csv', 'data_6trails_3people_cal.csv')
    # df = pd.read_csv('data_6trails_3people_cal.csv')
    # for index in df.index:
    #     try:
    #         print(df.loc[index, 'Time'])
    #         df.loc[index, 'Time'] = datetime.strptime(df.loc[index, 'Time'], "%Y-%m-%dT%H:%M:%S.%fZ")
    #     except ValueError:
    #         pass
    # df.reset_index().to_pickle('data_6trails_3people_cal.pkl')

    with open("6trials_win2_step05_nointerpolation_multilabel.pkl", "rb") as file:
        data_dict = pickle.load(file)
    X = data_dict['feature']
    y = data_dict['label']

    # Hyper parameters
    num_epochs = 10
    num_classes = 6
    batch_size = 32
    learning_rate = 0.0005

    full_set = Dataset(range(len(y)), torch.tensor(X), torch.tensor(y))
    train_size = int(0.8 * len(full_set))
    # dev_size = int((len(full_set) - train_size) / 2)
    test_size = len(full_set) - train_size
    train_set, dev_set = torch.utils.data.random_split(full_set, [train_size, test_size])

    # Data loader
    train_loader = torch.utils.data.DataLoader(dataset=train_set, batch_size=batch_size, shuffle=True)
    test_loader = torch.utils.data.DataLoader(dataset=dev_set, batch_size=batch_size, shuffle=False)

    model = ConvNet_nointerp(num_classes).to(device)

    # Loss and optimizer
    # criterion = nn.CrossEntropyLoss()
    criterion = nn.MultiLabelSoftMarginLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Train the model
    total_step = len(train_loader)
    correct = 0
    total = 0
    for epoch in range(num_epochs):
        for i, (features, labels) in enumerate(train_loader):
            features_gpu = features.to(device, dtype=torch.float)
            labels_gpu = labels.to(device, dtype=torch.float)
            # Forward pass
            outputs = model(features_gpu)
            loss = criterion(outputs, labels_gpu)
            # _, predicted = torch.max(outputs.data, dim=1)
            predicted = torch.sigmoid(outputs).data > 0.5
            total += labels.size(0)
            correct += (predicted == labels.to(device)).sum().item()/labels.size(1)
            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (i + 1) % batch_size == 10:
                print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'
                      .format(epoch + 1, num_epochs, i + 1, total_step, loss.item()))
    print('Training Accuracy of the model on the {} test features: {} %'.format(total, 100 * correct / total))

    # Test the model
    model.eval()  # eval mode (batchnorm uses moving mean/variance instead of mini-batch mean/variance)
    with torch.no_grad():
        correct = 0
        total = 0
        for features, labels in test_loader:
            features_gpu = features.to(device, dtype=torch.float)
            labels_gpu = labels.to(device, dtype=torch.float)
            outputs = model(features_gpu)
            # _, predicted = torch.max(outputs.data, dim=1)
            predicted = torch.sigmoid(outputs).data > 0.5
            total += labels.size(0)
            correct += (predicted == labels.to(device)).sum().item() / labels.size(1)

        print('Test Accuracy of the model on the {} test features: {} %'.format(total, 100 * correct / total))

except KeyboardInterrupt:
    print('Interrupted')
