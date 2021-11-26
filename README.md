# 

The main script, server.py, is an API framework made up of three key components, FastAPI, hypercorn and cross-domain middleware. 
The server.py script has few dependences inside the util folder and all configurations and high-level parameters (e.g. IP, port, external APIs,etc ) are all specified in the setting.py of Config folder.

### Fastapi:  python-based high-performance web framework used to create Rest APIs
- Its key features are that is fast, up to 300% faster to code, fewer bugs, easy to use, and production-friendly.
- Its performance can be compared with NodeJS and Go and it is rated as one of the fastest Python frameworks available. 
- Tech giants like Microsoft, Netflix, Uber amongst many other corporations are already started building their APIs with the FastAPI library. 


### Hypercorn :ASGI web server 
- Hypercorn is an ASGI web server based on the sans-io hyper, h11, h2, and wsproto libraries and inspired by Gunicorn. 
- Hypercorn supports HTTP/1, HTTP/2, WebSockets (over HTTP/1 and HTTP/2), ASGI/2, and ASGI/3 specifications. 
- Hypercorn can utilise asyncio, uvloop, or trio worker types.

### Command 
