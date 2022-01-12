#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 11:49:58 2021

@author: hridindu
"""
import pandas as pd
import time
import datetime
from psaw import PushshiftAPI

api = PushshiftAPI()
def date_to_epoch(date):
    epoch = time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple())
    return int(epoch)

def pushshift_to_df(subreddit, 
                    after_date, 
                    n_submissions):  ###date_after = date as '%dd/%mm/%yyyy'
    
    after_date = date_to_epoch(after_date)
    data = list(api.search_submissions(after     = after_date,
                                       # before    = time.time_ns()/1e9,
                                       subreddit = subreddit,
                                       filter    =['url','subreddit','author', 'title', 'selftext'],
                                       sort_type = 'created_utc',
                                       sort      = "asc", 
                                       limit     =n_submissions))
    data = pd.DataFrame(data)
    data = data.drop(['d_'], axis = 1)
    data = data[~data['author'].str.startswith('[deleted]')]
    data = data[~data['selftext'].str.startswith('[removed]')]
    data = data[data['selftext'].str.len() != 0]

    data['created_utc'] = pd.to_datetime(data['created_utc'], unit = 's')
    data['created']     = pd.to_datetime(data['created'], unit = 's')

    return data
#%%    
data = pushshift_to_df('abortion', '20/03/2020', 650)
#%%
data.to_excel('reddit_scrape_07042021.xlsx')
#%%
data2 = data[['title', 'selftext']]
#%%
data3 = 'Title: ' + data['title'] + '\n\nText: ' + data['selftext'] + '\n\n\n'
data3.to_csv('reddit_scrape_07042021_cat.txt')
    
    
    
    
    
    
    