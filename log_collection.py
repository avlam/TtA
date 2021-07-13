#!/usr/bin/env python
# coding: utf-8

# Context

# Objectives: 
# 1. Retrieve list of Game IDs from https://docs.google.com/spreadsheets/d/1Lvu2dSS43P-FoaHSVLAuLHJvVfyUAtrXrm9xtK-Cc-8/edit?usp=sharing
# 2. Access boardgaming-online.com
# 3. Scrape for Game Journals
# 
# Stretch Goals:
# 1. Scrape Civilopedia

# Setup
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
# from googleapiclient import discovery
from pathlib import Path
from bgo import login_data


# Google API
# Ideally, a connection using Google API could be made to reference GameIDs as logged in spreadsheet. Short of achieveing this, see below for list of Game IDs.

game_id_list = pd.read_csv('game_id_list.csv')
game_id_list = game_id_list['Game_ID'].to_list()


# Boardgaming-Online
# Set up session with login credentials from bgo.py
def create_BGO_session():
    """
    create an authenticated session for HTML scraping of boardgaming-online.com. returns a session object for use with requests.
    no input arguments needed unless this function is to be generalized in the future for other sites.
    """
    site = 'http://boardgaming-online.com'
    session = requests.Session()
    session.post(site, data=login_data)
    # Add error handling of authentication in the future
    return session


# Function(s)
def get_logs(session, game_id):
    """
    Retrieve game journal from Boardgaming-online.com provided an authenticated session.
    Outputs log as a dataframe
    game_id is expected to be an alphanumeric string
    """
    
    def get_page_max(response):
        """
        helper function to identify max page number for a game journal.
        """
        soup = bs(response.text, 'html.parser')
        page_links = soup.find_all('a', {'class': 'numPageLien'})
        page_numbers = [int(link.get_text()) for link in page_links]
        return max(page_numbers)
    
    def get_journal_page(response):
        """
        helper function to identify game journal content from html response, convert to dataframe, and clean columns
        """
        tables = pd.read_html(response.text.replace('<', '  <')) # replace separate lines formatted by HTML in text 
        page = tables[-1] # known that a few tables are present on webpage. last one is always the game journal
        page.rename(inplace=True,
            columns={0:'time',
                     1:'player',
                     2:'age',
                     3:'round',
                     4:'text'})
        return page

    url_template = 'http://www.boardgaming-online.com/index.php?cnt=52&pl={game_id}&pg={page_num}'
    page_num = 1 # default first page
    
    response = session.get(url_template.format(game_id=game_id, page_num=page_num))
    if response.status_code == 200:
        page_max = get_page_max(response)
        logs_paged = [get_journal_page(response)]
        if page_max > page_num:
            for page in range(page_num, page_max):
                response = session.get(url_template.format(game_id=game_id, page_num=page+1))
                logs_paged.append(get_journal_page(response))
            logs = pd.concat(logs_paged, ignore_index=True)
        else:
            logs = logs_paged[0]
    else:
        print('Something went wrong')
        pass
    
    return logs


# # Data Collection
if __name__ == "__main__":
    # As written log collection will cycle through all ids in game_id_list and recreate .csv files. add arguments to use this same script for single game log collection
    journal_path = Path('gamejournals')
    session = create_BGO_session()
    for game in game_id_list:
        output_file = journal_path.joinpath(f'{game}.csv')
        print(f'Collecting game data for {game}, saving to {output_file}')
        get_logs(session, game).to_csv(output_file)

