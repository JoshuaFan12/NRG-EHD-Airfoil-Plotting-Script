import pandas as pd
import os
import statistics as stat
from tkinter import Tk
from tkinter import filedialog


def calc_std(sums, key, i):
    if len(sums[key][i]) > 1:
        return stat.stdev(sums[key][i])
    else:
        return 0


def calc_std2(sums, key, i):
    if len(sums[key][i]) > 1:
        return stat.stdev(sums[key][i])
    else:
        return sums[key][i][0]


if __name__ == '__main__':

    for i in range(20):
        os.chdir('/')
        root = Tk()
        root.withdraw()
        paths = filedialog.askdirectory(title='Folder 1')
        if paths == '':
            break
        df = pd.DataFrame(pd.read_csv(paths + '/DEFAULT_RAW_AVG.csv'))
        for j in range(8):
            os.chdir('/')
            root = Tk()
            root.withdraw()
            path = filedialog.askdirectory(title=f'Folder {j + 2}')
            if path == '':
                break
            df.append(pd.DataFrame(pd.read_csv(paths + '/DEFAULT_RAW_AVG.csv')))
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
