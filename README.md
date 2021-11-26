# 

The main script, server.py, is an API framework made up of three key components, FastAPI, hypercorn and allow-cross-origin domain middleware. 
The server.py script has few dependences inside the util folder and all configurations and high-level parameters (e.g. IP, port, external APIs,etc ) are all specified in the setting.py of Config folder.

### Fastapi:  python-based high-performance web framework used to create Rest APIs
- Its key features are that is fast, up to 300% faster to code, fewer bugs, easy to use, and production-friendly.
- Its performance can be compared with NodeJS and Go and it is rated as one of the fastest Python frameworks available. 
- Tech giants like Microsoft, Netflix, Uber amongst many other corporations are already started building their APIs with the FastAPI library. 


### Hypercorn :ASGI web server 
- Hypercorn is an ASGI web server based on the sans-io hyper, h11, h2, and wsproto libraries and inspired by Gunicorn. 
- Hypercorn supports HTTP/1, HTTP/2, WebSockets (over HTTP/1 and HTTP/2), ASGI/2, and ASGI/3 specifications. 
- Hypercorn can utilise asyncio, uvloop, or trio worker types.

### Server IPs
- UAT: 10.200.23.218
- production: 10.200.22.237

Folder path: /opt/etnet/ipo_cornerstone_table

### Executions of Command lines
- locate cursor to the folder path: /opt/etnet/ipo_cornerstone_table
- Manuel trigger: python3 server.py
- Background trigger : systemctl start ipo_cornerstone_table.service 
- Background stop:  systemctl stop ipo_cornerstone_table.service

# Dependencies
- setting.py in Config Folder
- asa_handle.py in util folder : handle pdf file download and filetype checking from asa system
- paid_service.py in util folder : use external pdf table scan API to extract table from pdf file if exists and convert the tables into excel format
- search_prospectus in util folder : search and locate numbers of pdf pages containing "cornerstone" information

-----------------------------------------------------------------------------------------------------------------------------------------------------------
### Setting.py
All high-leve parameters are stored in config.yaml file of Config folder and the setting.py script aims to convert all parameters into python objects for further reuse.

high-low parameter setting includeIP:
IP: please refer to server IPs above
Port: 8007
API route: cornerstone

asa url: http://10.1.8.151/InfoPool-ASA/SingleFileTx.do?reqid=802b&server=FILESERVER&filepath= 
External pdf table extraction API key: p5lNdMtm5BNHvQs0WAzpTcGeSaQMzhYeAw6kUwdl  (will  be substituted by new API key once the quota is used up) 

functional file path:
log file: /IPO_cornerstone.log
keywords: /search_words.txt  (this text file contains words for searching relevant data in the Table of Content of pdf file)

-----------------------------------------------------------------------------------------------------------------------------------------------------------
### asa_handle.py

- three inputs  
-- asa url (http://10.1.8.151/InfoPool-ASA/SingleFileTx.do?reqid=802b&server=FILESERVER&filepath=<asa pdf file > )
-- stockcode : int
-- filetype : either AR (allotment result/分派結果, ~10-20 page) and prospectus (招股書 ~200-400 pages)
  
- Two process : 
-- download pdf file to temporary file path (memory-based), such that the pdf file will be removed once the table extraction process is completed
-- checking if file extension is .pdf. if yes, pass, otherwise, return statuscode 404, with message "file extension is not .pdf"

- output:
-- pdf file stored in temporary path and trigger the table extraction application functioned by paid_service.py
-- 404 status code with message "file extension is not .pdf" and no further process will be triggered. 

 -----------------------------------------------------------------------------------------------------------------------------------------------------------
 ### search_prospectus.py
 It aims to detect which pdf pages contain the "cornerstone investors" information within the several hundreds pdf pages. The script is only triggered
  
  
 ### paid_service.py
 - input : 
 -- local temporary file path of the downloaded pdf file from asa
 -- numbers of pdf pages containing "cornerstone
  
 - process
 -- call the external API by python module ExtracTable with required API key stored in config.yaml
 -- pass the local 
 
