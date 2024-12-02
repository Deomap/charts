from constants import BINANCE_COL_NAMES
from binance_hist import *
import matplotlib.pyplot as plt


df = pd.read_csv('btc_usdt_1d', sep='|', names=BINANCE_COL_NAMES, header=None)


def similar_periods():
    comp_params = {'pct_shift':0.5, 'body_l_h':1, 'way': 0,}
    period = 3
    start = 2300
    end = 2611

    ind_period = ['pct_shift', 'body_l_h', 'way']
    ind_b = ['index1', 'date1', 'index2', 'date2']

    dict_res = {}
    dates = []
    c = []
    for i in range(start, end + 1 - period + 1):
        df_period = pd.DataFrame(columns=ind_period)
        date = ''
        for j in range(period):
            if i == start or j == period - 1:
                r = candle_expand_info(df.iloc[[i + j]])
                c.append(r)
            else:
                r = c[j]
            if j == 0: dates.append(r.date)
            df_period.loc[i + j] = [r.pct_shift, r.body_l_h, r.way]
        del(c[0])
        dict_res[i] = df_period
        print(f'\r', i, end, end='') ###
    res = pd.concat(dict_res)

    print() ###

    nl = len(res) // period
    rc = pd.DataFrame(columns=ind_b)
    for i in range(start, start + nl - 1):
        p1 = res.loc[(i, )]
        for j in range(i + 1, start + nl):
            p2 = res.loc[(j, )]
            diff = abs(p1 - p2.values)
            if ((diff.pct_shift <= comp_params['pct_shift']).all()
                    and (diff.body_l_h <= comp_params['body_l_h']).all()
                    and (diff.way == comp_params['way'])).all():
                i1 = p1.index[0]
                i2 = p2.index[0]
                d1 = ts_to_datetime(df.ts[i1])
                d2 = ts_to_datetime(df.ts[i2])
                rc.loc[len(rc)] = [i1, d1, i2, d2]
        print(f'\r', i, start + nl - 1, end='') ###
    print() ###
    print(rc)


similar_periods()


#########################################################################


def x():
    a = all()
    b = any()


def similar_candles():
    pct1 = pd.Series()
    pct2 = pd.Series()
    start = 2610
    end = 2611
    for i in range(start, end + 1):
        r1 = df.iloc[[i]]
        r1s = candle_expand_info(r1)
        for j in range(i, end + 1):
            if i == j: continue
            r2 = df.iloc[[j]]
            r2s = candle_expand_info(r2)
            if r2s.way != r1s.way: continue
            pct1[f'{i}_{j}'] = abs(r1s.pct_shift - r2s.pct_shift)
            pct2[f'{i}_{j}'] = abs(r1s.body_l_h - r2s.body_l_h)
            print('\r', i, j, end='')
    print()
    for i in range(len(pct2)):
        if pct1.iloc[i] < 0.1 and pct2.iloc[i] < 0.2:
            ind = pct1.index[i]
            ind1 = int(ind.split('_')[0])
            ind2 = int(ind.split('_')[1])
            print(ts_to_datetime(df.ts[ind1]), ts_to_datetime(df.ts[ind2]))


def plot_volumes():
    x = pd.Series([_ for _ in df.index])
    y = pd.Series()
    yy = []
    for i in range(len(df)):
        b = candle_expand_info(df.iloc[[i]])
        yy.append(b.buy_pct)
    y = pd.Series(yy)
    print(y)
    plt.style.use('ggplot')
    y.plot(kind='bar', figsize=(13, 7))
    plt.show()


def free_candles():
    a = [1503014400, 420, 2403, 28, 1529, 1, 1, 1, 1, 10]
    c = [0, 93977.12, 94612.64, 93053.25, 93065.20, 7304.1, 1, 1, 1, 100]
    b = [0, 12120, 14502, 11024, 11030, 12, 1, 1, 1, 100]

    a = [37228.45607999999, 49.9153, 0, 0.1667, 0.000075, 1286.899,]
    b = [44461.48950999995, 47.2623, 0, 1.0066, 0.000068, 386.5955,]