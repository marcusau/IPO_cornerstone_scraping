
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

from Config.setting import config
from util.object_model import asa_obj
import openpyxl
import requests

##########################################################################################################
FORMAT = '%(levelname)s: %(asctime)-15s: %(filename)s: %(funcName)s: %(module)s: %(message)s'
logging.basicConfig(filename=config.log_file_path, level=logging.INFO, format=FORMAT)
LOGGER = logging.getLogger(__name__)

LOGGER.setLevel(logging.INFO)
fileHandler = logging.FileHandler(config.log_file_path)
fileHandler.setFormatter(FORMAT)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(FORMAT)

##########################################################################################################
def check_filetype_function(asa:asa_obj):
    if asa.file_ext is None:
        asa.file_ext_check=False
        asa.file_ext_msg=f"cannot guess file type of {asa.url} "
    elif asa.file_ext is not 'pdf':
        asa.file_ext_check = False
        asa.file_ext_msg =f"this is not pdf file in  {asa.url} "
    else:
        asa.file_ext_check = True
        asa.file_ext_msg =f"pdf file from {asa.url} is save at {asa.file_path} "
    return asa


##########################################################################################################
def download_asa(asa:asa_obj):

    asa_response = requests.get(asa.url)
    if asa_response.status_code not in [200,201]:
        asa.file_ext_check=False
        asa.status = 'failure'
        asa.file_ext_msg=f'cannot download pdf file from {asa.url}'
        asa.status_code=404
    else:
        asa_content=asa_response.content
        asa.file_ext= filetype.guess(asa_content).extension
        asa=check_filetype_function(asa)

        if not asa.file_ext_check:
            asa.status_code=404
            asa.status='failure'
        else:
            asa.status_code = 200
            with open(asa.file_path, 'wb') as f:
                 f.write(asa_content)
            asa.status = 'success'

    return asa

def create_blank_xlsx(excel_path:str):
    wb = openpyxl.Workbook()
    wb.save(excel_path)
