import asyncio
import time

from fastapi import FastAPI

app = FastAPI()


async def io_task(name: str, delay: int):
    await asyncio.sleep(delay)
    return f"{name} completed"


@app.get("/")
async def home():
    return {"message": "Async API is running"}


@app.get("/async-demo")
async def async_demo():
    start = time.perf_counter()

    results = await asyncio.gather(
        io_task("Task A", 2),
        io_task("Task B", 2),
        io_task("Task C", 2),
    )

    elapsed = time.perf_counter() - start

    return {
        "results": results,
        "total_time_seconds": round(elapsed, 2)
    }

@app.get("/safe-async-demo")
async def safe_async_demo():

    async def safe_task(name, delay):
        try:
            await asyncio.sleep(delay)
            return f"{name} completed"

        except asyncio.CancelledError:
            return f"{name} cancelled"

    try:
        results = await asyncio.wait_for(
            asyncio.gather(
                safe_task("Task A", 1),
                safe_task("Task B", 2),
                safe_task("Task C", 1)
            ),
            timeout=5
        )

        return {
            "status": "success",
            "results": results
        }

    except asyncio.TimeoutError:
        return {
            "status": "timeout",
            "message": "Tasks took too long"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }