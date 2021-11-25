#/usr/bin/env python
# -*- coding: utf-8 -*-
import os, pathlib, sys,logging, tempfile, filetype
from typing import Union
sys.path.append(os.getcwd())

parent_path = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(parent_path))

master_path = parent_path.parent
sys.path.append(str(master_path))

project_path = master_path.parent
sys.path.append(str(project_path))

from pydantic import BaseModel
##########################################################################################################
class asa_obj(BaseModel):
    stock_code: str
    url:str=''
    file_path:str
    file_type:str
    file_ext: Union[str, None]=None
    file_ext_check:bool=False
    file_ext_msg:str= ''
    status:str='error'
    cornerstone_toc_tag:str=None
    cornerstone_page=[]
    excel_path:str=None
    num_table:int=0
    status_code:int