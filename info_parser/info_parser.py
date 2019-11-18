#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from io import StringIO
import re

# Load the info.txt and the file storing all the problematic names
problem_entries_path = 'problem_entries.txt'
problem_entries=open(problem_entries_path,"r").read().split('\n')
data_path = 'info.txt'
data_file = open(data_path,"r").read().split('\n')

# Initialize the patterns used in parsing
year_pattern = re.compile("Year*")
entry_pattern = re.compile("[a-z]")

# Building a parsed dictionary
data_dict = {}
for line in data_file:
    if year_pattern.match(line):
        year = line.split(" ")[1]
        continue
    if entry_pattern.match(line):
        line = re.split(" +|\t+ *",line)
        if (len(line)>3 and len(line)<6):
            line[3:] = [' '.join(line[3:6])]
            data_dict.setdefault(year,[]).append(line)

# Building the multi-index for the DataFrame
tuples = []
for key in data_dict.keys():
    entry_num = len(data_dict[key])
    key_list = [key]*entry_num
    index_list = range(entry_num)
    tuples = tuples+(list(zip(key_list,index_list)))
index = pd.MultiIndex.from_tuples(tuples, names=['Year','Index'])

# Building the DataFrame from the dictioanry
info_df = pd.DataFrame(columns=['Name','Gender','Microphone','Accent'])
for key in data_dict.keys():
    year_df = pd.DataFrame(data_dict[key],columns=['Name','Gender','Microphone','Accent'])
    info_df=info_df.append(year_df)
info_df.index=index

# Remove the entries listed in problematic entry list
for p in problem_entries:
    indexName = info_df[info_df['Name']==p].index
    info_df.drop(indexName,inplace=True)

# Save to csv file
info_df.to_csv('recording_info.csv')





