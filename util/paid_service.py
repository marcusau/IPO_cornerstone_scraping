
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

from ExtractTable import ExtractTable
import pandas as pd
import openpyxl
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

et_sess = ExtractTable(config.ExtractTable_pay_service.API_key)

##########################################################################################################

def pdf2excel_function( asa:asa_obj):
    #print(f"pdf read: {asa.file_path}")

        if asa.file_type== "prospectus":
            print(f'pdf page: {asa.cornerstone_page[0]}-{asa.cornerstone_page[-1]}')
            print(f'file type: {asa.file_type}')
            table_data = et_sess.process_file(filepath=asa.file_path,  pages=f'{asa.cornerstone_page[0]}-{asa.cornerstone_page[-1]}' , output_format="df")#if asa.file_type is 'prospectus' else 'all'
            logging.info(f'{len(table_data)} tables detected in {asa.file_path}')
            print(f'{len(table_data)} tables detected in {asa.file_path}')
            asa.status_code = 200
        elif asa.file_type =='ar':
            print(f'file type: {asa.file_type}')
            table_data = et_sess.process_file(filepath=asa.file_path,  pages='all' , output_format="df")
            logging.info(f'{len(table_data)} tables detected in {asa.file_path}')
            print(f'{len(table_data)} tables detected in {asa.file_path}')
            asa.status_code = 200
        else:
            asa.status_code=404
            table_data =[]

        if asa.status_code ==404  :
            print(f'wrong pdf file type, we only accept prospectus or ar but we have {asa.file_type}')
            asa.file_ext_msg=f'wrong pdf file type, we only accept prospectus or ar but we have {asa.file_type}'
            asa.num_table = 0
            return asa
        elif asa.status_code==200 and len(table_data)==0:
            asa.num_table = 0
            asa.status_code=204
            asa.file_ext_msg = f"no table is detected from {asa.url}, pdf file type : {asa.file_type}, Please check pdf file type :{asa.file_type} or credit limit :{et_sess.check_usage().get( 'credits') - et_sess.check_usage().get('used')}"
            return asa
        else:
            try:
                asa.excel_path = pathlib.Path(asa.file_path).parent / (pathlib.Path(asa.file_path).stem + '.xlsx') #pathlib.Path(asa.file_path).parent
                writer = pd.ExcelWriter(asa.excel_path.as_posix(), engine='xlsxwriter')
                for i, t in enumerate(table_data):
                    t.to_excel(writer, sheet_name=f'{str(i + 1)}', index=False, header=False)
                writer.save()

                logging.info(f'{len(table_data)} tables are saved in excel path: {asa.excel_path}')
                print(f'{len(table_data)} tables are saved in excel path: {asa.excel_path}')
                asa.num_table=len(table_data)
                return asa



            except:
                asa.num_table = 0
                asa.status_code=404
                print(f'wrong pdf file type, we only accept prospectus or ar but we have {asa.file_type}')
                asa.file_ext_msg=f"error on table extraction from {asa.url}, Please credit limit :{et_sess.check_usage().get('credits') - et_sess.check_usage().get('used')}"
                return asa