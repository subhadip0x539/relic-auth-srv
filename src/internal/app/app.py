from config import config
from internal.infra import HttpServer
from internal.router import router

http = (
    HttpServer().host(config.server.host).port(config.server.port).cors().router(router)
)
