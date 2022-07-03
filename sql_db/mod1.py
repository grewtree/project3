
import pandas as pd

def pre(df_unemployment, name):
    name = name
    df_sum = df_unemployment.iloc[:, :19]
    header = df_sum.iloc[0]
    df_sum = df_sum[1:]
    df_sum.rename(columns = header, inplace=True)
    df_sum.drop(columns = '계',inplace=True)
    df_loc = pd.concat([df_sum['시점'], df_sum[name]], axis =1)
    df_loc = df_loc.replace('-', 0)
    a = df_loc['시점'].str.split('-')

    i=0
    ls = []
    lss = []
    while i < len(a) : 
        ls.append(a.iloc[i][0])
        lss.append(a.iloc[i][1])
        i += 1
    df_loc['year'] = ls
    df_loc['month'] = lss
    df_loc.drop(columns='시점', inplace=True)
    df_loc['loc'] = df_loc.columns[0]
    df_loc.rename(columns = {str(df_loc.columns[0]):'unemployment'}, inplace=True)
    df_loc[['unemployment','year', 'month']] = df_loc[['unemployment','year', 'month']].astype(int)
    
    return df_loc
