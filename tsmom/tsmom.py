import numpy as np

def momentum(main_data, long_only=False, risk=.4):
    asset_return = {}
    assets = list(main_data.columns)
    
    returns_12 = main_data.pct_change(periods=24) # dias uteis (1 mes)
    returns_1 = main_data.pct_change(periods=252) # dias uteis (12 meses)
    vol_1 = main_data.ewm(adjust=True, com=60, min_periods=0).std() #.dropna()
    
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
    return np.mean(array, axis=1)