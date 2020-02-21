#%%
import pandas as pd
import numpy as np
#%%
def load_data():
    tickers = ['AN_RAD.CSV', 'BN_RAD.CSV', 'CC_RAD.CSV', 'CN_RAD.CSV', 'CT_RAD.CSV',
               'DA_RAD.CSV', 'DX_RAD.CSV', 'EC_RAD.CSV', 'EN_RAD.CSV', 'ES_RAD.CSV',
               'FB_RAD.CSV', 'FN_RAD.CSV', 'GS_RAD.CSV', 'JN_RAD.CSV', 'JO_RAD.CSV',
               'KC_RAD.CSV', 'LB_RAD.CSV', 'MD_RAD.CSV', 'MP_RAD.CSV', 'MW_RAD.CSV',
               'SB_RAD.CSV', 'SC_RAD.CSV', 'SN_RAD.CSV', 'TU_RAD.CSV', 'CA_RAD.CSV',
               'TY_RAD.CSV', 'US_RAD.CSV', 'ZA_RAD.CSV', 'ZB_RAD.CSV', 'CB_RAD.CSV',
               'ZC_RAD.CSV', 'ZF_RAD.CSV', 'ZG_RAD.CSV', 'ZH_RAD.CSV', 'ZI_RAD.CSV',
               'ZK_RAD.CSV', 'ZL_RAD.CSV', 'ZM_RAD.CSV', 'ZN_RAD.CSV', 'ZO_RAD.CSV',
               'ZP_RAD.CSV', 'ZR_RAD.CSV', 'ZS_RAD.CSV', 'ZT_RAD.CSV', 'ZU_RAD.CSV',
               'ZW_RAD.CSV', 'ZZ_RAD.CSV', 'DT_RAD.CSV', 'HS_RAD.CSV', 'LX_RAD.CSV',
               'NK_RAD.CSV', 'SP_RAD.CSV', 'UB_RAD.CSV', 'AX_RAD.CSV']  
               # removed ND_RAD.csv since data ends in 2015

    asset_list = []

    for ticker in tickers:
        df = pd.read_csv('../data/' + ticker, 
                        names=["date_str", "open", "high", "low", "close", "volume", "open_interest"])
        df['date'] = pd.to_datetime(df['date_str'])
        # fixing missing date values
        r = pd.date_range(start=df.date.min(), end=df.date.max())
        df = df.set_index('date').reindex(r).fillna(method="ffill").rename_axis('date').reset_index()  # fixing missing date values
        df["weekday"] = df.date.dt.weekday
        toDrop5 = df[df['weekday'] == 5].index
        toDrop6 = df[df['weekday'] == 6].index
        df.drop(toDrop5, inplace=True)
        df.drop(toDrop6, inplace=True)
        df.index = df['date']
        df = df.drop(['date_str', 'date', 'weekday'], axis=1)
        df.fillna(method="ffill")  # treating missing data with forward fill

        df["daily_returns"] = df["close"].pct_change()
        # Exponentially weighted standard deviation, scaled annually, center of mass = 60 days
        df["volatility"] = 252*df["daily_returns"].ewm(com=60).std()

        asset_list.append(df.copy())
    return asset_list

def make_portfolio(assets, date, window):
    # date as dd-mm-yy
    date = pd.to_datetime(date)
    for asset in assets:
        asset["sign"] = np.sign(asset["close"].pct_change(periods=window))
        # asset["sign"] = 1 # benchmark sempre comprado/vendido
    weights = [(1/(asset["volatility"].loc[date]))*asset["sign"].loc[date] for asset in assets]
    weights /= sum(weights) # sum = 1
    for (asset, weight) in zip(assets, weights):
        asset["weighted_cumulative_returns"] = weight*(asset["close"]/asset["close"].loc[date] - 1)
        

def returns(assets, initial_date, final_date, lookback_window = 252):
    make_portfolio(assets, initial_date, lookback_window)
    returns = assets[-1]["weighted_cumulative_returns"]
    for i in range(len(assets) - 1):
        returns += assets[i]["weighted_cumulative_returns"]
    returns.loc[initial_date : final_date].plot()
    #return returns.loc[initial_date : final_date]

#%%
assets = load_data()
#%%
date = "20-1-2010"
end = "20-1-2015"
window = 252

returns(assets, date, end, window)
#%%