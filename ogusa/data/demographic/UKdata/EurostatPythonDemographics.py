'''
Download of Eurostat demographic data using the Eurostat Python Package
https://pypi.org/project/eurostat/

Downloads all the population, fertility & mortality data needed for 
OG-MOD (to be processed in demographics.py).
'''
import eurostat

###### USER ENTRY: country and year ########
Country = 'UK'
Year = 2018
############################################

StartPeriod = Year
EndPeriod = Year

filter_pars = {'GEO': [Country]}
df_pop = eurostat.get_sdmx_data_df('demo_pjan', StartPeriod, EndPeriod, filter_pars, flags = True, verbose=True)
df_mort = eurostat.get_sdmx_data_df('demo_magec', StartPeriod, EndPeriod, filter_pars, flags = True, verbose=True)
df_fert = eurostat.get_sdmx_data_df('demo_fasec', StartPeriod, EndPeriod, filter_pars, flags = True, verbose=True)

print(df_pop)
print(df_mort)
print(df_fert)

