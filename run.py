from fastapi import FastAPI
import uvicorn

import api.routes

app = FastAPI()

app.include_router(api.routes.router)

if __name__ == "__main__":
    uvicorn.run("run:app", host='0.0.0.0', port=6110, reload=True)
