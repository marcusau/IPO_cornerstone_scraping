#/usr/bin/env python
# -*- coding: utf-8 -*-
import os, pathlib, sys,logging,string,csv,json,tempfile,re

sys.path.append(os.getcwd())

parent_path = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(parent_path))

master_path = parent_path.parent
sys.path.append(str(master_path))

project_path = master_path.parent
sys.path.append(str(project_path))

from typing import List,Dict,Union,Optional
from collections import OrderedDict

from functools import lru_cache

import fitz
import cleantext
from rapidfuzz import  fuzz
from rapidfuzz import process as fuzz_process

from Config.setting import config

####################################################################################################################################################################################################################
FORMAT = '%(levelname)s: %(asctime)-15s: %(filename)s: %(funcName)s: %(module)s: %(message)s'
logging.basicConfig(filename=config.log_file_path, level=logging.INFO, format=FORMAT)
LOGGER = logging.getLogger(__name__)

LOGGER.setLevel(logging.INFO)
fileHandler = logging.FileHandler(config.log_file_path)
fileHandler.setFormatter(FORMAT)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(FORMAT)

####################################################################################################################################################################################################################

@lru_cache(maxsize=None)
def toc_keywords(file_path:Union[str,pathlib.Path]):
    word4search={}
    with open(file_path,'r',encoding='utf-8') as f:
        for line in f.readlines() :
            t_, lang, t_words=line.strip().split('\t')
            if t_ not in word4search:
                word4search[t_]={'chi':[], 'eng':[]}
            word4search[t_][lang].append(t_words)
    return word4search

toc_keywords_dict=toc_keywords(config.search_word_file)

#########-----------------------------------------------------------------------------------------------------------------

def toc_search(toc_pages,tag:str='cornerstone',lang:str='eng'):
    fuzz_toc = {t: fuzz_process.extractOne(t, choices=toc_keywords_dict[tag][lang], scorer=fuzz.WRatio)[1] for t in    toc_pages}
    tag_toc = max(fuzz_toc, key=fuzz_toc.get)
    tag_pages=toc_pages[tag_toc]
    tag_pages=list(filter(lambda x:x>=0,tag_pages))
    return tag_pages,tag_toc

#########-----------------------------------------------------------------------------------------------------------------

def fetch_toc_pages(fitz_toc):
    raw_toc = OrderedDict()
    for i, item in enumerate(fitz_toc):
        lvl, title, pno, ddict = item

        row_text = str(title, )

        row_text = ' '.join([w.capitalize() for w in row_text.split(' ')])
        row_text = cleantext.replace_emails(row_text,'')
        row_text = cleantext.replace_urls(row_text,'')
        row_text = cleantext.normalize_whitespace(row_text)

        toc_pagenum = int(pno)
        raw_toc[i] = {'content': row_text, 'start': toc_pagenum, }

    toc = {}
    for k, v in raw_toc.items():
        if k < max(raw_toc.keys()):
            start = v['start'] - 1
            end = int(raw_toc[k + 1].get('start')) - 1
            toc[v['content']] = list(range(start, end + 1))  # {'start': start, 'end': end}
    return toc

#########-----------------------------------------------------------------------------------------------------------------
@lru_cache(maxsize=None)
def locate_pages(pdf_file_path,tag='cornerstone',lang='eng'):

    doc = fitz.open(pdf_file_path)
    fitz_toc = doc.get_toc(simple = False)
    if len(fitz_toc) == 0:
        logging.error("No Table of Contents available")
        return None,None
    else:
        toc_pages=fetch_toc_pages(fitz_toc)
        pi_pages,tag_toc =toc_search(toc_pages, tag= tag, lang=lang)
        if not pi_pages:
            logging.error(f'cannot find the pages of "{tag}" for stocks:{pdf_file_path}')
            return [],None
        else:
            return pi_pages, tag_toc


# if __name__=='__main__':
#     for k,v in toc_keywords_dict.items():
#         print(k,v,'\n')
