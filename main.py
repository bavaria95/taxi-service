from datetime import datetime

from fastapi import FastAPI


app = FastAPI()


@app.get("/api")
def healthcheck():
    return {"status": "OK", "time": datetime.utcnow()}
