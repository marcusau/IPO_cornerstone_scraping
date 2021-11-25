#/usr/bin/env python
# -*- coding: utf-8 -*-
import os, pathlib, sys,logging, tempfile, filetype, time,re
from typing import Union
sys.path.append(os.getcwd())

parent_path = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(parent_path))

master_path = parent_path.parent
sys.path.append(str(master_path))

project_path = master_path.parent
sys.path.append(str(project_path))

from Config.setting import config
from util import search_prospectus as search_toc_func
from util import asa_handle
from util import paid_service
from util.object_model import asa_obj

from functools import lru_cache

from fastapi import FastAPI, Form, HTTPException,Request
from fastapi.responses import FileResponse,StreamingResponse,JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import asyncio
from hypercorn.config import Config as Hypercorn_Config
from hypercorn.asyncio import serve



########  -------------------------- define  log file --------------------------  #####
FORMAT = '%(levelname)s: %(asctime)-15s: %(filename)s: %(funcName)s: %(module)s: %(message)s'
logging.basicConfig(filename=config.log_file_path, level=logging.DEBUG, format=FORMAT)
LOGGER = logging.getLogger(__file__)


LOGGER.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler(config.log_file_path)
fileHandler.setFormatter(FORMAT)
fileHandler.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(FORMAT)
consoleHandler.setLevel(logging.DEBUG)

####  ---------  instantiate Fastapi , temp path  ------------  #####
temp_dir= tempfile.TemporaryDirectory()

app = FastAPI()

origins=['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
####  ---------  instantiate hypercorn and config ------------  #####
Hypercorn_Config.bind = [f"{config.API.host}:{str(config.API.port)}"]

##########################################################################################################
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
def startup_event():
    et_usage = paid_service.et_sess.check_usage()
    logging.info(f"remaining credit from pay service:  {et_usage.get('credits') - et_usage.get('used')}")




@lru_cache()
@app.get(f"/{config.API.route.main}/asa")
def get_asa(code:str,path:str,file_type:str): #request:Request

    start=time.time()
    ####----------- receive parameter from requests ------------####
    logging.info(f'receive get request info : stockcode :{code}, url path: {path}, file type :{file_type}')
    print(f'receive get request info : stockcode :{code}, url path: {path}, file type :{type}')
    asa=asa_obj(stock_code=code,url=config.external_API.pdf + path,file_type=file_type,file_path=os.path.join(temp_dir.name,   f"{str(code)}_{file_type}.pdf"))

    ####----------- download pdf from asa to local temp path ------------####
    asa = asa_handle.download_asa(asa)
    logging.info(asa.file_ext_msg)


    if asa.file_ext_check :
        ####----------- if file typs is prosectus , check page range of cornerstone , else all ------------####
        if asa.file_type=='prospectus':
            pi_pages, tag_toc = search_toc_func.locate_pages(asa.file_path,tag='cornerstone',lang='eng')
            asa.cornerstone_page,asa.cornerstone_toc_tag =pi_pages,tag_toc

        ####----------- use third party : ExtractTable service ,to scan table and load to excel ------------####
        paid_service_start=time.time()

        asa_paid_service=paid_service.pdf2excel_function(asa)

        ####----------- use third party : check remaining quota------------####
        remaining_credits=paid_service.et_sess.check_usage().get(  'credits') - paid_service.et_sess.check_usage().get('used')
        logging.info(f"remaining credit from pay service: {remaining_credits} pages")
        print(f"remaining credit from pay service: {remaining_credits} pages")

        paid_service_finish = time.time()
        paid_service_processing_time=round(paid_service_finish-paid_service_start,2)
        print(f'paid_service_processing_time:{paid_service_processing_time}')
        finish = time.time()
        print(f'total processing time :{round(finish - start, 2)}, {asa.file_ext_msg}')
        ####-----------output 1: there is table , output excel------------####
        if asa_paid_service.num_table>0 and asa_paid_service.status_code==200:
            file_like = open(asa_paid_service.excel_path, mode="rb")
            print(f'total processing time :{ round(finish-start,2)}')
            headers = { 'status':'200','message':'success','Content-Disposition': f'''attachment; filename="{str(pathlib.Path(asa.file_path).stem + '.xlsx')}"''' }
            return StreamingResponse(file_like,      headers=headers,     media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
           # return FileResponse(asa.excel_path)
        elif asa_paid_service.num_table==0  and asa_paid_service.status_code==204:
            ####-----------output 2:  no table , output blank excel------------####

            return JSONResponse(status_code=asa_paid_service.status_code, content={"message": f"{asa.file_ext_msg}"})
        else:
            #raise HTTPException(status_code=404, detail=asa.file_ext_msg)
            return JSONResponse(status_code=asa_paid_service.status_code, content={"message": f"{asa.file_ext_msg}"})

            # asa.excel_path=asa.excel_path = pathlib.Path(asa.file_path).parent / (pathlib.Path(asa.file_path).stem + '.xlsx')
            # asa_handle.create_blank_xlsx(asa.excel_path)
            # file_like = open(asa.excel_path, mode="rb")
            # headers = {'status': '204','message':asa.file_ext_msg, 'Content-Disposition': f'''attachment; filename="{str(  pathlib.Path(asa.file_path).stem + '.xlsx')}"'''}
            # return StreamingResponse(file_like,     headers=headers,       media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    else:
        ####-----------output 3:  cannot download file , output blank excel------------####
        asa.status_code=404
        print(asa.file_ext_msg)
       # raise HTTPException(status_code=404,detail=asa.file_ext_msg)
        return JSONResponse(status_code=asa.status_code, content={"message": f"{asa.file_ext_msg}"})
        # asa.excel_path = asa.excel_path = pathlib.Path(asa.file_path).parent / ( pathlib.Path(asa.file_path).stem + '.xlsx')
        # asa_handle.create_blank_xlsx(asa.excel_path)
        # file_like = open(asa.excel_path, mode="rb")
        # headers = {'status': '404', 'message': asa.file_ext_msg,   'Content-Disposition': f'''attachment; filename="{str(   pathlib.Path(asa.file_path).stem + '.xlsx')}"'''}
        # return  StreamingResponse(file_like,  headers=headers,       media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


if __name__ == "__main__":

   asyncio.run(serve(app, Hypercorn_Config()))
