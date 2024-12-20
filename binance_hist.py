from datetime import datetime, timezone, timedelta, tzinfo
import time
import pytz

import pandas as pd
import ssdeep

from colors import Colors as cf
from constants import BINANCE_COL_NAMES, TF_TICKS, DT_FMT


def tf_transform(new_tf: int | str, filename, ticks_base):

    print(f'\n> Transforming {str.upper("".join(filename.split("_")[:2]))} {ticks_base}t to {new_tf}{"" if isinstance(new_tf, str) else "t"}')

    # prepare dataset
    adj_tf = int((TF_TICKS[new_tf] if isinstance(new_tf, str) else new_tf) / ticks_base)
    df = pd.read_csv(filename, sep='|', names=BINANCE_COL_NAMES, header=None)
    df = df.drop(df[df.ts % ticks_base != 0].index)
    df.reset_index(inplace=True)
    adj_ts = df.ts / ticks_base

    # prepare loop
    n = len(df) # number or rows
    n_periods = (adj_ts[n - 1] - adj_ts[0]) // adj_tf # number of estimated periods (without errors)
    errors = 0
    complete = 0
    pos = 0 # active index position
    last_ts = adj_ts[n - 1]
    tf_limit = adj_tf - 1

    while True:
        if adj_ts[pos] + adj_tf >= last_ts - 1:
            break
        try:
            if (adj_ts[pos] % adj_tf != 0 or
                    adj_ts[pos + adj_tf - 1] - adj_ts[pos] != tf_limit):
                pos += 1
                continue

            df_part = df[pos : pos + adj_tf]
            df_part.reset_index(inplace=True)

            df_new = pd.DataFrame([[
                df_part.ts[0],
                df_part.o[0],
                max(df_part.h),
                min(df_part.l),
                df_part.c[adj_tf - 1],
                sum(df_part.v_b),
                sum(df_part.v_t_b_q),
                sum(df_part.v_t_b_b),
                sum(df_part.v_q),
                sum(df_part.nt),
            ]])

            df_new.to_csv(
                '_'.join(filename.split('_')[:2] +
                         [new_tf if isinstance(new_tf, str) else str(new_tf) + 't']),
                index=False,
                header=False,
                sep='|',
                mode='a',
            )

            complete += 1
            pos += adj_tf

            print(f'\r{cf.blue}{complete}{cf.endc} / {int(n_periods)} READY. '
                  f'({cf.bold}{round(complete / n_periods * 100, 2)}%{cf.endc})',
                  end='')

        except KeyError:
            errors += 1
            pos += 1

        except Exception as e:
            errors += 1

    print('\n========== complete ==========')
    print(f'{cf.fail}{errors}{cf.endc} ERRORS. '
          f'{cf.warn}{int(n_periods - complete - errors)}{cf.endc} MISSING.')


def candle_expand_info(row):
    row = row.squeeze()
    v_t_s_b = row.v_b - row.v_t_b_b
    v_t_s_q = row.v_q - row.v_t_b_q
    way = int((row.o - row.c) < 0)
    change = row.c / row.o - 1 if way else (1 - row.c / row.o)
    pct_high = row.h / row.c - 1 if way else row.h / row.o - 1
    pct_low = 1 - row.l / row.o if way else 1 - row.l / row.c

    extras = {
        'date': ts_to_datetime(row.ts),
        'v_t_s_b': v_t_s_b,
        'v_t_s_q': v_t_s_q,
        'v_m_b_b': v_t_s_b,
        'v_m_b_q': v_t_s_q,
        'v_m_s_b': row.v_t_b_b,
        'v_m_s_q': row.v_t_b_q,
        'sell_pct': round(v_t_s_b / row.v_b * 100, 4),
        'buy_pct': round(row.v_t_b_b / row.v_b * 100, 4),
        'way': way,
        'body': abs(row.o - row.c),
        'pct_shift': round(change * 100, 4),
        'center': (row.c + row.o) / 2,
        'pct_trade_vol': round(row.v_b / row.nt / row.v_b * 100, 10),
        'pct_h': round(pct_high * 100, 4),
        'pct_l': round(pct_low * 100, 4),
        'l_h': row.h - row.l,
        'body_l_h': round(((row.h - row.l) / abs(row.o - row.c) - 1), 4)
    }
    return pd.Series(extras)


def ts_to_datetime(ts):
    return datetime.fromtimestamp(ts, timezone.utc).strftime(DT_FMT)


def datetime_to_ts(dt):
    return int(time.mktime(datetime.strptime(dt, DT_FMT).timetuple())
            - time.timezone)


def find_row_i(df, p, f):
    if f == 'dt':
        return df.index[df.ts == datetime_to_ts(p)].tolist()[0]
    if f == 'ts':
        return df.index[df.ts == p].tolist()[0]


def df_to_str(df):
    return ' '.join([' '.join(df.iloc[[i]].squeeze().astype(str))
              for i in range(0, len(df))])


def df_info(df):
    df.reset_index(drop=True, inplace=True)

    s = 0
    for i in range(0, len(df)):
        row = df.iloc[[i]].squeeze()
        pct_change = (row.c / row.o - 1 if (row.o - row.c) < 0
            else (1 - row.c / row.o)) * 100
        s += pct_change
    avg_volatility = round(s / len(df), 4)

    s = df_to_str(df)

    info = {
        'avg_volat': avg_volatility,
        'num_candles': int(len(df)),
        'hash': hash_candles(s)
    }
    return pd.Series(info)


def hash_candles(s):
    return ssdeep.hash(s)

