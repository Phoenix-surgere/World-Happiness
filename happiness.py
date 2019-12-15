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

Standard Error
The standard error of the happiness score.

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

Dystopia Residual
The extent to which Dystopia Residual contributed to the calculation of the Happiness Score.
"""

import glob 
import pandas as pd
directory = 'world-happiness'
all_files = glob.glob(directory + "/*.csv")
ls = []
#df = pd.concat((pd.read_csv(f) for f in all_files), sort=False)

for f in all_files:
    ls.append(pd.read_csv(f))    


for df in ls:
    print(df.columns)
    print('*'*5)
    
print('%'*20)
#LIST OF FIXES TO EQUALIZE dfs or to drop non-useful columns or rename etc
ls[1].drop(columns=['Lower Confidence Interval','Upper Confidence Interval'], inplace=True)
ls[0].drop(columns=['Standard Error'], inplace=True)
ls[3].rename(columns={'Country or region': 'Country'}, inplace=1)
ls[2].drop(columns=['Whisker.low','Whisker.high'], inplace=True)

ls[2].rename(columns={'Happiness.Rank' : 'Happiness Rank', 
 'Happiness.Score': 'Happiness Score', 
 'Economy..GDP.per.Capita.': 'Economy (GDP per Capita)', 
 'Health..Life.Expectancy.' : 'Health (Life Expectancy)', 
 'Trust..Government.Corruption.': 'Trust (Government Corruption)', 
 'Dystopia.Residual': 'Dystopia Residual'}, inplace=1)

for df in ls:
    print(df.columns)
    print('*'*5)