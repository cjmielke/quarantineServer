import pandas
import pandas as pd

indexDF = pandas.read_csv('static/csv/index.csv', index_col='key')

indexUS = indexDF[indexDF.country_code=='US']

indexStates = indexUS[indexUS.aggregation_level==1].rename(columns=dict(subregion1_code='state'))

#FIXME update later if timestmap is old
epData = 'static/csv/epidemiology.csv'
epDF = pandas.read_csv(epData)

stateKeys = list(indexStates.index)

stateEpi = epDF[epDF['key'].isin(stateKeys)]


#dfUS = df[df['key'].str.startswith('US_')]

merged = pandas.merge(stateEpi, indexStates['state'], left_on='key', right_on='key', how='left')

del merged['key']

'''
merged = merged.set_index(['date', 'state'])
merged = merged.fillna(0)
merged = merged.astype(int)

#merged=merged.sort_values('state')

merged = merged.tail(5000)
merged.to_csv('static/state-epi.tsv', sep='\t')
'''

df = merged
print df.head

df['date'] = pd.to_datetime(df['date']) - pd.to_timedelta(7, unit='d')
df = df.groupby(['state', pd.Grouper(key='date', freq='W-MON')]).sum().reset_index().sort_values('date')


df = df.set_index(['date', 'state'])
df = df.fillna(0)
df = df.astype(int)

df = df.tail(50*100)
df.to_csv('static/state-epi-byweek.tsv', sep='\t')



#print df


# ============== counties


indexCounties = indexUS[indexUS.aggregation_level==2]#.rename(columns=dict(subregion1_code='state'))




