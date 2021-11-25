import dataclasses

#/usr/bin/env python
# -*- coding: utf-8 -*-
import os, pathlib, sys

sys.path.append(os.getcwd())

parent_path = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(parent_path))

master_path = parent_path.parent
sys.path.append(str(master_path))

project_path = master_path.parent
sys.path.append(str(project_path))

import yaml2pyclass


class Config(yaml2pyclass.CodeGenerator):
    @dataclasses.dataclass
    class ExternalApiClass:
        sec_firm: str
        pdf: str
    
    @dataclasses.dataclass
    class ApiClass:
        @dataclasses.dataclass
        class RouteClass:
            main: str
        
        port: int
        host: str
        route: RouteClass
    
    @dataclasses.dataclass
    class ExtracttablePayServiceClass:
        API_key: str
    
    external_API: ExternalApiClass
    API: ApiClass
    log_file_path: str
    search_word_file: str
    ExtractTable_pay_service: ExtracttablePayServiceClass
