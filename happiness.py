# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 20:48:49 2019

@author: black

LEGEND

Country
Name of the country.

Region
Region the country belongs to.

Happiness Rank
Rank of the country based on the Happiness Score.

Happiness Score
A metric measured in 2015 by asking the sampled people the question: "How would you rate your happiness on a scale of 0 to 10 where 10 is the happiest."

Economy (GDP per Capita)
The extent to which GDP contributes to the calculation of the Happiness Score.

Family
The extent to which Family contributes to the calculation of the Happiness Score

Health (Life Expectancy)
The extent to which Life expectancy contributed to the calculation of the Happiness Score

Freedom
The extent to which Freedom contributed to the calculation of the Happiness Score.

Trust (Government Corruption)
The extent to which Perception of Corruption contributes to Happiness Score.

Generosity
The extent to which Generosity contributed to the calculation of the Happiness Score.

"""

#NOW ALL DATAFRAMES HAVE SAME COLUMNS, SAME columns
import glob 
import pandas as pd
directory = 'world-happiness'
all_files = glob.glob(directory + "/*.csv")
ls = []

for f in all_files:
    ls.append(pd.read_csv(f))    
    
print('%'*20)
#LIST OF FIXES TO EQUALIZE dfs or to drop non-useful columns or rename etc
ls[1].drop(columns=['Lower Confidence Interval','Upper Confidence Interval'], inplace=True)
ls[0].drop(columns=['Standard Error'], inplace=True)
ls[2].drop(columns=['Whisker.low','Whisker.high'], inplace=True)
ls[2].rename(columns={'Happiness.Rank' : 'Happiness Rank', 
 'Happiness.Score': 'Happiness Score', 
 'Economy..GDP.per.Capita.': 'Economy (GDP per Capita)', 
 'Health..Life.Expectancy.' : 'Health (Life Expectancy)', 
 'Trust..Government.Corruption.': 'Trust (Government Corruption)', 
 'Dystopia.Residual': 'Dystopia Residual'}, inplace=1)

df = ls[3]
dfcol = df.columns.tolist()
order = [1, 0, 2, 3, 4, 5, 6, 8,7]  #Order of the items selected from original list
dfordered = [dfcol[i] for i in order]
print(dfordered)
ls[3] = ls[3][dfordered]
ls[4] = ls[4][dfordered]

#drop non-common column Dystopia  - Add back later?
ls[0].drop(columns=['Dystopia Residual'], inplace=True)
ls[1].drop(columns=['Dystopia Residual'], inplace=True)
ls[2].drop(columns=['Dystopia Residual'], inplace=True)
regions_map = dict(zip(ls[0].Country, ls[0].Region ))
#Manually adding some info to reflect later developments
regions_map.update({'Somalia': 'Sub-Saharan Africa',
 'South Sudam': 'Middle East and Northern Africa',
 'Namibia': 'Sub-Saharan Africa',
 'Belize':'Latin America and Caribbean',
 'Northern Cyprus': 'Western Europe',
 'Trinidad & Tobago': 'Latin America and Caribbean',
 'Taiwan Province of China': 'Eastern Asia',
 'North Macedonia': 'Central and Eastern Europe',
 'Hong Kong S.A.R., China': 'Eastern Asia',
 'Gambia':'Sub-Saharan Africa',
 'South Sudan': 'Sub-Saharan Africa'
                    })
for i in range(2,5):
    try:    
        ls[i]['Region'] = ls[i]['Country or region'].replace(regions_map)
    except KeyError:
        ls[i]['Region'] = ls[i]['Country'].replace(regions_map)
        
for i in range(0,2):
    ls[i]['Greater Region']  = ls[i].Region
    ls[i].drop(columns=['Region'],inplace=True)
    ls[i].rename(columns={'Greater Region': 'Region'},inplace=True)

ls[3].columns, ls[4].columns = ls[0].columns, ls[1].columns

years = ['2015', '2016', '2017', '2018', '2019']
for i in range(0,5):
    ls[i]['Year'] = pd.to_datetime(years[i])

for df in ls:
    print(df.columns)
    print('*'*5)
    
#NOW dataframes all have same columns, same order, with region added, with time column so ready for merging if need be and EDA

data = pd.concat(ls, ignore_index=True,sort=True)
#EDA BEGINS BELOW-----------------    

import matplotlib.pyplot as plt 
les_miserables = data.loc[data['Happiness Rank'] > 140].reset_index(drop=True)
A=les_miserables.groupby(by='Year').Region.value_counts()
#print(A)
A.unstack(level=0).plot(kind='bar', subplots=True, figsize=(10,10)); plt.show()

happy = data.loc[data['Happiness Rank'] < 20].reset_index(drop=True)
A=happy.groupby(by='Year').Region.value_counts()
#print(A)
A.unstack(level=0).plot(kind='bar', subplots=True, figsize=(10,10)); plt.show()

#Exploring Outliers - Happiest and Saddest Regions
westEurope = happy.loc[happy['Region'] == 'Western Europe'].reset_index(drop=True)
subSahara = les_miserables.loc[les_miserables['Region'] == 'Sub-Saharan Africa'].reset_index(drop=True)

westEuroped = westEurope.groupby(by='Country').mean().drop(columns=['Happiness Rank', 'Happiness Score'])
subSaharad = subSahara.groupby(by='Country').mean().drop(columns=['Happiness Rank', 'Happiness Score'])

westEuroped = westEuroped.median()
subSaharad = subSaharad.median()

plt.xticks(rotation=90); 
plt.title('Median Happiness Factor values across Happiest Region (West Europe)')
sns.barplot(data=pd.DataFrame(westEuroped).T); plt.show()

plt.xticks(rotation=90); 
plt.title('Median Happiness Factor values across Saddest Region (Sub Sahara)')
sns.barplot(data=pd.DataFrame(subSaharad).T); plt.show()


#Exploring regions more generally
regions = data.groupby(by='Region').median()
for factor in regions:
    if factor != 'Happiness Rank' and factor != 'Happiness Score':
        plots = regions.loc[:,factor].sort_values(ascending=False)
        print(plots)
        print('\n')
        
    
#exploring time series trend of factors and scores    
years = data.drop(columns=['Happiness Rank', 'Happiness Score']).groupby(by='Year').median() 
years.plot(subplots=True, figsize=(10,10),title='Median Global values over time'); 
plt.show()

import seaborn as sns
import numpy as np
corr = regions.drop(columns=['Happiness Rank']).corr()
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
sns.heatmap(corr, annot=True); plt.show()

#Continent analysis, inspired by kaggle notebook by Javad Zabihi
continents = {'Western Europe': 'Europe',
               'Central and Eastern Europe': 'Europe',
              'Eastern Asia': 'Asia',  
              'Southeastern Asia': 'Asia',
              'Southern Asia': 'Asia' ,
              'Latin America and Caribbean': 'South America', 
              'Middle East and Northern Africa': 'Africa', 
              'Sub-Saharan Africa':'Africa',
              'Australia and New Zealand': 'Australia'}
data['Continent'] = np.nan
data['Continent'] = data['Region'].replace(continents)

fig, (ax1, ax2) = plt.subplots(2,1, figsize=(10,10))
ax1.title.set_text('Happiness across Continents - Boxplot')
ax2.title.set_text('Happiness across Continets - Scatterplot')
sns.boxplot(ax=ax1, data=data, y='Happiness Score', x='Continent')
#sns.swarmplot(ax=ax2, x='Continent' , y='Happiness Score', hue='Continent',data=data)
plt.show()

#Violinplots for every factor affecting Happiness across Continents
data_copy = data.drop(columns=['Happiness Rank', 'Happiness Score', 'Region', 'Year', 'Country'])
for column in data_copy.columns[:-1]:
    plt.xticks(rotation=90)
    plt.title(f'{column} Distribution across Continents')
    sns.violinplot(data=data_copy, y=column, x='Continent')
    plt.show()
    
#Scatterplots for every factor affecting Hapiness across Continents to get extra sense  
data_copy = data.drop(columns=['Happiness Rank',  'Region', 'Year', 'Country'])
for column in data_copy.columns[:-1]:
    plt.xticks(rotation=90)
    plt.title(f'{column} Distribution across Continents')
    sns.scatterplot(x=column, y='Happiness Score', data=data, hue='Continent');
    plt.show()
