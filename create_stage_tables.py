#!/usr/bin/env python
# coding: utf-8

# Setup
import pandas as pd
from pathlib import Path
import re
from parameters import locations, SPACING_CHAR
from journal_phrases import journal_phrases

output_dir = locations['staging']
game_list = list(locations['raw'].glob('*.csv'))

searches = {
    'outcome': re.compile(r'(\w+) is (.*?) as (\w+) \((.*?)\)', re.IGNORECASE),
    'game_name': re.compile(r'Game (?P<name>.*?) created.', re.IGNORECASE),
    'points': re.compile(r'(?P<points>\d+)', re.IGNORECASE)
}

## Functions
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


def generate_tables(game, *tables):
    """
    handler for stage table creation. reads game data based on Path object game and passes common information to each table generator.
    game: Path object to game journal file
    *tables: tables to generate
    """
    
#     need to add arguments to pass through mode and save options
    game_data = pd.read_csv(game, index_col=0)
    game_id = game.stem


def table_games(game, mode='add', save=False):
    """
    creates stage table 'games' or adds game to existing stage table 'games'
    returns dataframe of data
    game: Path object to game journal
    mode: ['add', 'create']
    save: bool - determines if resulting dataframe is saved to file
    overwrite: bool - if False, appends to existing file
    """
    GAMES_FILENAME = 'games.csv'
    GAMES_PATH = locations['staging'].joinpath(GAMES_FILENAME)
    if mode == 'create':
        games = pd.DataFrame(columns=['game_name', 'num_turns', 'start_date', 'end_date'])
    elif mode == 'add':
        if GAMES_PATH.exists():
            games = pd.read_csv(GAMES_PATH, index_col=0)
        else:
            raise(f'{GAMES_FILENAME} does not exist. Use mode=\'create\'')
    else:
        raise ValueError(f'mode {mode} not found. Must be either "add" or "create"')
    
    game_id = game.stem
    game_data = pd.read_csv(game, index_col=0)
    find_name = re.search(searches['game_name'], get_str_from_journal(game,'creation')['creation'])
    if find_name:
        game_name = find_name.group('name')
    else: 
        game_name = ''
    
    summary = {
        'game_name': game_name,
        'num_turns': game_data['round'].max()-1, # offset by one to account for post-game scoring listed as a turn in journal
        'end_date': game_data['time'].max(),
        'start_date':game_data['time'].min()
    }
    
    games = games.append(pd.DataFrame(summary,index=[game_id]))
    
    if save:
        games.to_csv(GAMES_PATH)
    return games
    
    
def parse_journal(game, save=False):
    """
    Create set of stage tables parsing each journal entry phrase defined in dict journal_phrases
    Input is path to individual game file
    returns a dict of dfs representing each generated table.
    """
    journal = pd.read_csv(game, index_col=0)
    journal['game_id'] = game.stem
    output = {}
    for phrase, template in journal_phrases.items():
#         print(f'parsing {phrase}')
        file = f'{phrase}.csv'
        filepath = locations['staging'].joinpath(file)
        search = re.compile(template, re.IGNORECASE)
        matches = journal['text'].apply(lambda logentry: re.match(search, logentry))
        matches.dropna(inplace=True)
        parsed_df = pd.DataFrame(matches.apply(lambda x: x.groupdict()).to_list(), index=matches.index)
        parsed_df = parsed_df.join(journal[['time','age','round','game_id','text']])
        if filepath.exists():
            existing_data = pd.read_csv(filepath, index_col=0)
            parsed_df = existing_data.append(parsed_df)
        parsed_df.reset_index(drop=True, inplace=True)
        output[phrase] = parsed_df
        if save:
            parsed_df.to_csv(filepath)
    return output
    
    
# Generate Tables
if __name__ == "__main__":
    players = pd.DataFrame()
    scores = pd.DataFrame()

    for game in game_list:
        game_data = pd.read_csv(game, index_col=0)
        game_id = game.stem
        parse_journal(game, save=True)
        summary_df = parse_summary(game)
        summary_df = summary_df.transpose().reset_index()
        summary_df['game_id'] = game_id
        players = players.append(summary_df.loc[:,['game_id','player','name']])
        scores = players.append(summary_df)


    # Store Tables

    players.reset_index().drop('index').to_csv(output_dir.joinpath('players.csv'))
    scores.reset_index().drop('index').to_csv(output_dir.joinpath('scores.csv'))

