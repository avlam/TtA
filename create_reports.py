#!/usr/bin/env python
# coding: utf-8

# Setup
import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt
import parameters

# Load Tables
games = pd.read_csv(parameters.locations['staging'].joinpath('games.csv'), index_col=0)
views = list(parameters.locations['analysis'].glob('*.csv'))

analysis_views={}
for view in views:
    analysis_views[view.stem] = pd.read_csv(view, index_col=0)
analysis_views['game_scores'].head()

# Reports
## player performance
data_source = analysis_views['game_scores']
focus_player = 'david'

filtered_data = data_source.loc[data_source['players']==focus_player]
overall = filtered_data.groupby('seat').agg({'game_id':'count', 'scores':['mean', 'median']})
overall.columns = ['count', 'mean culture', 'median culture']
place_counts = filtered_data.groupby('seat')['place'].value_counts().unstack().fillna(0)
overall.index = pd.CategoricalIndex(overall.index, ['orange','purple','green','grey'])
overall.sort_index().join(place_counts)

## seating order randomization

