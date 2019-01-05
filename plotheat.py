import os
import numpy as np
import csv
import matplotlib.pyplot as plt
import time
import threading
import pickle

def drawheatmap(starttime,endtime):
    data=[]
    score=[]
    for i in range(0,6):
        tmp = []
        tmp_i = []
        for j in range(0,5):
            tmp.append("")
            tmp_i.append(0)
        data.append(tmp)
        score.append(tmp_i)

    data[1][0] = "E20000193907010913105176"
    data[3][0] = "E2000019390701391310743D"
    data[4][0] = "E200001939070129131062B4"
    data[0][1] = "E20000193907004213101285"
    data[1][1] = "E200001939070030131007FF"
    data[2][1] = "E200001939070028131007FE"
    data[4][1] = "E200001939070029131009B6"
    data[5][1] = "E200001939070027131009B5"
    data[3][2] = "E200001939070157131085BE"
    data[5][2] = "E20000193907014513107440"
    data[1][3] = "E2000019390700821310357D"
    data[2][3] = "E2000019390700701310266F"
    data[3][3] = "E2000019390700681310266E"
    data[4][3] = "E200001939070079131030EB"
    data[5][3] = "E20000193907006913102966"
    data[1][4] = "E20000193907006213101F63"
    data[2][4] = "E20000193907005113101B4D"
    data[3][4] = "E200001939070049131014D4"
    data[4][4] = "E20000193907006113102226"
    data[5][4] = "E200001939070050131018B5"
    # # lamp
    # data[0][5] = "E20000193907012013105670"
    # # medicine
    # data[0][6] = "E20000195919016317508F2D"
    # # cup
    # data[0][7] = "E200001959190172175092DA"
    # data[1][7] = "E200001959190171175097E5"
    # # PC
    # data[0][8] = "E200001959190170175092D9"
    # # book
    # data[0][9] = "E20000195919016717508F2F"
    # data[1][9] = "E20000195919016817508A1C"
    # data[2][9] = "E200001959190170175092D9"
    # # drawer
    # data[0][10] = "E20000195919016417508A1A"
    # data[1][10] = "E20000195919016517508F2E"
    # data[2][10] = "E20000195919016217508A19"
    # data[3][10] = "E2000019591901601750815C"
    datadic={}
    length = 0
    for i in range(0,5):
            for j in range(0,6):
                if not data[j][i] == "":
                    picklefilename = data[j][i]+'.pkl'
                    pkl_file = open("./data/"+picklefilename, 'rb')
                    print(data[j][i])
                    datadic[data[j][i]] = pickle.load(pkl_file)
                    length = len(datadic[data[j][i]])

    datalist=[]
    for k in range(starttime,endtime):
        if k >= length:
            print("sorry, it is out of range!")
            return
        score=[]
        for i in range(0,6):
            tmp_i = []
            for j in range(0,5):
                tmp_i.append(0)
            score.append(tmp_i)
        for i in range(0,5):
            for j in range(0,6):
                if not data[j][i] == "":
                    score[j][i] = datadic[data[j][i]][k][1]
        datalist.append(score)

    # a blank one, used to draw colorbar
    score=[]
    for i in range(0,6):
        tmp_i = []
        for j in range(0,5):
            tmp_i.append(0)
        score.append(tmp_i)
    plt.figure(1)
    plt.imshow(score, cmap=plt.cm.hot,vmin=-85, vmax=-40)
    plt.colorbar()
    for key in datalist:
        plt.imshow(key, cmap=plt.cm.hot,vmin=-85, vmax=-40)
        plt.pause(0.25)
    plt.show()