# charts
 
### tf_transform(new timeframe, filename, ticks base)
create csv with transformed candles

    #
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

### find_row_i(df, position, format)
get row index by known position

    #
    # position: '01-01-0001 01:01:01' OR timestamp
    #
    # format: 'dt' if datetime; 'ts' if timestamp
    #

### candle_expand_info(row)
get extra info about df row

### ts_into_datetime(timestamp)
timestamp to datetime. format '01-01-0001 01:01:01' GMT0

### datetime_to_ts(datetime)
datetime to timestamp. format '01-01-0001 01:01:01' GMT0

### df_info(dataframe)
get info about df

### hash_candles(s)
get hist hash