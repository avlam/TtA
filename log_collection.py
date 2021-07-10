#!/usr/bin/env python
# coding: utf-8

# # Context

# Objectives: 
# 1. Retrieve list of Game IDs from https://docs.google.com/spreadsheets/d/1Lvu2dSS43P-FoaHSVLAuLHJvVfyUAtrXrm9xtK-Cc-8/edit?usp=sharing
# 2. Access boardgaming-online.com
# 3. Scrape for Game Journals
# 
# Stretch Goals:
# 1. Scrape Civilopedia

# # Setup

# In[1]:


import pandas as pd
import requests
# from splinter import Browser
from bs4 import BeautifulSoup as bs
# from googleapiclient import discovery
from pathlib import Path
from bgo import login_data


# ## Google API

# In[ ]:


credentials = None
service = discovery.build('sheets','v4', credentials=credentials)


# In[ ]:


# copied from google api doc example:
# The ID of the spreadsheet to retrieve data from.
spreadsheet_id = '1195389494'  # TODO: Update placeholder value.

# The A1 notation of the values to retrieve.
range_ = 'A1:A100'  # TODO: Update placeholder value.

# How values should be represented in the output.
# The default render option is ValueRenderOption.FORMATTED_VALUE.
value_render_option = ''  # TODO: Update placeholder value.

# How dates, times, and durations should be represented in the output.
# This is ignored if value_render_option is
# FORMATTED_VALUE.
# The default dateTime render option is [DateTimeRenderOption.SERIAL_NUMBER].
date_time_render_option = ''  # TODO: Update placeholder value.

request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_, valueRenderOption=value_render_option, dateTimeRenderOption=date_time_render_option)
response = request.execute()


# Ideally, a connection using Google API could be made to reference GameIDs as logged in spreadsheet. Short of achieveing this, see below for list of Game IDs.

# In[2]:


game_id_list = pd.read_csv('game_id_list.csv')


# ## Boardgaming-Online

# Set up session with login credentials from bgo.py

# In[3]:


site = 'http://boardgaming-online.com'

session = requests.Session()
session.post(site, data=login_data)


# ### Functions

# In[14]:


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
        tables = pd.read_html(response.text)
        page = tables[-1]
        page.rename(inplace=True,
            columns={0:'time',
                     1:'player',
                     2:'age',
                     3:'round',
                     4:'text'})
        return page

    url_template = 'http://www.boardgaming-online.com/index.php?cnt=52&pl={game_id}&pg={page_num}'
    page_num = 1
    
    response = session.get(url_template.format(game_id=game_id, page_num=page_num))
    if response.status_code == 200:
        page_max = get_page_max(response)
        print(f'max_pages: {page_max}')
        logs_paged = [get_journal_page(response)]
        if page_max > page_num:
            for page in range(page_num, page_max):
                print(f'retrieving page: {page+1} of {page_max} \nurl: {url_template.format(game_id=game_id, page_num=page+1)}')
                response = session.get(url_template.format(game_id=game_id, page_num=page+1))
                logs_paged.append(get_journal_page(response))
            logs = pd.concat(logs_paged, ignore_index=True)
            print(logs_paged)
        else:
            logs = logs_paged[0]
    else:
        print('Something went wrong')
        pass
    
    return logs


# In[ ]:


response = session.get(url_template.format(game_id=game_id))
soup = bs(response.text, 'html.parser')


# In[ ]:


soup.find_all('a', {'class': 'numPageLien'})


# In[ ]:


max([int(link.get_text()) for link in soup.find_all('a', {'class': 'numPageLien'})])


# In[ ]:


tables = pd.read_html(response.text)
log = tables[-1]

# clean log
log.rename(inplace=True,
    columns={0:'time',
             1:'player',
             2:'age',
             3:'round',
             4:'text'})


# In[ ]:


log['text'][0]


# # Data Collection

# In[15]:


result = get_logs(session, '7493350')


# In[16]:


result


# In[ ]:




