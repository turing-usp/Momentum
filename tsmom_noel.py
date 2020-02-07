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
            'NK_RAD.CSV', 'SP_RAD.CSV', 'UB_RAD.CSV', 'AX_RAD.CSV']  # removed ND_RAD.csv since data ends ins 2015

    asset_list = []

    for ticker in tickers:
        df = pd.read_csv('data/' + ticker, names=["date_str", "open", "high", "low", "close", "volume", "open_interest"])
        df['date'] = pd.to_datetime(df['date_str'])
        r = pd.date_range(start=df.date.min(), end=df.date.max())  # fixing missing date values
        df = df.set_index('date').reindex(r).fillna(method="ffill").rename_axis('date').reset_index()  # fixing missing date values
        df["weekday"] = df.date.dt.weekday
        toDrop5 = df[df['weekday'] == 5].index
        toDrop6 = df[df['weekday'] == 6].index
        df.drop(toDrop5, inplace=True)
        df.drop(toDrop6, inplace=True)
        df.index = df['date']
        df = df.drop(['date_str', 'date', 'weekday'], axis=1)
        df.fillna(method="ffill")  # treating missing data with forward fill
        asset_list.append(df.copy())
        return asset_list

def prepare_data(df, window = 252):
        df["daily_returns"] = df["close"].pct_change()
        df["lagged_returns"] = df["close"].pct_change(periods=window)
        # sign function over return from last 252 days
        df["sign"] = np.sign(df["lagged_returns"])
        # Exponentially weighted standard deviation, scaled annually, center of mass = 60 days (as in Section 2.4)
        df["volatility"] = 252*df["daily_returns"].ewm(com=60).std()
        num = df["sign"]._get_numeric_data()
        num[num < 0] = 0
        return df
#%%
assets = load_data()
assets = [prepare_data(asset) for asset in assets]
#%%
date = pd.to_datetime("22-06-16")  # initial date dd-mm-yy

# weights are inversely proportional to an asset volatility
weights = [1/(asset["volatility"].loc[date])*asset["sign"].loc[date] for asset in assets]
weights /= sum(weights) # sum = 1

# cumulative returns based on initial date and weighted
for (asset, weight) in zip(assets, weights):
    asset["cumulative_weighted_returns"] = weight*(asset["close"]/asset["close"].loc[date] - 1)*asset["sign"]

#%%
portfolio = assets[-1]["cumulative_weighted_returns"]
for i in range(len(assets)-1):
    portfolio += assets[i]["cumulative_weighted_returns"]
# plot cumulative weighted returns
portfolio.loc[date : "22-06-17"].plot()
# %%
