#!/usr/bin/env python
# coding: utf-8

# # Setup

# In[1]:


import pandas as pd
from pathlib import Path


# In[2]:


staging_dir = Path(Path.cwd(),'staging')
analysis_dir = Path(Path.cwd(),'analysis')


# # Load Data

# In[3]:


staging_tables = list(staging_dir.glob('*.csv'))


# In[4]:


data = {}
for table in staging_tables:
    data[table.stem] = pd.read_csv(table, index_col=0)


# # Create View

# In[5]:


players_stack = pd.DataFrame(data['players'].stack(),columns=['players'])
scores_stack = pd.DataFrame(data['scores'].stack(),columns=['scores'])
game_scores = players_stack.join(scores_stack)


# In[6]:


game_scores = game_scores.reset_index().rename(columns={'level_0':'game_id', 'level_1':'seat'})


# In[7]:


game_scores['place'] = game_scores.groupby('game_id')['scores'].rank(ascending=False, method='min')


# # Save View

# In[8]:


game_scores.to_csv(analysis_dir.joinpath('game_scores.csv'))

