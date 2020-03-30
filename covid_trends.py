import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
plt.rcParams['animation.convert_path'] = r'C:\Program Files\ImageMagick-7.0.10-Q16\convert.exe'
plt.rcParams['animation.ffmpeg_path'] = r'C:\Program Files\ffmpeg\bin'


def grouping(df):
    df_country_grouped = df.groupby(['Country/Region']).sum().reset_index()
    #df_country_filtered = df_country_grouped.loc[df_country_grouped['Country/Region'].isin(countries_list)]
    df_used_columns = df_country_grouped.drop(columns=['Lat', 'Long'])
    return df_used_columns


def clean_data(df, oldname, newname):
    df_melted = pd.melt(df, id_vars=['Country/Region'], var_name='Date', value_name='Cases')
    df_country = df_melted.set_index(['Country/Region','Date'])
    df_country.index=df_country.index.set_levels([df_country.index.levels[0], pd.to_datetime(df_country.index.levels[1])])
    df_country=df_country.sort_values(['Country/Region','Date'],ascending=True)
    df_country=df_country.rename(columns={oldname:newname})
    return df_country

def dailydata(dfcountry,oldname,newname):
    dfcountrydaily=dfcountry.groupby(level=0).diff().fillna(0)
    dfcountrydaily=dfcountrydaily.rename(columns={oldname:newname})
    return dfcountrydaily


ConfirmedCases_raw=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
DeathCases_raw = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
RecoveredCases_raw = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

ConfirmedCases_country_cleaned = clean_data(grouping(ConfirmedCases_raw),'Cases', 'Total Confirmed Cases')
DeathCases_country_cleaned = clean_data(grouping(DeathCases_raw),'Cases','Total Deaths')
RecoveredCases_country_cleaned = clean_data(grouping(RecoveredCases_raw),'Cases','Total Recoveries')

ConfirmedCases_country_daily = dailydata(ConfirmedCases_country_cleaned,'Total Confirmed Cases', 'Daily Confirmed Cases')
DeathCases_country_daily = dailydata(DeathCases_country_cleaned,'Total Deaths','Daily Deaths')
RecoveredCases_country_daily = dailydata(RecoveredCases_country_cleaned,'Total Recoveries','Daily Recoveries')

## combining tables
complete_dataset = pd.merge(ConfirmedCases_country_cleaned, ConfirmedCases_country_daily, how='left', left_index=True, right_index=True)
complete_dataset = pd.merge(complete_dataset, DeathCases_country_cleaned, how='left', left_index=True, right_index=True)
complete_dataset = pd.merge(complete_dataset, DeathCases_country_daily, how='left', left_index=True, right_index=True)
complete_dataset = pd.merge(complete_dataset, RecoveredCases_country_cleaned, how='left', left_index=True, right_index=True)
complete_dataset = pd.merge(complete_dataset, RecoveredCases_country_daily, how='left', left_index=True, right_index=True)
complete_dataset['Active Cases'] = complete_dataset['Total Confirmed Cases'] - complete_dataset['Total Deaths'] - complete_dataset['Total Recoveries']
complete_dataset['Percentage Active'] = np.round(complete_dataset['Active Cases']/complete_dataset['Total Confirmed Cases'], decimals=2)

TotalCasesCountry=complete_dataset.max(level=0)['Total Confirmed Cases'].reset_index().set_index('Country/Region')
TotalCasesCountry=TotalCasesCountry.sort_values(by='Total Confirmed Cases',ascending=False)
top_countries = TotalCasesCountry.head(20)
top_countries_list = list(top_countries.index.values)

print(complete_dataset.loc['Germany'])

# days = []
# y_conf = []
# ctr = 0

# for case in list(ConfirmedCases_germany):
#     days.append(ctr)
#     y_conf.append(float(ConfirmedCases_germany[case]))
#     ctr += 1

# days = np.asarray(days, dtype=np.float32)
# y_conf = np.asarray(y_conf, dtype=np.float32)


# fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
# sigmoid, = ax1.plot(days, y_conf, color='m', linestyle='dotted',label='Confirmed')
# ax1.legend()
# ax1.set_title('Sigmoid')


# line = [sigmoid]


# for ax in fig.get_axes():
#     ax.label_outer()

# plt.plot()

# def update(num, line):
#     line[0].set_data(days[:num], y_conf[:num])
#     line[0].axes.axis([0, 200, 0, 90000])
#     return line,

# ani = animation.FuncAnimation(fig, update, len(days), fargs=[line], blit=False)
# ani.save('test.gif', writer='imagemagick', fps=20)