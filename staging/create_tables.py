#!/usr/bin/env python
# coding: utf-8

# # Context

# Read game journals found in directory 'gamejournals'
# Create the following tables:
# - games
# - scores
# - players
# - wonders
# - leaders
# - tactics

# ### Columns

# - game_id (pk)
# - game_name
# - ~~winner (player name)~~
# - num_turns 
# - start_date 
# - end date

# ### Scores

# - game_id (pk)
# - orange (1st player)
# - purple (2nd player)
# - green (3rd player)
# - grey (4th player)

# ### Players

# - game_id (pk)
# - orange (1st player)
# - purple (2nd player)
# - green (3rd player)
# - grey (4th player)

# # Setup

# In[1]:


import pandas as pd
from pathlib import Path
import re


# In[2]:


staging_dir = Path.cwd()
journal_dir = Path(staging_dir,'..','gamejournals')
game_list = list(journal_dir.glob('*.csv'))


# In[3]:


searches = {
    'outcome': re.compile(r'(\w+) is (.*?) as (\w+) \((.*?)\)', re.IGNORECASE),
    'game_name': re.compile(r'Game (?P<name>.*?) created.', re.IGNORECASE),
    'points': re.compile(r'(?P<points>\d+)', re.IGNORECASE)
}


# ## Functions

# In[35]:


def get_str_from_journal(target_file, *targets):
    """
    helper to extract specific key strings from game journal. (e.g. summary text, game title)
    returns a dictionary with *targets as keys
    """
    
    key_strings = {
        'results': 1, # will always be first line in log after the headers for a completed game.
        'creation': -1 # will always be last line in log IF log is complete
    }
    output = {}
    
    if target_file.exists:
        with open(target_file, 'r') as game_journal:
            lines = game_journal.readlines()
            for target in targets:
                output.update({target: lines[key_strings[target]]})
    else:
        print(f'{target_file} not found.')
        pass
    
    return output


def alias_player(username):
    """
    lookup usernames and return player name
    
    future changes: move aliases to separate file and prompt for input when a new username is encountered.
    """
    alias = {
        'david li': 'david',
        'li david': 'david',
        'micah yospe': 'micah',
        'teddy yeh': 'teddy',
        'x l':'xan'
    }
    if username in alias.keys():
        return alias[username]
    else:
        print(f'new username found: {username}')
        return username
    
def parse_score(score_str):
    """
    Given a str score_str, try to extract score in points. if fails, return Nan
    """
    try:
        return re.match(searches['points'], score_str).group()
    except:
        return None
    
def parse_summary(game_file):
    """
    given a path game_file, output summary info is dict for input into df construction
    calls get_str_from_journal() for summary string
    """
    summary = re.findall(searches['outcome'], get_str_from_journal(game_file,'results')['results'].lower())
    summary_df = pd.DataFrame(summary)
    summary_df.rename(inplace=True,
                      columns={
                          0:'result',
                          1:'name',
                          2:'player',
                          3:'score'
                      })
    summary_df.set_index('player', inplace=True)
    summary_df['name'] = summary_df['name'].apply(alias_player)
    summary_df['score'] = summary_df['score'].apply(parse_score)
    return summary_df.transpose()


# # Generate Tables

# In[36]:


games = pd.DataFrame(columns=['game_name', 'num_turns', 'start_date', 'end_date'])
players = pd.DataFrame(columns=['orange', 'purple', 'green', 'grey'])
scores = pd.DataFrame(columns=['orange', 'purple', 'green', 'grey'])

for game in game_list:
    game_data = pd.read_csv(game, index_col=0)
    game_id = game.stem
    try:
        game_name = re.search(searches['game_name'], get_str_from_journal(game,'creation')['creation']).group('name')
    except:
        game_name = ''
    num_turns = game_data['round'].max()-1 # offset by one to account for post-game scoring listed as a turn in journal
    end_time = game_data['time'].max()
    start_time = game_data['time'].min()

    this_summary = {
        'game_name': game_name,
        'num_turns': num_turns,
        'start_date': start_time,
        'end_date': end_time
    }

    summary_df = parse_summary(game)

    games = games.append(pd.DataFrame(this_summary,index=[game_id]))
    players = players.append(pd.DataFrame(summary_df.loc['name',:].to_dict(),index=[game_id]))
    scores = scores.append(pd.DataFrame(summary_df.loc['score',:].to_dict(),index=[game_id]))


# # Store Tables

# In[37]:


players.to_csv()


# In[38]:


scores


# In[39]:


games


# In[ ]:




