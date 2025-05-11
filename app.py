import fastapi
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from FSParser import fetch_dedi_info, fetch_dedi_settings

app = FastAPI()


@app.get("/health")
def health_check():
    """
    Health check endpoint to verify if the service is running.
    """
    return JSONResponse(content={"status": "healthy"}, status_code=200)


@app.get("/server_info")
def get_server_info():
    """
    Endpoint to fetch server information.
    """
    try:
        info = fetch_dedi_info()
        if info is None:
            raise HTTPException(status_code=500, detail="Failed fetching server info.")
        return JSONResponse(content=info, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/game_settings")
def get_game_settings():
    """
    Endpoint to fetch server information.
    """
    try:
        info = fetch_dedi_settings()
        if info is None:
            raise HTTPException(status_code=500, detail="Failed fetching server info.")
        return JSONResponse(content=info, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
