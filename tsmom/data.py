import pandas as pd
import numpy as np

tickers = ['AN_RAD.CSV','BN_RAD.CSV','CC_RAD.CSV','CN_RAD.CSV','CT_RAD.CSV',\
            'DA_RAD.CSV','DX_RAD.CSV','EC_RAD.CSV','EN_RAD.CSV','ES_RAD.CSV',\
            'FB_RAD.CSV','FN_RAD.CSV','GS_RAD.CSV','JN_RAD.CSV','JO_RAD.CSV',\
            'KC_RAD.CSV','LB_RAD.CSV','MD_RAD.CSV','MP_RAD.CSV','MW_RAD.CSV',\
            'SB_RAD.CSV','SC_RAD.CSV','SN_RAD.CSV','TU_RAD.CSV','CA_RAD.CSV',\
            'TY_RAD.CSV','US_RAD.CSV','ZA_RAD.CSV','ZB_RAD.CSV','CB_RAD.CSV',\
            'ZC_RAD.CSV','ZF_RAD.CSV','ZG_RAD.CSV','ZH_RAD.CSV','ZI_RAD.CSV',\
            'ZK_RAD.CSV','ZL_RAD.CSV','ZM_RAD.CSV','ZN_RAD.CSV','ZO_RAD.CSV',\
            'ZP_RAD.CSV','ZR_RAD.CSV','ZS_RAD.CSV','ZT_RAD.CSV','ZU_RAD.CSV',\
            'ZW_RAD.CSV','ZZ_RAD.CSV','DT_RAD.CSV','HS_RAD.CSV','LX_RAD.CSV',\
            'NK_RAD.CSV','SP_RAD.CSV','UB_RAD.CSV','AX_RAD.CSV']    #removed ND_RAD.csv since data ends ins 2015
    

def load():
    aux_list =[]

    for ticker in tickers:
        #df = pd.read_csv(ticker,names=["date_str", "open", "high", "low", ticker[0:2], "volume", "open_interest"])
        path = '../data/' + ticker
        df = pd.read_csv(path, names=["date_str", "open", "high", "low", "close", "volume", "open_interest"])
        df['date'] = pd.to_datetime(df['date_str'])
        r = pd.date_range(start=df.date.min(), end=df.date.max()) #fixing missing date values
        df = df.set_index('date') \
            .reindex(r).fillna(method = "ffill") \
            .rename_axis('date').reset_index() #fixing missing date values
        df["weekday"] = df.date.dt.weekday
        toDrop5 = df[df['weekday'] == 5].index
        toDrop6 = df[df['weekday'] == 6].index
        df.drop(toDrop5, inplace=True)
        df.drop(toDrop6, inplace=True)
        df.index = df['date']
        df = df.drop(['date_str','date','weekday'], axis = 1)
        df.fillna(method = "ffill") #treating missing data with forward fill
        
        new_df = prepare(df)
        new_df.columns = ['open', 'high', 'low', ticker[0:2], 'volume', 'open_interest',
       'daily_returns', 'lagged_returns', 'sign', 'volatility']
        aux_list.append(new_df[[ticker[0:2]]])

    return aux_list

def prepare(df, window = 252):
    df["daily_returns"] = df["close"].pct_change()
    df["lagged_returns"] = df["close"].pct_change(periods=window)
    # sign function over return from last 252 days
    df["sign"] = np.sign(df["lagged_returns"])
    # Exponentially weighted standard deviation, scaled annually, center of mass = 60 days (as in Section 2.4)
    df["volatility"] = 252*df["daily_returns"].ewm(com=60).std()
    num = df["sign"]._get_numeric_data()
    num[num < 0] = 0
    return df

# def close_price():
#     asset_data = load()
#     pass
    
# Main data
def get_main_data():
    data = load()
    main_data = data[0]
    for dataframe in data[1:]:
        main_data = pd.merge(main_data, dataframe, left_index=True, right_index=True)