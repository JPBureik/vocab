#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 21:21:47 2024

@author: jp
"""
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import numpy as np
from datetime import date

from vocab.core.load_from_db import load_from_db, save_to_db
from vocab.vis.user_interface import UserInterface
from vocab.core.language_select import language_select

ui = UserInterface()

# Select foreign language:
# foreign_lang = language_select(ui.ti)
foreign_lang = 'Spanish'

# Load table from database:
table_df = load_from_db(foreign_lang)

# Display stats:
# ui.ti.print_table(foreign_lang, table_df)

url_trad = {
    'Spanish': 'spanisch'
    }



with open('/Users/jp/Library/Application Support/Google/Chrome/Profile 6/Bookmarks', 'r') as handle:
    bookmarks = handle.read().split('\n')
    bm_keep = []
    for b in bookmarks:
        if 'dict.leo.org' in b:
            if url_trad[foreign_lang] in b:
                if not 'name' in b:
                    bm_keep.append(b.split('"url": ')[1].strip('"'))
                    
# Print number of available new items:
# print(f'To add: {len(bm_keep)} items\n')

for b in tqdm(bm_keep, desc='Fetching vocable items'):

    page = requests.get(b)
    
    soup = BeautifulSoup(page.content, "html.parser")
    
    # print(b)
    
    # results = soup.find(id="ResultsContainer")
    
    a = soup.find_all("div", id="centerColumn")
    
    # a = a.split('<tbody>')[1]
    
    print('\n')

    
    break

excl_str = ['Pl.', 'Adj.']
shift_str = ['-', 'auch']

res = pd.Series(dtype=str)

for aa in a:
    try:
        for aaa in aa.split('\xa0'):
            pass
    except:
        pass
    x = aa.text
    xx = x.split('\xa0')
    for idx, i in enumerate(xx):
        if idx > 2:
            if not str.isspace(i):
                if any(expr in i for expr in excl_str):
                    continue
                else:
                    if i:
                        if any(i.startswith(s) for s in shift_str):
                            res.at[res.index.max()] += i
                        else:
                            res.at[idx] = i
                            
                        
# Re-index:
res.index=range(res.size)

idxs_to_delete = set()

# Exclude German grammar annotations:
for idx in res.index:
    if res[idx]=='|':
        # Delete following row as well:
        idxs_to_delete.add(idx)
        idxs_to_delete.add(idx + 1)
for idx in idxs_to_delete:
    res.drop(idx, inplace=True)
        
# Re-index:
res.index=range(res.size)

# Remove final annotation marker:
for idx in res.index:
    if res[idx].startswith('| '):
        res.at[idx] = res.loc[idx].split('| ')[1]

# Check for trailing annotations:
idxs_to_delete = set()
for idx in res.index:
    if res[idx].startswith('-'):
        res[idx - 1] += res[idx]
        idxs_to_delete.add(idx)
    
for idx in idxs_to_delete:
    res.drop(idx, inplace=True)
        
# Re-index:
res.index=range(res.size)


     
# Remove trailing section headings:
section_headings = ['Substantive', 'Verben', 'Adjektive / Adverbien']

for idx in res.index:
    for sh in section_headings:
        if sh in res.loc[idx]:
            res.at[idx] = str.join('', res.loc[idx].split(sh)).strip()

# End marker:
end_marker = 'Werbung'  # Orthographisch ähnliche Wörter / Aus dem Umfeld der Suche

for idx in res.index:
    if end_marker in res.loc[idx]:
        res.at[idx] = res.loc[idx].split(end_marker)[0]
        end_idx = idx
        break
    
res.drop(res.index[res.index>end_idx], inplace=True)





new_df = pd.DataFrame(columns=[f'{foreign_lang}', 'German'])

for idx in np.arange(res.index[0], res.index[-1], 2):
    new_df.loc[idx] = pd.Series({
        f'{foreign_lang}': res[idx].strip(),
        'German': res[idx + 1].strip()
            })
    
# Re-index:
new_df.index=range(new_df.shape[0])
    
# Merge duplicates:
for idx in new_df.index:
    if new_df.duplicated(subset=f'{foreign_lang}')[idx]:
        new_df.loc[idx] = pd.Series({
            f'{foreign_lang}': new_df[f'{foreign_lang}'][idx],
            'German': f'{new_df["German"][idx-1]}, {new_df["German"][idx]}'
            })
        new_df.drop(idx-1, inplace=True)
        

# Exclude foreign alternatives:
for idx in new_df.index:
    # Alias:
    f = new_df[f'{foreign_lang}'].loc[idx]
    if '(auch' in f:
        new_df[f'{foreign_lang}'].at[idx] = f.split('(auch')[0] + str.join(')', f.split('(auch')[1].split(')')[1:]).strip()

# Move annotations to German side:

move_str = ['(', '[']

for idx in new_df.index:
    # Alias:
    f = new_df[f'{foreign_lang}'].loc[idx]
    for ms in move_str:
        if ms in f:
            new_df[f'{foreign_lang}'].at[idx] = f.split(ms)[0]
            new_df['German'].at[idx] += f' {ms}{f.split(ms)[1]}'
            # Only once per item:
            break
   

# Package imports:
from vocab.core.to_db import to_db
from vocab.core.vocable import Vocable
from vocab.vis.terminal_interface import TerminalInterface
ti = TerminalInterface()
    
for idx in new_df.index:
    
    voc = Vocable(foreign_lang, new_df['German'].loc[idx], new_df[f'{foreign_lang}'].loc[idx])
    print(voc)
    cont_query = input('Continue?\n')
    if cont_query=='':
        ti.del_lines(7)
    else:
        break


    # to_db(voc, phase=voc.phase, date=date)
