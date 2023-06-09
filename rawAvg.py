from main import *
from CONSTANTS import *


def filepaths(paths):
    lpath = []
    for path in paths:
        if path != 'None':
            lpath.append(os.path.join(path, 'DEFAULT_RAW.csv'))
    return lpath


def Q_Calc(df):
    df['Q (psf)'] = (df['Q (mA)'] - 4) / 16 * Q_max
    # df['stdQ'] = (df['Sigma Pressure (mA)']) / 16 * Q_max


def C_D_Calc(df):
    errdrag1 = (df['Sigma Drag 1 (mV/V)']) * drag1_cal_factor / (df['Q (psf)'] * span / 12 * chord / 12)
    errdrag2 = (df['Sigma Drag 2 (mV/V)']) * drag2_cal_factor / (df['Q (psf)'] * span / 12 * chord / 12)
    drag1 = (df['Drag 1 (mV/V)'] - df['WOZ Drag 1 (mV/V)']) * drag1_cal_factor / (
                df['Q (psf)'] * span / 12 * chord / 12)
    drag2 = (df['Drag 2 (mV/V)'] - df['WOZ Drag 2 (mV/V)']) * drag2_cal_factor / (
                df['Q (psf)'] * span / 12 * chord / 12)
    df['C_D'] = drag1 + drag2
    # df['stdC_D'] = (errdrag1 ** 2 + errdrag2 ** 2) ** .5


def C_Lm_Calc(df):
    errlift1 = (df['Sigma Lift 1 (mV/V)']) * lift1_cal_factor / (df['Q (psf)'] * span / 12 * chord / 12)
    errlift2 = (df['Sigma Lift 2 (mV/V)']) * lift2_cal_factor / (df['Q (psf)'] * span / 12 * chord / 12)
    errlift3 = (df['Sigma Lift 3 (mV/V)']) * lift3_cal_factor / (df['Q (psf)'] * span / 12 * chord / 12)
    errlift4 = (df['Sigma Lift 4 (mV/V)']) * lift4_cal_factor / (df['Q (psf)'] * span / 12 * chord / 12)
    lift1 = (df['Lift 1 (mV/V)'] - df['WOZ Lift 1 (mV/V)']) * lift1_cal_factor / (
                df['Q (psf)'] * span / 12 * chord / 12)
    lift2 = (df['Lift 2 (mV/V)'] - df['WOZ Lift 2 (mV/V)']) * lift2_cal_factor / (
                df['Q (psf)'] * span / 12 * chord / 12)
    lift3 = (df['Lift 3 (mV/V)'] - df['WOZ Lift 3 (mV/V)']) * lift3_cal_factor / (
                df['Q (psf)'] * span / 12 * chord / 12)
    lift4 = (df['Lift 4 (mV/V)'] - df['WOZ Lift 4 (mV/V)']) * lift4_cal_factor / (
                df['Q (psf)'] * span / 12 * chord / 12)
    df['C_L'] = lift1 + lift2 + lift3 + lift4
    # df['stdC_L'] = (errlift1 ** 2 + errlift2 ** 2 + errlift3 ** 2 + errlift4 ** 2) ** .5

    errmom1 = errlift1 * (FWD_moment_arm / 12) / (chord / 12)
    errmom2 = errlift2 * (FWD_moment_arm / 12) / (chord / 12)
    errmom3 = errlift3 * (AFT_moment_arm / 12) / (chord / 12)
    errmom4 = errlift4 * (AFT_moment_arm / 12) / (chord / 12)
    mom1 = lift1 * (FWD_moment_arm / 12) / (chord / 12)
    mom2 = lift2 * (FWD_moment_arm / 12) / (chord / 12)
    mom3 = lift3 * (AFT_moment_arm / 12) / (chord / 12)
    mom4 = lift4 * (AFT_moment_arm / 12) / (chord / 12)

    df['C_m'] = mom1 + mom2 - (mom3 + mom4)
    plt.plot(df['Alpha (deg)'], df['C_m'])
    plt.show()
    # df['stdC_m'] = (errmom1 ** 2 + errmom2 ** 2 + errmom3 ** 2 + errmom4 ** 2) ** .5


if __name__ == '__main__':
    for i in range(10):
        os.chdir('/')
        root = Tk()
        root.withdraw()
        paths = [filedialog.askdirectory(title='Baseline Folder')]
        if paths[0] == '':
            break
        lpath = filepaths(paths)
        df = frames(lpath)[0]
        Q_Calc(df)
        C_D_Calc(df)
        C_Lm_Calc(df)
        df.to_csv(paths[0] + '/DEFAULT_RAW_AVG.csv')
