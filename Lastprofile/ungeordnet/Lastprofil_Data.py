import pandas as pd
import numpy as np

class Data():
    def __init__(self):
        None
    def __call__ (self):
        # Data1 = pd.read_excel("RDE_Normal_ungeordnet.xlsx", usecols=['time in s', 'speed in m/s', 'a in m/s^2'])
        # Data2 = pd.read_excel("RDE_Sport_ungeordnet.xlsx", usecols=['time in s', 'speed in m/s', 'a in m/s^2'])
        # Data1 = Data1[::10]
        # Data2 = Data2[::10]
        # Data1.to_excel("RDE_Normal.xlsx", index=False)
        # Data2.to_excel("RDE_Sport.xlsx", index=False)
        # print('ende')
        Data3 = pd.read_csv("NEDC.csv")
        Data3.to_excel("NEDC.xlsx", index=False)
if __name__ == '__main__':
    gainData = Data()
    gainData()
    print('ende')