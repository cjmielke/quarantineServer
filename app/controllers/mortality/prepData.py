import pandas


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

merged = merged.set_index(['date', 'state'])




pandas.options.display.float_format = '{:,.0f}'.format
merged = merged.fillna(0)
merged = merged.astype(int)


#merged=merged.sort_values('state')

merged = merged.tail(5000)

merged.to_csv('static/state-epi.tsv', sep='\t')


#print df




