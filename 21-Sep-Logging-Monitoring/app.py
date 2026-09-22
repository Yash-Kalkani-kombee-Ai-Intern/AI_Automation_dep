import time

from fastapi import FastAPI, Request

from logger import logger
from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from metrics import REQUEST_COUNT, REQUEST_LATENCY

app = FastAPI(title="Monitoring Demo")

@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    start_time = time.perf_counter()

    logger.info(
        "Request started | method=%s | path=%s",
        request.method,
        request.url.path,
    )

    response = await call_next(request)

    process_time = time.perf_counter() - start_time
    latency_ms = process_time * 1000

    REQUEST_COUNT.labels(
        method=request.method,
        path=request.url.path,
        status=response.status_code,
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        path=request.url.path,
    ).observe(process_time)

    logger.info(
        "Request completed | method=%s | path=%s | status=%s | latency=%.2fms",
        request.method,
        request.url.path,
        response.status_code,
        latency_ms,
    )

    return response

@app.get("/")
def home():
    logger.info("Home endpoint called")

    return {
        "message": "Monitoring demo is running"
    }


@app.get("/health")
def health():
    logger.info("Health check requested")

    return {
        "status": "healthy"
    }


@app.get("/error")
def error_demo():
    try:
        result = 10 / 0

        return {
            "result": result
        }

    except ZeroDivisionError:
        logger.error("Division by zero error occurred")

        return {
            "error": "Something went wrong"
        }


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)