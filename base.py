from binance_hist import *

##### code #####



################

# create csv with transformed candles
# tf_transform()
    #
    # new_tf, int or str
    # new timeframe, must be a multiple of ticks_base
    # premade TFs: 15m, 1h, 4h, 1d OR free number of ticks
    #
    # filename, 'baseAsset_quoteAsset_timeframe' (csv)
    #
    # ticks_base, int
    # number of ticks between candles in original file
    #
    # RESULT data adapted to new TF saved in project folder
    #

# get extra info about row
# row_expand_info()
    #
    # row, from pandas df
    #
    # RESULT pandas Series object
    #

# timestamp to datetime
# ts_into_datetime()
    #
    # ts, timestamp
    #
    # RESULT datetime in format 01-01-0001 01:01:01
    #

# datetime to timestamp
# datetime_to_ts()
    #
    # dt, datetime in format '01-01-0001 01:01:01'
    #
    # RESULT timestamp
    #

# get info about period
# period_info()
    #
    # df, dataframe
    #
    # start, start of the period: index / timestamp / datetime
    #
    # end, end of the period: index / timestamp / datetime
    #
    # f, format of start and end.
    # 'i' for index, 'ts' for timestamp, 'dt' for datetime ('01-01-0001 01:01:01')
    #
    # RESULT pandas Serial object
    #