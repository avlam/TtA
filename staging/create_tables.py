#!/usr/bin/env python
# coding: utf-8

# # Context

# Read game journals found in directory 'gamejournals'
# Create the following tables:
# - outcome_summary
# - players
# - wonders
# - leaders
# - tactics

# # Setup

# In[32]:


import pandas as pd
from pathlib import Path
import re


# In[23]:


staging_dir = Path.cwd()
journal_dir = Path(staging_dir,'..','gamejournals')
games = list(journal_dir.glob('*.csv'))


# In[ ]:


searches = {
    'outcome': re.compile(r'(\w+) is (.*?) as (\w+) \((.*?)\)', re.IGNORECASE)
    'game_name': re.compile(r'Game (.*?) created.', re.IGNORECASE)
}


# ## Functions

# In[118]:


def get_str_from_journal(game_id, *targets):
    """
    helper to extract specific key strings from game journal. (e.g. summary text, game title)
    """
    
    key_strings = {
        'results': 1, # will always be first line in log after the headers for a completed game.
        'creation': -1 # will always be last line in log 
    }
    output = {}
    
    target_file = journal_dir.joinpath(f'{game_id}.csv')
    if target_file.exists:
        with open(target_file, 'r') as game_journal:
            lines = game_journal.readlines()
            for target in targets:
                output.update({target: lines[key_strings[target]]})
    else:
        print(f'{target_file} not found.')
        pass
    
    return output


# In[120]:


target_file = journal_dir.joinpath(f'7493350.csv')
with open(target_file, 'r') as game_journal:
    lines = game_journal.readlines()


# In[121]:





# In[119]:


get_str_from_journal('7493350', 'creation','results')


# # Explore

# In[ ]:




