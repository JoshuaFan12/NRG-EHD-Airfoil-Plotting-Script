import pandas as pd
# import numpy as np
# import ast
import os
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter import filedialog
from datetime import datetime
from main import *
from avger import *
import matplotlib as mpl

mpl.rc('font', family='Times New Roman')  # The default font that is used in all plots

# HALF SPAN? Uncomment the appropriate line
#HALF_SPAN = 'Suction'
# HALF_SPAN = 'Pressure'
HALF_SPAN = 'Full_SPAN'

CUSTOM_LABS = False  # custom labels?
labs = ['Baseline', 'Plasma on', '10kV DC']

CUSTOM_TITLE = False # append custom title? 'C_[] vs Alpha' + 
cust_title = ' w/ 30kV 4kHz AC'


def avger(paths):
    df = pd.DataFrame(pd.read_csv(paths + '/DEFAULT_EU.csv'))
    sums = {}
    average = {}
    std = {}
    alpha = df['Alpha (deg)']
    for i in range(len(alpha)):
        angle = round(alpha[i])
        if angle not in sums:
            sums[angle] = [[df['C_D'][i]], [df['C_L'][i]], [df['C_m'][i]]]
        else:
            sums[angle] = [sums[angle][0] + [df['C_D'][i]], sums[angle][1] + [df['C_L'][i]],
                           sums[angle][2] + [df['C_m'][i]]]
    for key in sums.keys():
        average[key] = [stat.mean(sums[key][i]) for i in range(3)]
        std[key] = [calc_std(sums, key, i) for i in range(3)]
    keys = list(average.keys())
    keys.sort()
    output = pd.DataFrame(
        {
            'Alpha (deg)': keys,
            'C_D': [average[key][0] for key in keys],
            'C_L': [average[key][1] for key in keys],
            'C_m': [average[key][2] for key in keys],
            'stdC_D': [std[key][0] for key in keys],
            'stdC_L': [std[key][1] for key in keys],
            'stdC_m': [std[key][2] for key in keys]
        }
    )
    output.to_csv(paths + '/DEFAULT_EU_AVG.csv')


def filepaths(paths):
    lpath = []
    for path in paths:
        if path != 'None':
            if not os.path.exists(os.path.join(path, 'DEFAULT_EU_AVG.csv')):
                avger(path)
            lpath.append(os.path.join(path, 'DEFAULT_EU_AVG.csv'))
    return lpath


#
#
# def frames(lpath):
#     df_arr = []
#     for path in lpath:
#         df_arr.append(pd.DataFrame(pd.read_csv(path)))
#     return df_arr
#
#
# def splitter(df_arr, FILE_PATH):
#     asc_S_arr = []
#     des_S_arr = []
#     asc_P_arr = []
#     des_P_arr = []
#     for ind, df in enumerate(df_arr):
#
#         # Ascending (Suction Side)
#
#         low = df['Alpha (deg)'].idxmin()
#         mini = df['Alpha (deg)'].min()
#         df_asc_S = df.iloc[:low + 1].copy()
#         if not df_asc_S['Alpha (deg)'].is_monotonic_decreasing:
#             raise Exception(
#                 f'Double check {FILE_PATH[ind]} csv file, unusual angles of attack detected between 0 and {mini} degrees')
#
#         # Descending (Suction Side)
#         middle = -2
#         for i in range(len(df['Alpha (deg)'][low:])):
#             if round(df['Alpha (deg)'][low + i]) == 0:
#                 middle = low + i
#                 break
#         df_des_S = df.iloc[low:middle + 1].copy()
#         if not df_des_S['Alpha (deg)'].is_monotonic_increasing:
#             raise Exception(
#                 f'Double check {FILE_PATH[ind]} csv file, unusual angles of attack detected between {mini} and 0 degrees')
#
#         if middle > -2 and middle < len(df['Alpha (deg)'] - 1):
#             # Ascending (Pressure Side)
#
#             high = df['Alpha (deg)'].idxmax()
#             maxi = df['Alpha (deg)'].max()
#             df_asc_P = df.iloc[middle:high + 1].copy()
#             if not df_asc_P['Alpha (deg)'].is_monotonic_increasing:
#                 print(df_asc_P)
#                 raise Exception(
#                     f'Double check {FILE_PATH[ind]} csv file, unusual angles of attack detected between 0 and {maxi} degrees')
#
#             # Descending (Pressure Side)
#
#             df_des_P = df.iloc[high:].copy()
#             if not df_des_P['Alpha (deg)'].is_monotonic_decreasing:
#                 raise Exception(
#                     f'Double check {FILE_PATH[ind]} csv file, unusual angles of attack detected between {maxi} and 0 degrees')
#         else:
#             df_asc_P = None
#             df_des_P = None
#
#         asc_S_arr.append(df_asc_S)
#         des_S_arr.append(df_des_S)
#         asc_P_arr.append(df_asc_P)
#         des_P_arr.append(df_des_P)
#     return [asc_S_arr, des_S_arr, asc_P_arr, des_P_arr]
#
#
# def absol(df):
#     df['Alpha (deg)'] = -1 * (df['Alpha (deg)'])
#     df['C_L'] = -1 * (df['C_L'])
#     # df['C_m'] = -1*df['C_m']
#
#
# def unpack(string):
#     string_arr = string[2:-2].split('\'')
#
#     return [dir for dir in string_arr if dir != ', ']


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

    FILE_PATH = '/'.join(paths[0].split('/')[:-1])
    labels = []
    windspeed = ''
    for directory in paths[0:]:
        # windspeed = directory.split('/')[-2]
        windspeed = directory.split('/')[-3]
        # labels.append(directory.split('/')[-1])
        labels.append(windspeed + ' ' + directory.split('/')[-1])
    if CUSTOM_LABS:
        labels = labs
    DATA = filepaths(paths)

    df_arr = frames(DATA)

    for df in df_arr:
        absol(df)

    icons = ['k-', 'bo--', 'rs--', 'gx--', 'cp--', 'mP--', 'yd--', 'h--', '--', '--', '--', '--', '--', '--', '--',
             '--']
    direction = ['Ascending', 'Descending', 'Ascending', 'Descending']
    sides = ['Suction', 'Suction', 'Pressure', 'Pressure']
    coeff = ['C_D', 'C_L', 'C_m']
    now = datetime.now().strftime('%Y_%m_%d %H %M')
    os.mkdir(os.path.join(FILE_PATH, now))
    for coefficient in coeff:
        location = 'lower right'
        if coefficient == 'C_D':
            location = 'upper center'
        plt.figure(figsize=(10, 8))
        plt.grid(linestyle='--', linewidth=1.2)
        plt.tick_params(labelright=True, right=True, which='both', labelsize=18, direction='in', length=10, width=3)
        for i, dfs in enumerate(df_arr):
            # plt.plot(dfs["Alpha (deg)"], dfs[coefficient], icons[i], label=labels[i])
            if HALF_SPAN == 'Suction':
                dfs = dfs.loc[dfs["Alpha (deg)"] > -0.5]
            if HALF_SPAN == 'Pressure':
                dfs = dfs.loc[dfs["Alpha (deg)"] < 0.5]
            plt.errorbar(dfs["Alpha (deg)"], dfs[coefficient], fmt=icons[i], label=labels[i],
                         yerr=dfs['std' + coefficient] / 2, capsize=3, markersize=10)
            plt.legend(loc=location, fontsize=15)
            df_arr[i] = dfs
        plt.xlabel('Angle of Attack (deg)', fontsize=18)
        plt.ylabel(f'${coefficient}$', fontsize=20)
        title = f'${coefficient}$ vs AoA'
        if CUSTOM_TITLE:
            title += cust_title
        plt.title(title, fontsize=30, weight="bold")
        title = f'${coefficient}$ vs AoA'
        plt.savefig(os.path.join(FILE_PATH, now, title), bbox_inches="tight")

    if HALF_SPAN == 'Suction':
        for i in range(len(df_arr)):
            df_arr[i] = df_arr[i].iloc[::-1].reset_index(drop=True)
    for i in reversed(range(len(df_arr))):
        # df_arr[i]['stdC_D'] = (df_arr[i]['stdC_D']**2 + df_arr[0]['stdC_D']**2)**.5 / df_arr[0]['C_D']
        # df_arr[i]['stdC_L'] = (df_arr[i]['stdC_L']**2 + df_arr[0]['stdC_L']**2)**.5 / df_arr[0]['C_L']
        # df_arr[i]['stdC_m'] = (df_arr[i]['stdC_m']**2 + df_arr[0]['stdC_m']**2)**.5 / df_arr[0]['C_m']
        df_arr[i]['stdC_D'] = df_arr[i]['stdC_D']  # / df_arr[0]['C_D']
        df_arr[i]['stdC_L'] = df_arr[i]['stdC_L']  # / df_arr[0]['C_L']
        df_arr[i]['stdC_m'] = df_arr[i]['stdC_m']  # / df_arr[0]['C_m']
        df_arr[i]['C_D'] = (df_arr[i]['C_D'] - df_arr[0]['C_D'])  # / df_arr[0]['C_D']

        df_arr[i]['C_L'] = (df_arr[i]['C_L'] - df_arr[0]['C_L'])  # / df_arr[0]['C_L']
        df_arr[i]['C_m'] = (df_arr[i]['C_m'] - df_arr[0]['C_m'])  # / df_arr[0]['C_m']

    for coefficient in coeff:
        plt.figure(figsize=(12, 8))
        plt.grid(linestyle='--')
        plt.tick_params(labelright=True, right=True, which='both')
        for i, dfs in enumerate(df_arr):
            # plt.plot(dfs["Alpha (deg)"], dfs[coefficient], icons[i], label=labels[i])
            if i == 0:
                plt.errorbar(dfs["Alpha (deg)"], dfs[coefficient], fmt=icons[i], label=labels[i],
                             yerr=0, capsize=3)
            else:
                plt.errorbar(dfs["Alpha (deg)"], dfs[coefficient], fmt=icons[i], label=labels[i],
                             yerr=dfs['std' + coefficient] / 2, capsize=3)
            plt.legend(loc='lower right')
        plt.xlabel('Angle of Attack (deg)')
        plt.ylabel(f'$\Delta {coefficient}$')
        title = f'$\Delta {coefficient}$ vs AoA'
        # plt.ylabel(f'Normalized $\Delta {coefficient}$')
        # title = f'Normalized $\Delta {coefficient}$ vs AoA'
        plt.title(title)
        plt.minorticks_off()

        # if coefficient == 'C_L' or coefficient == 'C_m':
        #     mini = 0
        #     maxi = 0
        #     for i, df in enumerate(df_arr):
        #         if i == 0:
        #             continue
        #         mini = min(min(df[coefficient]), mini)
        #         maxi = max(max(df[coefficient]), maxi)
        #     if maxi > 1.0:
        #         maxi = 1.0
        #         plt.ylim(mini, maxi)
        #     if mini < -1.0:
        #         mini = -1.0
        #         plt.ylim(mini, maxi)
        #     plt.yticks(np.arange(round(mini*11)/10, maxi * 1.1, 0.1))
        # else:
        #     plt.minorticks_on()
        plt.savefig(os.path.join(FILE_PATH, now, title.replace('\\', '')))
