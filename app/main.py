from fastapi import FastAPI
from app.api.v1.endpoints import organizations

app = FastAPI(title="Directory API")

app.include_router(
    organizations.router, prefix="/api/v1/organizations", tags=["organizations"]
)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
