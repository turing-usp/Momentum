import numpy as np

def tsmom_dates(main_data):
    change_month = []
    dates = main_data.iloc[252:].index 
    current_date = dates[0]
    for date in dates[1:]:
        if date.month != current_date.month:
            change_month.append(current_date)
        current_date = date
        
    return change_month

def tsmom_factor(r_1, r_12, v_1, risk, long_only):
    if long_only:
        sinal = np.ones(r_12.shape)
    else:
        sinal = np.sign(r_12)
    return risk * r_1 * sinal / v_1

def momentum2(df, long_only=False, risk=.4, dates=None):
    asset_return = {}
    
    returns_1 = df.pct_change(periods=24) # dias uteis (1 mes)
    returns_12 = df.pct_change(periods=252) # dias uteis (12 meses)
    vol_1 = np.sqrt(21) * df.pct_change().ewm(adjust=True, com=60, min_periods=0).std()
    
    r_1 = returns_1.loc[dates]
    r_12 = returns_12.loc[dates]
    v_1 = vol_1.loc[dates]
    
    array = tsmom_factor(
        r_1.values[1:,:],
        r_12.values[:-1,:],
        v_1.values[:-1,:],
        risk,
        long_only
    )
#     array = tsmom_factor(
#         r_1.values,
#         r_12.values,
#         v_1.values,
#         risk,
#         long_only
#     )
    
    for index, asset in enumerate(list(df.columns)):
        asset_return[asset] = array[:,index]
    return asset_return

def momentum(main_data, long_only=False, risk=.4, date=None):
    asset_return = {}
    assets = list(main_data.columns)
    
    returns_1 = main_data.pct_change(periods=24) # dias uteis (1 mes)
    returns_12 = main_data.pct_change(periods=252) # dias uteis (12 meses)
    vol_1 = np.sqrt(20) * main_data.ewm(adjust=True, com=60, min_periods=0).std() #.dropna()
    
    for asset in assets:
        tsmom_return = []
        current_date = returns_12.iloc[252:].index[0]
        for date in returns_12.index[253:]:
            if date.month != current_date.month: # mapeia transição entre meses
                s = sign(returns_12[asset][current_date]) if not long_only else 1
                r = s * returns_1[asset][current_date] * risk / vol_1[asset][current_date]
                tsmom_return.append(r)
            current_date = date
        asset_return[asset] = tsmom_return
    return asset_return

def sign(x):
    return 1 if x > 0 else -1

def tsmom_return(assets_return):
    array = np.array(list(assets_return.values()))
    return np.mean(array, axis=0)