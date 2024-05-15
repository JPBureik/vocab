#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 21:21:47 2024

@author: jp
"""
import requests
import sys
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import numpy as np
from datetime import date
from langdetect import detect

from vocab.core.load_from_db import load_from_db, save_to_db
from vocab.vis.user_interface import UserInterface
from vocab.core.language_select import language_select
from vocab.core.to_db import to_db
from vocab.core.vocable import Vocable
from vocab.vis.terminal_interface import TerminalInterface

import warnings
from bs4 import XMLParsedAsHTMLWarning
warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)

ui = UserInterface()

# Select foreign language:
foreign_lang = language_select(ui.ti)
# foreign_lang = 'Spanish'

# Load table from database:
table_df = load_from_db(foreign_lang)

# Display stats:
ui.ti.print_table(foreign_lang, table_df)



lang_det_trad = {
    'Spanish': 'es'
    }

def read_bookmarks(foreign_lang):

    url_trad = {
        'Spanish': 'spanisch'
        }

    with open('/Users/jp/Library/Application Support/Google/Chrome/Profile 6/Bookmarks', 'r') as handle:
        all_bookmarks = handle.read().split('\n')
        lang_bookmarks = []
        for b in all_bookmarks:
            if 'dict.leo.org' in b:
                if url_trad[foreign_lang] in b:
                    if not 'name' in b:
                        lang_bookmarks.append(b.split('"url": ')[1].strip('"'))
                        
    return lang_bookmarks
    
def fetch_site_contents(bookmark):
                    
    page = requests.get(bookmark)
    
    soup = BeautifulSoup(page.content, "html.parser")
    
    vocab_fields = soup.find_all("div", id="centerColumn")
    
    return vocab_fields

def parse_text(vocab_fields):
        
    excl_str = ['Pl.', 'Adj.', 'Suchverlauf', 'Zur mobilen Version wechseln', 'Substantive', '(Verb)', 'Phrasen']
    shift_str = ['-', 'auch']
    
    res = pd.Series(dtype=str)
    
    for aa in vocab_fields:
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
    end_markers = ['Werbung', 'Publicidad']  # Orthographisch ähnliche Wörter / Aus dem Umfeld der Suche
    
    end_idx = None
    
    for idx in res.index:
        for em in end_markers:
            if em in res.loc[idx]:
                res.at[idx] = res.loc[idx].split(em)[0]
                end_idx = idx
                break
    if end_idx:
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
    
    return new_df

def user_exit():
    ui.ti.del_lines(1)
    print('Bye!')
    sys.exit(0)

def user_input(new_df):
    
    # Package imports:
    
    ti = TerminalInterface()
        
    for idx in new_df.index:
        
        voc = Vocable(foreign_lang, new_df['German'].loc[idx], new_df[f'{foreign_lang}'].loc[idx])
        print(voc)
        cont_query = input('Press <Enter> to add to library. Enter <mod> to edit. Enter <skip> to move on to next item.\n')
        if cont_query=='quit':
            user_exit()
        elif cont_query=='skip':
            ui.ti.del_lines(7)
            continue
        elif cont_query=='':
            to_db(voc, phase=0, date=date.today())
            table_df = load_from_db(foreign_lang)
            ui.update_ui(table_df, foreign_lang, correct_counter=ctr,
                          total=len(lang_bookmarks), context='added new vocable')
        else:
            break    
    
    
def extract_vocab(bookmark, ctr):

    vocab_fields = fetch_site_contents(bookmark)    
    
    # Print number of available0 items:
    ui.ti.progress_bar(ctr, len(lang_bookmarks))

    new_df = parse_text(vocab_fields)
    
    user_input(new_df)
        
    ui.ti.del_lines(1)
    
#%% Execution:
    
if __name__ == '__main__':
    
    lang_bookmarks = read_bookmarks(foreign_lang)
    
    for ctr, bookmark in enumerate(lang_bookmarks):
        
        extract_vocab(bookmark, ctr)

    
    
    
        # to_db(voc, phase=voc.phase, date=date)
