from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


class HttpServer:
    def __init__(self):
        self._host = "localhost"
        self._port = 8080
        self._reload = True
        self.app = FastAPI(title="RELIC CORE SRV")

    def host(self, host: str) -> "HttpServer":
        self._host = host
        return self

    def port(self, port: int) -> "HttpServer":
        self._port = port
        return self

    def router(self, router: APIRouter):
        self.app.include_router(router)
        return self

    def cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        return self

    def serve(self):
        uvicorn.run(
            "internal.app.app:http.app",
            host=self._host,
            port=self._port,
            reload=self._reload,
        )
