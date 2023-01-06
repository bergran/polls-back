import gzip
import time
from datetime import datetime
from typing import Callable

from fastapi import FastAPI
from prometheus_client import Summary, Histogram, Counter, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST, \
    REGISTRY, Gauge
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info
from starlette.requests import Request
from starlette.responses import Response

from src.modules.polls.presentation.views import api_router as polls_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(polls_router, prefix="/api/v1")


@app.get("/metrics", include_in_schema=False)
def metrics(request: Request):
    """Endpoint that serves Prometheus metrics."""
    collector_registry = REGISTRY
    if "gzip" in request.headers.get("Accept-Encoding", ""):
        resp = Response(content=gzip.compress(generate_latest(collector_registry)))
        resp.headers["Content-Type"] = CONTENT_TYPE_LATEST
        resp.headers["Content-Encoding"] = "gzip"
    else:
        resp = Response(content=generate_latest(collector_registry))
        resp.headers["Content-Type"] = CONTENT_TYPE_LATEST

    return resp


SUMMARY = Summary(
    "http_request_summary", "Requests summary that it's going to metric requests by latency", labelnames=("method", "status_code", "path")
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    now = datetime.now()
    response = None
    try:
        response = await call_next(request)
    finally:
        request_path = (
            request.scope["route"].path
            if "route" in request.scope
            else request.url.path
        )
        labels = {
            "method": request.method,
            "path": request_path,
            "status_code": response.status_code if response else 500
        }
        final_datetime = (datetime.now() - now).microseconds / 1000
        SUMMARY.labels(**labels).observe(final_datetime)

    return response
