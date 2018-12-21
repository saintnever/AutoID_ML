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


def feature_extraction_reimag(df_data, win, step):
    df_data['Amp'] = 10 ** ((df_data['RSSI'] + 60) / 10)
    z = df_data['Amp'] * np.exp(1j * df_data['Phase'] * np.pi / 180)
    df_data['re'] = np.real(z)
    df_data['imag'] = np.imag(z)

    win = timedelta(seconds=win)
    step = timedelta(seconds=step)
    # xFrame = [[] for _ in df_data['EPC'].unique()]
    xFrame = list()
    yFrame = list()
    df_data = df_data[df_data['pos'] == 0]
    for state in df_data['state'].unique():
        print('state is {}'.format(state))
        df_state = df_data[df_data['state'] == state]
        timeStart = df_state['Time'].min()
        timeEnd = df_state['Time'].max()
        time = timeStart
        while time < timeEnd:
            df_frame = df_state[(df_state['Time'] >= time) & (df_state['Time'] < time + win)]
            # df_frame = df_frame.fillna(0)
            tagFrame_re = list()
            tagFrame_imag = list()
            print(time)
            for i, tag in enumerate(df_state['EPC'].unique()):
                # print('tag is {}'.format(tag))
                df_frame = df_frame[df_frame['EPC'] == tag]
                if len(df_frame.index) == 0:
                    tagFrame_re.append(0)
                    tagFrame_imag.append(0)
                else:
                    tagFrame_re.append(np.nanmean(df_frame['RSSI'].values))
                    tagFrame_imag.append(np.nanmean(df_frame['Phase'].values))
                # xFrame[i].append([np.nanmean(df_frame['re'].values), np.nanmean(df_frame['imag'].values)])
            time += step
            xFrame.append([[tagFrame_re], [tagFrame_imag]])
            yFrame.append(state)
    return xFrame, yFrame


def feature_extraction_rssiphase(df_data, win, step):
    win = timedelta(seconds=win)
    step = timedelta(seconds=step)
    # xFrame = [[] for _ in df_data['EPC'].unique()]
    xFrame = list()
    yFrame = list()
    for pos in df_data['pos'].unique():
        df_pos = df_data[df_data['pos'] == pos]
        for state in df_pos['state'].unique():
            print('state is {}'.format(state))
            df_state = df_pos[df_pos['state'] == state]
            df_state['RSSI'] = (df_state['RSSI'] - df_state['RSSI'].mean())/df_state['RSSI'].std()
            df_state['Phase'] = (df_state['Phase'] - df_state['Phase'].mean())/df_state['Phase'].std()
            timeStart = df_state.index[0]
            timeEnd = df_state.index[-1]
            time = timeStart
            while time < timeEnd:
                # df_frame = df_frame.fillna(0)
                tagFrame_re = list()
                tagFrame_imag = list()
                print(time)
                for i, tag in enumerate(df_data['EPC'].unique()):
                    # print('tag is {}'.format(tag))
                    df_frame = df_state[df_state['EPC'] == tag]
                    df_frame = df_frame.loc[time:time+win, :]
                    if len(df_frame.index) == 0:
                        tagFrame_re.append(0)
                        tagFrame_imag.append(0)
                    else:
                        tagFrame_re.append(np.nanmean(df_frame['RSSI'].values))
                        tagFrame_imag.append(np.nanmean(df_frame['Phase'].values))
                    # xFrame[i].append([np.nanmean(df_frame['re'].values), np.nanmean(df_frame['imag'].values)])
                time += step
                xFrame.append([[tagFrame_re], [tagFrame_imag]])
                yFrame.append(state + 3*pos)
    return np.array(xFrame), np.array(yFrame)


def cal_dim(dim_in, dim_kernel, dim_padding, dim_stride):
    assert dim_in.shape == dim_kernel.shape == dim_padding.shape == dim_stride.shape
    dim_out = np.zeros(dim_in.shape)
    for i, dim in enumerate(dim_in):
        dim_out[i] = np.floor((dim + 2 * dim_padding[i] - (dim_kernel[i] - 1) - 1) / dim_stride[i] + 1)
    return dim_out


