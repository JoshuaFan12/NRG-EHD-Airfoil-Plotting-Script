# SOP:
# When running code (green arrow top right), select baseline folder first, then the tests folders in the popup window.
# Hit 'cancel' instead when you are done choosing folders.

import pandas as pd
import os
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter import filedialog
from datetime import datetime

def filepaths(paths):
    lpath = []
    for path in paths:
        if path != 'None':
            lpath.append(os.path.join(path, 'DEFAULT_EU.csv'))
    return lpath


def frames(lpath):
    df_arr = []
    for path in lpath:
        df_arr.append(pd.DataFrame(pd.read_csv(path)))
    return df_arr


def splitter(df_arr, FILE_PATH):
    asc_S_arr = []
    des_S_arr = []
    asc_P_arr = []
    des_P_arr = []
    for ind, df in enumerate(df_arr):

        # Ascending (Suction Side)

        low = df['Alpha (deg)'].idxmin()
        mini = df['Alpha (deg)'].min()
        df_asc_S = df.iloc[:low + 1].copy()
        if not df_asc_S['Alpha (deg)'].is_monotonic_decreasing:
            raise Exception(
                f'Double check {FILE_PATH[ind]} csv file, unusual angles of attack detected between 0 and {mini} degrees')

        # Descending (Suction Side)
        middle = -2
        for i in range(len(df['Alpha (deg)'][low:])):
            if round(df['Alpha (deg)'][low + i]) == 0:
                middle = low + i
                break
        df_des_S = df.iloc[low:middle + 1].copy()
        if not df_des_S['Alpha (deg)'].is_monotonic_increasing:
            raise Exception(
                f'Double check {FILE_PATH[ind]} csv file, unusual angles of attack detected between {mini} and 0 degrees')

        if middle > -2 and middle < len(df['Alpha (deg)']-1):
            # Ascending (Pressure Side)

            high = df['Alpha (deg)'].idxmax()
            maxi = df['Alpha (deg)'].max()
            df_asc_P = df.iloc[middle:high + 1].copy()
            if not df_asc_P['Alpha (deg)'].is_monotonic_increasing:
                print(df_asc_P)
                raise Exception(
                    f'Double check {FILE_PATH[ind]} csv file, unusual angles of attack detected between 0 and {maxi} degrees')

            # Descending (Pressure Side)

            df_des_P = df.iloc[high:].copy()
            if not df_des_P['Alpha (deg)'].is_monotonic_decreasing:
                raise Exception(
                    f'Double check {FILE_PATH[ind]} csv file, unusual angles of attack detected between {maxi} and 0 degrees')
        else:
            df_asc_P = None
            df_des_P = None

        asc_S_arr.append(df_asc_S)
        des_S_arr.append(df_des_S)
        asc_P_arr.append(df_asc_P)
        des_P_arr.append(df_des_P)
    return [asc_S_arr, des_S_arr, asc_P_arr, des_P_arr]


def absol(df):
    df['Alpha (deg)'] = -1 * (df['Alpha (deg)'])
    df['C_L'] = -1*(df['C_L'])
    # df['C_m'] = -1*df['C_m']


def unpack(string):
    string_arr = string[2:-2].split('\'')

    return [dir for dir in string_arr if dir != ', ']


if __name__ == '__main__':
    os.chdir('/')
    root = Tk()
    root.withdraw()
    paths = [filedialog.askdirectory(title='Baseline Folder')]
    while True:
        dir = filedialog.askdirectory(title='Next Test Folder')
        if dir == '':
            break
        paths.append(dir)
    # if input('Select Folders? (Y/N) ').lower() == 'y':
    #     root = Tk()
    #     root.withdraw()
    #     paths = [filedialog.askdirectory(title='Baseline Folder')]
    #     while True:
    #         dir = filedialog.askdirectory(title='Next Test Folder')
    #         if dir == '':
    #             break
    #         paths.append(dir)
    # else:
    #     paths = unpack(input('Copy + Paste Path Here: '))
    # print(paths)

    FILE_PATH = '/'.join(paths[0].split('/')[:-1])
    labels = []
    windspeed = ''
    for directory in paths[0:]:
        windspeed = directory.split('/')[-2]
        labels.append(windspeed + ' ' + directory.split('/')[-1])

    DATA = filepaths(paths)

    df_arr = frames(DATA)

    split_arrs = splitter(df_arr, DATA)

    for arrs in split_arrs:
        for df in arrs:
            if type(df) != type(None):
                absol(df)
    for df in df_arr:
        absol(df)

    icons = ['k-', 'bo--', 'rs--', 'gx--', 'cp--', 'mP--', 'yd--', 'h--', '--', '--', '--', '--', '--', '--', '--', '--']
    direction = ['Ascending', 'Descending', 'Ascending', 'Descending']
    sides = ['Suction', 'Suction', 'Pressure', 'Pressure']
    coeff = ['C_D', 'C_L', 'C_m']
    now = datetime.now().strftime('%Y_%m_%d %H %M')
    os.mkdir(os.path.join(FILE_PATH, now))

    for coefficient in coeff:
        for i, arr in enumerate(split_arrs):
            plotit = False
            plt.figure(figsize=(12, 8))

            for j, df in enumerate(arr):
                if df is None: continue
                plotit = True
                plt.plot(df['Alpha (deg)'], df[coefficient], icons[j], label=labels[j])
            if plotit:
                plt.grid(linestyle='--')
                plt.legend(loc='lower right')
                plt.xlabel('Angle of Attack (deg)')
                plt.ylabel(f'${coefficient}$')
                title = f'{windspeed} {direction[i]} ${coefficient}$ vs AoA({sides[i]} side)'
                plt.title(title)
                plt.savefig(os.path.join(FILE_PATH, now, title))
            # if arr[3] is None:
            #     continue
            # alpha = [arr[0]['Alpha (deg)'][i] + arr[1]['Alpha (deg)'][-i] for i in range(len(arr[0]))]
            # a_pressure = [arr[2]['Alpha (deg)'][i] + arr[3]['Alpha (deg)'][-i] for i in range(len(arr[0]))]
            # alpha += a_pressure



        plt.figure(figsize=(12, 8))
        plt.grid(linestyle='--')
        for i, dfs in enumerate(df_arr):
            plt.plot(dfs["Alpha (deg)"], dfs[coefficient], icons[i], label=labels[i])
        plt.legend(loc='lower right')
        plt.xlabel('Angle of Attack (deg)')
        plt.ylabel(f'${coefficient}$')
        title = f'${coefficient}$ vs AoA'
        plt.title(title)
        plt.savefig(os.path.join(FILE_PATH, now, title))

